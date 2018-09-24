# coding=utf-8
import requests

# import pygbif

__version__ = '0.2.2.1'
__title__ = 'pygbif'
__author__ = 'Scott Chamberlain'
__license__ = 'MIT'

# Original logic by Scott Chaimberlain, extracted from his pygbif repo
# Modified by Tim and Etienne to use QgsNetworkAccessManager rather
from qgis.PyQt.QtCore import QUrl, QEventLoop
from qgis.core import QgsMessageLog, QgsFileDownloader

from tempfile import mkstemp
import json


class NoResultException(Exception):
    pass


def gbif_GET(url, args, **kwargs):
    handle, output_path = mkstemp()
    QgsMessageLog.logMessage(
        'gbif_GET outfile: %s' % output_path, 'SpeciesExplorer', 0)
    QgsMessageLog.logMessage('gbif_GET URL: %s' % url, 'SpeciesExplorer', 0)
    loop = QEventLoop()
    downloader = QgsFileDownloader(QUrl(url), output_path, delayStart=True)
    downloader.downloadExited.connect(loop.quit)
    downloader.startDownload()
    loop.exec_()
    file = open(output_path, 'rt', encoding='utf-8')
    data = file.read()
    file.close()

    return json.loads(data, encoding='utf-8')


gbif_baseurl = "http://api.gbif.org/v1/"

requests_argset = ['timeout', 'cookies', 'auth', 'allow_redirects',
                   'proxies', 'verify', 'stream', 'cert']


def bn(x):
    if x:
        return x
    else:
        return None


def check_data(x, y):
    if len2(x) == 1:
        testdata = [x]
    else:
        testdata = x

    for z in testdata:
        if z not in y:
            raise TypeError(z + ' is not one of the choices')


def len2(x):
    if x.__class__ is str:
        return len([x])
    else:
        return len(x)


def get_meta(x):
    if has_meta(x):
        return {z: x[z] for z in ['offset', 'limit', 'endOfRecords']}
    else:
        return None


def has_meta(x):
    if x.__class__ != dict:
        return False
    else:
        tmp = [y in x.keys() for y in ['offset', 'limit', 'endOfRecords']]
        return True in tmp


def name_parser(name, **kwargs):
  '''
  Parse taxon names using the GBIF name parser

  :param name: [str] A character vector of scientific names. (required)

  reference: http://www.gbif.org/developer/species#parser

  Usage::

      from pygbif import species
      species.name_parser('x Agropogon littoralis')
      species.name_parser(['Arrhenatherum elatius var. elatius',
        'Secale cereale subsp. cereale', 'Secale cereale ssp. cereale',
        'Vanessa atalanta (Linnaeus, 1758)'])
  '''
  url = gbif_baseurl + 'parser/name?name=' + name
  return gbif_GET(url, name, **kwargs)


def name_usage(key=None, name=None, data='all', language=None,
               datasetKey=None, uuid=None, sourceId=None, rank=None,
               shortname=None,
               limit=100, offset=None, **kwargs):
    '''
    Lookup details for specific names in all taxonomies in GBIF.

    :param key: [fixnum] A GBIF key for a taxon
    :param name: [str] Filters by a case insensitive, canonical namestring,
         e.g. 'Puma concolor'
    :param data: [str] The type of data to get. Default: ``all``. Options: ``all``,
        ``verbatim``, ``name``, ``parents``, ``children``,
        ``related``, ``synonyms``, ``descriptions``, ``distributions``, ``media``,
        ``references``, ``speciesProfiles``, ``vernacularNames``, ``typeSpecimens``,
        ``root``
    :param language: [str] Language, default is english
    :param datasetKey: [str] Filters by the dataset's key (a uuid)
    :param uuid: [str] A uuid for a dataset. Should give exact same results as datasetKey.
    :param sourceId: [fixnum] Filters by the source identifier.
    :param rank: [str] Taxonomic rank. Filters by taxonomic rank as one of:
            ``CLASS``, ``CULTIVAR``, ``CULTIVAR_GROUP``, ``DOMAIN``, ``FAMILY``, ``FORM``, ``GENUS``, ``INFORMAL``,
            ``INFRAGENERIC_NAME``, ``INFRAORDER``, ``INFRASPECIFIC_NAME``, ``INFRASUBSPECIFIC_NAME``,
            ``KINGDOM``, ``ORDER``, ``PHYLUM``, ``SECTION``, ``SERIES``, ``SPECIES``, ``STRAIN``, ``SUBCLASS``, ``SUBFAMILY``,
            ``SUBFORM``, ``SUBGENUS``, ``SUBKINGDOM``, ``SUBORDER``, ``SUBPHYLUM``, ``SUBSECTION``, ``SUBSERIES``,
            ``SUBSPECIES``, ``SUBTRIBE``, ``SUBVARIETY``, ``SUPERCLASS``, ``SUPERFAMILY``, ``SUPERORDER``,
            ``SUPERPHYLUM``, ``SUPRAGENERIC_NAME``, ``TRIBE``, ``UNRANKED``, ``VARIETY``
    :param shortname: [str] A short name..need more info on this?
    :param limit: [fixnum] Number of records to return. Default: ``100``. Maximum: ``1000``. (optional)
    :param offset: [fixnum] Record number to start at. (optional)

    References: http://www.gbif.org/developer/species#nameUsages

    Usage::

            from pygbif import species

            species.name_usage(key=1)

            # Name usage for a taxonomic name
            species.name_usage(name='Puma', rank="GENUS")

            # All name usages
            species.name_usage()

            # References for a name usage
            species.name_usage(key=2435099, data='references')

            # Species profiles, descriptions
            species.name_usage(key=3119195, data='speciesProfiles')
            species.name_usage(key=3119195, data='descriptions')
            species.name_usage(key=2435099, data='children')

            # Vernacular names for a name usage
            species.name_usage(key=3119195, data='vernacularNames')

            # Limit number of results returned
            species.name_usage(key=3119195, data='vernacularNames', limit=3)

            # Search for names by dataset with datasetKey parameter
            species.name_usage(datasetKey="d7dddbf4-2cf0-4f39-9b2a-bb099caae36c")

            # Search for a particular language
            species.name_usage(key=3119195, language="FRENCH", data='vernacularNames')
    '''
    args = {'language': language, 'name': name, 'datasetKey': datasetKey,
            'rank': rank, 'sourceId': sourceId, 'limit': limit,
            'offset': offset}
    data_choices = ['all', 'verbatim', 'name', 'parents', 'children',
                    'related', 'synonyms', 'descriptions',
                    'distributions', 'media', 'references', 'speciesProfiles',
                    'vernacularNames', 'typeSpecimens', 'root']
    check_data(data, data_choices)
    if len2(data) == 1:
        return name_usage_fetch(data, key, shortname, uuid, args, **kwargs)
    else:
        return [name_usage_fetch(x, key, shortname, uuid, args, **kwargs) for x
                in data]


def name_usage_fetch(x, key, shortname, uuid, args, **kwargs):
    if x is not 'all' and key is None:
        raise TypeError(
            'You must specify `key` if `data` does not equal `all`')

    if x is 'all' and key is None:
        url = gbif_baseurl + 'species'
    else:
        if x is 'all' and key is not None:
            url = gbif_baseurl + 'species/' + str(key)
        else:
            if x in ['verbatim', 'name', 'parents', 'children', 'related',
                     'synonyms', 'descriptions',
                     'distributions', 'media', 'references', 'speciesProfiles',
                     'vernacularNames', 'typeSpecimens']:
                url = gbif_baseurl + 'species/%s/%s' % (str(key), x)
            else:
                if x is 'root':
                    url = gbif_baseurl + 'species/%s/%s' % (uuid, shortname)

    res = gbif_GET(url, args, **kwargs)
    return res
