# 📦 pgdoc-datatype-parser

[![PyPI][pypi-version-image]][pypi-link]
[![Tests][tests-image]][tests-link]
[![Coverage][coverage-image]][coverage-link]
[![PostgreSQL versions][pg-versions-image]][pg-datatypes-link]

Provides PostgreSQL documentation [datatypes table][pg-datatypes-link] as a dictionary specifying a version. Supports all versions next to `6.3`.

<p align="center">
  <img width="576" height="576" src="https://raw.githubusercontent.com/mondeja/pgdoc-datatype-parser/master/pgdoc-datatypes-parsed.png">
</p>


## Quickstart

```
pip install pgdoc-datatype-parser
```

You can retrieve all PostgreSQL datatypes for the latest version using:

```python
>>> from pprint import pprint
>>> from pgdoc_datatype_parser import pgdoc_datatypes
>>>
>>> pprint(pgdoc_datatypes())
{'bigint': {'aliases': 'int8', 'description': 'Signed eight-byte integer'},
 'bigserial': {'aliases': 'serial8',
               'description': 'Autoincrementing eight-byte integer'},
 'bit [ (n) ]': {'aliases': None, 'description': 'Fixed-length bit string'},
 'bit varying [ (n) ]': {'aliases': 'varbit [ (n) ]',
                         'description': 'Variable-length bit string'},
 'boolean': {'aliases': 'bool', 'description': 'Logical boolean (true/false)'},
 'box': {'aliases': None, 'description': 'Rectangular box on a plane'},
 'bytea': {'aliases': None, 'description': 'Binary data (byte array)'},
 'character [ (n) ]': {'aliases': 'char [ (n) ]',
                       'description': 'Fixed-length character string'},
 'character varying [ (n) ]': {'aliases': 'varchar [ (n) ]',
                               'description': 'Variable-length character '
                                              'string'},
 'cidr': {'aliases': None, 'description': 'Ipv4 or ipv6 network address'},
 'circle': {'aliases': None, 'description': 'Circle on a plane'},
 'date': {'aliases': None, 'description': 'Calendar date (year, month, day)'},
 'double precision': {'aliases': 'float8',
                      'description': 'Double precision floating-point number '
                                     '(8 bytes)'},
 'inet': {'aliases': None, 'description': 'Ipv4 or ipv6 host address'},
 'integer': {'aliases': ['int', ' int4'],
             'description': 'Signed four-byte integer'},
 'interval [ fields ] [ (p) ]': {'aliases': None, 'description': 'Time span'},
 'json': {'aliases': None, 'description': 'Textual json data'},
 'jsonb': {'aliases': None, 'description': 'Binary json data, decomposed'},
 'line': {'aliases': None, 'description': 'Infinite line on a plane'},
 'lseg': {'aliases': None, 'description': 'Line segment on a plane'},
 'macaddr': {'aliases': None,
             'description': 'Mac (media access control) address'},
 'macaddr8': {'aliases': None,
              'description': 'Mac (media access control) address (eui-64 '
                             'format)'},
 'money': {'aliases': None, 'description': 'Currency amount'},
 'numeric [ (p, s) ]': {'aliases': 'decimal [ (p, s) ]',
                        'description': 'Exact numeric of selectable precision'},
 'path': {'aliases': None, 'description': 'Geometric path on a plane'},
 'pg_lsn': {'aliases': None, 'description': 'Postgresql log sequence number'},
 'pg_snapshot': {'aliases': None,
                 'description': 'User-level transaction id snapshot'},
 'point': {'aliases': None, 'description': 'Geometric point on a plane'},
 'polygon': {'aliases': None,
             'description': 'Closed geometric path on a plane'},
 'real': {'aliases': 'float4',
          'description': 'Single precision floating-point number (4 bytes)'},
 'serial': {'aliases': 'serial4',
            'description': 'Autoincrementing four-byte integer'},
 'smallint': {'aliases': 'int2', 'description': 'Signed two-byte integer'},
 'smallserial': {'aliases': 'serial2',
                 'description': 'Autoincrementing two-byte integer'},
 'text': {'aliases': None, 'description': 'Variable-length character string'},
 'time [ (p) ] [ without time zone ]': {'aliases': None,
                                        'description': 'Time of day (no time '
                                                       'zone)'},
 'time [ (p) ] with time zone': {'aliases': 'timetz',
                                 'description': 'Time of day, including time '
                                                'zone'},
 'timestamp [ (p) ] [ without time zone ]': {'aliases': None,
                                             'description': 'Date and time (no '
                                                            'time zone)'},
 'timestamp [ (p) ] with time zone': {'aliases': 'timestamptz',
                                      'description': 'Date and time, including '
                                                     'time zone'},
 'tsquery': {'aliases': None, 'description': 'Text search query'},
 'tsvector': {'aliases': None, 'description': 'Text search document'},
 'txid_snapshot': {'aliases': None, 'description': 'Pg_snapshot'},
 'uuid': {'aliases': None, 'description': 'Universally unique identifier'},
 'xml': {'aliases': None, 'description': 'Xml data'}}
```

You can check what is the latest version using [latest_version](#latest_version) function:

```python
>>> from pgdoc_datatype_parser import latest_version
>>> latest_version()
'13.1b'
```

> If you want to retrieve PostgreSQL datatypes for other version, you can specify the optional parameter `version` of [pgdoc_datatypes](#pgdoc_datatypes) function.

> All versions can be listed using [versions](#versions) function.

## Documentation

<a name="pgdoc_datatypes" href="#pgdoc_datatypes">#</a> <b>pgdoc_datatypes</b>(<i>version="latest"</i>, <i>pg_releases_filepath=None</i>) ⇒ `dict`

Provides information for all PostgreSQL data types from [documentation data types table](https://www.postgresql.org/docs/current/datatype.html#DATATYPE-TABLE).

- **version** (str) Version from which PostgreSQL datatypes will be retrieved. 
- **pg_releases_filepath** (str) Path to PostgreSQL releases/commits file. By default, the file included with the package will be used.

<a name="versions" href="#versions">#</a> <b>versions</b>(<i>pg_releases_filepath=None</i>) ⇒ `list`

Returns all PostgreSQL available versions.

- **pg_releases_filepath** (str) Path to PostgreSQL releases/commits file. By default, the file included with the package will be used.

<a name="latest_version" href="#latest_version">#</a> <b>latest_version</b>(<i>pg_releases_filepath=None</i>) ⇒ `str`

Returns latest PostgreSQL available version.

- **pg_releases_filepath** (str) Path to PostgreSQL releases/commits file. By default, the file included with the package will be used.

<a name="pg_release_name_to_version" href="#pg_release_name_to_version">#</a> <b>pg_release_name_to_version</b>(<i>release_name</i>) ⇒ `str`

PostgreSQL releases are named in the form `REL<MAJOR>_<MINOR>_<RC><PATCH>`. You can use this function to convert release names into semantic version form. 

- **release_name** (str) Name of the PostgreSQL release name to convert into it's correspondent semantic version form.

[pypi-link]: https://pypi.org/project/pgdoc-datatype-parser
[pypi-version-image]: https://img.shields.io/pypi/v/pgdoc-datatype-parser
[tests-link]: https://github.com/mondeja/pgdoc-datatype-parser/actions?query=workflow%3ACI
[tests-image]: https://github.com/mondeja/pgdoc-datatype-parser/workflows/CI/badge.svg
[coverage-image]: https://img.shields.io/coveralls/github/mondeja/pgdoc-datatype-parser?logo=coveralls
[coverage-link]: https://coveralls.io/github/mondeja/pgdoc-datatype-parser
[pg-versions-image]: https://img.shields.io/static/v1?label=PostgreSQL&message=%3E=6.3&color=336791&logo=postgresql
[pg-datatypes-link]: https://www.postgresql.org/docs/current/datatype.html
