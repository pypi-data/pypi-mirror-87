# resif data reporter
Cet outil collecte sur un ou plusieurs espaces disques en structure SDS l'espace occupé par les réseaux sismo.


## À propos
-   licence : Ce projet est livré sous licence GPLv3 ou plus
-   auteur : Jonathan Schaeffer <jonathan.schaeffer@univ-grenoble-alpes.fr>

### Collecte des volumes

Les données sont dans un ou plusieurs dossier(s) contenant un sous-dossier par année et pour chaque année, un dossier par réseau.

Dans le rapport final, on souhaite distinguer les réseaux permanents des expériences temporaires.

Les données collectées sont écrites en YAML dans un fichier cache.

Les données sont ensuite écrites dans une base postgres.

## Configuration

Le script de collecte a besoin d'un fichier de configuration. Le fichier `config.yml.example` fournit toute la documentation nécessaire pour un paramétrage initial.

Par défaut, le script collecte les données (en faisant des `du`), les compile et les écrit dans le fichier `data.yaml`.

Si les données contenues dans `data.yaml` ne sont pas plus anciennes que ce que spécifie la configuration `data_cache_ttl` (en jour), alors le script scanne le fichier data.json pour le restituer et n'effectue pas le scan des volumes.


### Postgres

Quelle config sur le serveur postgres ? Quelle base et quelles tables créer ?

``` sql
CREATE TYPE sismo_data_type AS ENUM('bud', 'validated')
CREATE TABLE dataholdings (network varchar(2),
                          year varchar(4),
                          station varchar(5),
                          channel varchar(3),
                          quality varchar(1),
                          type sismo_data_type,
                          size bigint,
                          is_permanent boolean,
                          date date);
```


## Tester


### Lancer des tests unitaires

```shell
pip install -e .
pytest
```


### Lancer un docker postgres

```shell
docker pull postgres
docker run --name pg -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```


## Configuration

Un fichier de Configuration pour les tests :
``` yaml
    volumes:
      - path: /tmp/pytest-of-schaeffj/pytest-22/validated/
        type: validated
      - path: /tmp/pytest-of-schaeffj/pytest-22/bud
        type: bud
    postgres:
      host: localhost
      database: stats
      port: 5432
      user: postgres
      password: mysecretpassword

    metadata:    # Information about the gathered data. Used to tag the timeserie values
      permanent_networks: #  List all permanent networks here. Otherwise, they will be considered as temporary
        - CL
        - GL
        - MQ
        - ND
        - PF
        - RD
        - FR
        - G
        - RA
        - WI
```

## Tester le programme complet :

    python resif_data_reporter.py --config config.yml
