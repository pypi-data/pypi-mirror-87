# pyglottolog

Programmatic access to [Glottolog data](https://github.com/glottolog/glottolog).

[![Build Status](https://github.com/glottolog/pyglottolog/workflows/tests/badge.svg)](https://github.com/glottolog/pyglottolog/actions?query=workflow%3Atests)
[![codecov](https://codecov.io/gh/glottolog/pyglottolog/branch/master/graph/badge.svg)](https://codecov.io/gh/glottolog/pyglottolog)
[![PyPI](https://img.shields.io/pypi/v/pyglottolog.svg)](https://pypi.org/project/pyglottolog)


## Install

To install `pyglottolog` you need a python installation on your system, running python >3.4. Run
```shell script
pip install pyglottolog
```

This will also install the command line interface `glottolog`.

**Note:** To make use of `pyglottolog` you also need a local copy of the
[Glottolog data](https://github.com/glottolog/glottolog). This can be
- a clone of the [glottolog/glottolog](https://github.com/clld/glottolog) repository or your fork of it,
- an unzipped [released version of Glottolog](https://github.com/glottolog/glottolog/releases) from GitHub,
- or an unzipped download of a [released version of Glottolog](https://doi.org/10.5281/zenodo.596479) from ZENODO.

Make sure you remember where this local copy of the data is located - you may
have to pass this location as option when using `pyglottolog`.

A convenient way to clone the data repository, keep it updated and access it
from `pyglottolog` is provided
by [`cldfbench`](https://pypi.org/project/cldfbench). See the [`README`](https://github.com/cldf/cldfbench#catalogs) for details.


## Python API

Using `pyglottolog`, Glottolog data can be accessed programmatically from within python programs.
All functionality is mediated through an instance of `pyglottolog.Glottolog`, e.g.
```python
>>> from pyglottolog import Glottolog
>>> glottolog = Glottolog('.')
>>> print(glottolog)
<Glottolog repos v0.2-259-g27ac0ef at /.../glottolog>
```

### Accessing languoid data

The data in languoid info files in the `languoids/tree` subdirectory is mainly accessed through
two methods:

```python
>>> glottolog.languoid('stan1295')
<Language stan1295>
>>> print(glottolog.languoid('stan1295'))
German [stan1295]
```

### Accessing reference data
```python
>>> print(api.bibfiles['hh.bib']['s:Karang:Tati-Harzani'])
@book{s:Karang:Tati-Harzani,
    author = {'Abd-al-'Ali Kārang},
    title = {Tāti va Harzani},
    publisher = {Tabriz: Tabriz University Press},
    address = {Tabriz},
    pages = {6+160},
    year = {1334 [1953]},
    glottolog_ref_id = {41999},
    hhtype = {grammar_sketch},
    inlg = {Farsi [pes]},
    lgcode = {Harzani [hrz]},
    macro_area = {Eurasia}
}
```

### Performance considerations

Reading the data for Glottolog's almost 25,000 languoids from the same number of files in individual
directories isn't particularly quick. So on average computers running
```python
>>> list(glottolog.languoids())
```
would take around 15 seconds.

Due to this, care should be taken not to read languoid data from disk repeatedly. In particular
"N+1"-type problems should be avoided, where one would read all languoid into memory and then look
up attributes on each languoid, thereby triggering new reads from disk. This may easily happen,
since attributes such as `Languoid.family` are implemented as
[properties](https://docs.python.org/3/howto/descriptor.html#properties), which traverse the
directory tree and read information from disk at **access** time.

To make it possible to avoid such problems, many of these properties can be substituted with a call
to a similar method of `Languoid`, which accepts a "node map" (i.e. a `dict` mapping `Languoid.id` 
to `Languoid` objects) as parameter, e.g. `Languoid.ancestors_from_nodemap` or
`Languoid.descendants_from_nodemap`. Typical usage would look as follows:
```python
>>> languoids = {l.id: l for l in glottolog.languoids()}
>>> for l in languoids.values():
...    if not l.ancestors_from_nodemap(languoids):
...        print('top-level {0}: {1}'.format(l.level, l.name))
```


### Accessing configuration data

The `config` subdirectory of Glottolog data contains machine readable metadata like the list
of macroareas. This information can be accessed via an instance of `Glottolog`, too, using the
stem of the filename as attribute name:
```python
>>> for ma in glottolog.macroareas.values():
...     print(ma.name)
...     
South America
Eurasia
Africa
Papunesia
North America
Australia
```

Note that the data read from the INI files is stored as `dict`, with section names (or explicit
`id` options) as keys and instances of the corresponding class in `pyglottolog.config` as
values.


## Command line interface

Command line functionality is implemented via sub-commands of `glottolog`. The list of
available sub-commands can be inspected running
```shell script
$ glottolog -h
usage: glottolog [-h] [--log-level LOG_LEVEL] [--repos REPOS]
                 [--repos-version REPOS_VERSION]
                 COMMAND ...

optional arguments:
  -h, --help            show this help message and exit
  --log-level LOG_LEVEL
                        log level [ERROR|WARN|INFO|DEBUG] (default: 20)
  --repos REPOS         clone of glottolog/glottolog
  --repos-version REPOS_VERSION
                        version of repository data. Requires a git clone!
                        (default: None)

available commands:
  Run "COMAMND -h" to get help for a specific command.

  COMMAND
    cldf                Dump Glottolog data as CLDF dataset
    create              Create a new languoid directory for a languoid
                        specified by name and level.
    edit                Open a languoid's INI file in a text editor.
    htmlmap             Create an HTML/Javascript map (using leaflet) of
                        Glottolog languoids.
    iso2codes           Map ISO codes to the list of all Glottolog languages
                        and dialects subsumed "under" it.
    langdatastats       List all metadata fields used in languoid INI files
                        and their frequency.
    langsearch          Search Glottolog languoids.
    languoids           Write languoids data to csv files
    refsearch           Search Glottolog references
    searchindex         Index
    show                Display details of a Glottolog object.
    tree                Print the classification tree starting at a specific
                        languoid.
```


### Extracting languoid data

Glottolog data is often integrated with other data or incorporated as reference
data in tools, e.g. as [LanguageTable](https://github.com/cldf/cldf/tree/master/components/languages)
in a [CLDF](https://cldf.clld.org) dataset.

To make this easier, `pyglottolog` provides the `languoids` subcommand, which
dumps basic languoid data into a CSVW file with accompanying metadata:

```shell script
glottolog languoids [--output=OUTDIR] [--version=VERSION]
```

This will create a CSVW package, i.e. 
- a CSV table `glottolog-languoids-VERSION.csv`
- and a JSON description `glottolog-languoids-VERSION.csv-metadata.json`

where `VERSION` is the result of running `git describe` on the data repository,
or the version string passed as`--version=VERSION` in case you are running the command
on an export of the repository or a download from ZENODO.


### Languoid search

To allow convenient search across all languoid info files, `pyglottolog` comes with functionality
to create and search a [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html) index. To do
so, run
```shell script
glottolog searchindex
```

This will take a couple of minutes and build an indeces of about 750 MB size at `build/`.

Now you can search the index, e.g. using alternative names as query:
```shell script
$ glottolog langsearch "Abipónok"
1 matches
Abipon [abip1241] language
languoids/tree/guai1249/guai1250/abip1241/md.ini
Abipónok [hu]

1 matches
```

But you can also exploit the schema defined in [pyglottolog.fts.get_langs_index](src/pyglottolog/fts.py):
```shell script
$ glottolog langsearch "country:Papua New Guinea"
...

Alamblak [alam1246] language
languoids/tree/sepi1257/sepi1258/east2496/alam1246/md.ini
Papua New Guinea (PG)

900 matches

$ glottolog --repos=. langsearch "iso:mal"
...

Malayalam [mala1464] language
languoids/tree/drav1251/sout3133/sout3138/tami1291/tami1292/tami1293/tami1294/tami1297/tami1298/mala1541/mala1464/md.ini

1 matches
```


### Reference search

The same can be done for reference data: To create a Whoosh index with all reference data, run
```shell script
glottolog searchindex
```

Now you can query the index:
```shell script
$ glottolog refsearch "author:Haspelmath AND title:Atlas"
...
(13 matches)
```
