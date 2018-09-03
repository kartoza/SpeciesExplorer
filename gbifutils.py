# coding=utf-8
import requests

# import pygbif

__version__ = '0.2.2.1'
__title__ = 'pygbif'
__author__ = 'Scott Chamberlain'
__license__ = 'MIT'

# Modified by Tim to use QgsNetworkAccessManager rather
from qgis.PyQt.QtCore import QUrl, QEventLoop
from qgis.core import (
    QgsNetworkAccessManager, QgsMessageLog, QgsFileDownloader)
from qgis.PyQt.QtNetwork import QNetworkRequest

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
