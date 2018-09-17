# SpeciesExplorer

SpeciesExplorer is a QGIS (3 or greater) plugin for quickly retrieving species occurrence data from GBIF (http://gbif.org).

[![IMAGE ALT TEXT](http://img.youtube.com/vi/La2ml0yDW6M/0.jpg)](http://www.youtube.com/watch?v=La2ml0yDW6M "Species Explorer")

I  published a plugin about 8 years ago that fetched GBIF data in QGIS. It was part of a toolkit for running [openModeller] (http://openmodeller.sourceforge.net) for performing ecological niche modelling. But the plugin was written in C++ and not easy to maintain or distribute to different platforms. I am aiming to eventually re-instate openModeller support in QGIS but using an approach that makes it more broadly accessible. The plugin will fetch the openModeller C++ compiled binary for your platform and the rest will be written in python to make it easier to maintain and extend (and hopefully garner contributions from others). 

## Funders wanted

If you are interested and able to fund this work please contact me.

## How it works

The plugin will create an in-memory layer for each search result. The attribute table of the layer will contain all the standard metadata returned by a GBIF occurrence search. To save the layer permanently, right click on it and use the built-in QGIS "save as" functionality.

You can install the plugin from the QGIS plugin repository as shown in the above video. Alternatively you can get the release zip file from the [releases page](https://github.com/kartoza/SpeciesExplorer/releases) and install it using the 'Install from Zip' in the QGIS plugin manager tab.

# Contributing and reporting issues

I would welcome any contributions, please do so via a [pull request](https://github.com/kartoza/SpeciesExplorer/pulls). If you encounter any bugs with the plugin, please file an [issue](https://github.com/kartoza/SpeciesExplorer/issues).

# Contact / credits

This plugin was developed by Tim Sutton
tim@kartoza.com
