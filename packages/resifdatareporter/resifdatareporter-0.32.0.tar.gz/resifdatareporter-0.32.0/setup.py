from io import open
from setuptools import setup, find_packages
import resifdatareporter

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='resifdatareporter',
    version=resifdatareporter.__version__,
    description='Scans the resif data repository and compute metrics. Sends the result in influxdb or postgres',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Jonathan Schaeffer',
    author_email='jonathan.schaeffer@univ-grenoble-alpes.fr',
    maintainer='Jonathan Schaeffer',
    maintainer_email='jonathan.schaeffer@univ-grenoble-alpes.fr',
    url='https://gricad-gitlab.univ-grenoble-alpes.fr/OSUG/RESIF/resif_data_reporter',
    license='GPL-3.0',
    packages=find_packages(),
    install_requires=[
        'fdsnextender',
        'Click',
        'PyYAML',
        'psycopg2-binary',
        'h5py'
    ],
    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

    ],

    tests_require=['coverage', 'pytest'],
    entry_points='''
    [console_scripts]
    resifdatareporter=resifdatareporter.resifdatareporter:cli
    '''
)
