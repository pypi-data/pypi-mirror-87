#!/bin/env python

import logging
import os
import sys
import io
import subprocess
import re
from datetime import datetime, date, timedelta
import yaml
import psycopg2
import click
import h5py
from fdsnextender import FdsnExtender
from resifdatareporter import __version__
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def scan_volume(path):
    """
    Scanne un volume indiqué par son chemin (path).
    La fonction lance une commande "du -d4 path" et analyse chaque ligne renvoyée.
    Elle renvoie une liste de dictionnaires :
    [ {year: 2011, network: 'G', size: '100', station: 'STAT', channel: 'BHZ.D'}, ...]
    """
    data = []
    volume = os.path.realpath(path)+'/'
    logger.debug("Volume %s", volume)
    starttime = datetime.now()
    proc = subprocess.Popen(["du", "--exclude", ".snapshot", "-b", "-d4", volume], stdout=subprocess.PIPE)
    for l in io.TextIOWrapper(proc.stdout, encoding='utf-8'):
        l = l.strip()
        logger.debug("Scanned %s",l)
        (size, path) = l.split('\t')
        # On ne garde que le chemin qui nous intéresse
        path = path.replace(volume, '').split('/')
        # Ne pas considérer le seul chemin de niveau 1
        if len(path) == 4:
            logger.debug("path: %s, size: %s", path, size)
            try:
                (channel, quality) = path[3].split('.')
            except ValueError:
                logger.info("%s is probably not a normal path. Skip it.", path)
                continue
            if re.match('[1-9][0-9]{3}', path[0]):
                data.append({'year': path[0], 'network': path[1], 'station': path[2],
                             'channel': channel, 'quality': quality, 'size': size})
            else:
                data.append({'year': path[1], 'network': path[0], 'station': path[2],
                             'channel': channel, 'quality': quality, 'size': size})
            logger.debug(data[-1])
    logger.debug("Volume scanned in %s", datetime.now() - starttime)
    return data

def scan_ph5_volume(volpath):
    """
    Un repertoire contenant des données nodes doit être analysé différemment
    - a minima, un /du/ du répertoire et on stocke l'info seulement pour le réseau
    - sinon, en analysant les volumes ph5, mais je ne sais pas si on en a vraiment besoin.
    """
    data = []
    volume = os.path.realpath(volpath)+'/'
    logger.debug("Volume %s", volume)
    proc = subprocess.Popen(["ls", volume], stdout=subprocess.PIPE)
    for l in io.TextIOWrapper(proc.stdout, encoding='utf-8'):
        network = l.strip()
        path = f"{volume}/{network}"
        logger.debug("Scanned %s", network)
        try:
            year = int(network[2:])
        except ValueError:
            # Bon, ça n'a pas marché, on fait quoi ?
            logger.error("Unable to get year from path %s. Ignoring this one", path)
            continue

        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for i in filenames:
                logger.debug("Scanning %s: file %s", network, i)
                if i.endswith('ph5'):
                    total = total + os.path.getsize(f"{path}/{i}")
        logger.debug("Total size of %s is %s (%s GB)", network, total, total/(1024**3) )
        # Make a statistic array with those stations dividing total size on each station.
        data.append({'type': 'ph5', 'year': year, 'network': network, 'station': None,
                         'channel': None, 'quality': None, 'size': total})
    return data


def scan_volumes(volumes):
    # volumes is a complex data type :
    # List of dictionaries of 2 elements (path and type)
    # [{path: /bla/bla, type: plop}, {path: /bli/bli, type: plip}]
    # En sortie, une liste de dictionnaires :
    # [ {stat}, {stat}, ]
    volume_stats = []
    starttime = datetime.now()
    for volume in volumes:
        logger.debug("Preparing scan of volume %s", volume['path'])
        if 'path' in volume:
            if 'type' in volume and volume['type'] == "ph5":
                stats = scan_ph5_volume(volume['path'])
            else:
                stats = scan_volume(volume['path'])
                # On rajoute le type comme un élément de chaque statistique
                if 'type' in volume:
                    for s in stats:
                        s['type'] = volume['type']
            if 'name' in volume:
                for s in stats:
                    s['volume'] = volume['name']
            volume_stats.append(stats)
            # If a type of data was specified, then we add this tag to the stats
        else:
            raise ValueError("Volume has no path key : %s" % (volume))
    # on applati la liste de listes :
    logger.info("All volumes scanned in %s",
                 (datetime.now() - starttime))
    return [x for vol in volume_stats for x in vol]


@click.command()
@click.option("--version", flag_value=True, default=False, help="Print version and exit")
@click.option('--config-file',  'configfile', type=click.File(), help='Configuration file path', envvar='CONFIG_FILE', show_default=True,
              default=f"{os.path.dirname(os.path.realpath(__file__))}/config.yml")
@click.option('--force-scan', flag_value=True, default=False, help='Force scanning of the archive')
@click.option('--dryrun', flag_value=True, default=False, help="Do not send metrics to database")
@click.option("--verbose", flag_value=True, default=False, help="Verbose mode")
@click.version_option(__version__)
def cli(configfile, force_scan, dryrun, verbose, version):
    """
    Command line interface. Stands as main
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
    logger.info("Starting")
    try:
        cfg = yaml.load(configfile, Loader=yaml.SafeLoader)
    except yaml.YAMLError as err:
        logger.error("Could not parse %s", configfile)
        logger.error(err)
        sys.exit(1)

    # At this point we ensure that configuration is sane.
    statistics = []
    today = date.today().strftime("%Y-%m-%d")

    if not force_scan:
        # Get last stat date
        conn = psycopg2.connect(dbname=cfg['postgres']['database'], user=cfg['postgres']['user'],
                                host=cfg['postgres']['host'], password=cfg['postgres']['password'], port=cfg['postgres']['port'])
        cur = conn.cursor()
        cur.execute('select distinct date from dataholdings order by date desc limit 1;')
        last_stat_date = cur.fetchone()[0]
        logger.info("Last report: %s", last_stat_date)
        conn.close()
        if date.today() - last_stat_date > timedelta(days=(cfg['cache_ttl'])):
            logger.info("Last report is old enough. Let's get the job done.")
        else:
            logger.info(
                "Last data report made at %s. Younger than %s. Don't scan",
                last_stat_date, cfg['cache_ttl'])
            sys.exit(0)

    statistics = scan_volumes(cfg['volumes'])

    # add the network_type (is the network permanent or not) to the statistic
    # also insert the extended network code.
    extender = FdsnExtender()
    for stat in statistics:
        # Les réseaux commençant par 1 à 9 et X Y Z sont des réseaux non
        # permanents
        stat['is_permanent'] = not re.match('^[1-9XYZ]', stat['network'])
        # Si le réseau temporaire est en 2 lettres, alors on veut son nom
        # étendu
        if not stat['is_permanent'] and len(stat['network']) < 3 :
            try:
                stat['network'] = extender.extend(
                    stat['network'], int(stat['year']))
            except ValueError:
                logger.debug("Network %s exists ?" % stat['network'])
        stat['date'] = today
        logger.debug(stat)

    if dryrun:
        logger.info("Dryrun mode, dump stats and exit")
        for stat in statistics:
            print(stat)
        sys.exit(0)
        # Write to postgres database
    if 'postgres' in cfg:
        logger.info('Writing to postgres database')
        conn = psycopg2.connect(dbname=cfg['postgres']['database'], user=cfg['postgres']['user'],
                                host=cfg['postgres']['host'], password=cfg['postgres']['password'], port=cfg['postgres']['port'])
        cur = conn.cursor()
        for stat in statistics:
            try:
                cur.execute(
                    """
                    INSERT INTO dataholdings (network, year, station, channel, quality, type, size, is_permanent, volume, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (network,year,station,channel,type,date) DO UPDATE SET size = EXCLUDED.size;
                    """,
                    (stat['network'], stat['year'], stat['station'], stat['channel'], stat['quality'], stat['type'], stat['size'], stat['is_permanent'], stat['volume'], stat['date']))
            except psycopg2.Error as err:
                logging.error(err)
                logging.info(cur.mogrify(
                    """
                    INSERT INTO dataholdings (network, year, station, channel, quality, type, size, is_permanent, volume, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (network,year,station,channel,type,date) DO UPDATE SET size = EXCLUDED.size;
                    """,
                    (stat['network'], stat['year'], stat['station'], stat['channel'], stat['quality'], stat['type'], stat['size'], stat['is_permanent'], stat['volume'], stat['date'])
                ))
        conn.commit()

if __name__ == "__main__":
    cli()
