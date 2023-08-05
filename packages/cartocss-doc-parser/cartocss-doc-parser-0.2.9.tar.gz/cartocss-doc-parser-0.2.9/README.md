# cartocss-doc-parser

[![PyPI][pypi-version-image]][pypi-link]
[![Python versions][pypi-pyversions-image]][pypi-link]
[![Tests][tests-image]][tests-link]
[![Coverage Status][coverage-image]][coverage-link]


[CartoCSS documentation][cartocss-doc-link] Python parser.

<p align="center">
  <img width="512" height="512" src="https://raw.githubusercontent.com/mondeja/cartocss-doc-parser/master/cartocss-doc-parsed.png">
</p>

## Install

```bash
pip install cartocss-doc-parser
```

## Quickstart

The main function [cartocss_doc](#cartocss_doc) returns a dictionary with
almost every section of the documentation. All the properties are wrapped in
generators.

```python
>>> from pprint import pprint
>>> from cartocss_doc_parser import cartocss_doc
>>>
>>> doc = cartocss_doc()
>>> pprint(doc)
{'building': <generator object ...>,
 'common_elements': <generator object ...>,
 'line': <generator object ...>,
 'line_pattern': <generator object ...>,
 'map_background_and_string_elements': <generator object ...>,
 'markers': <generator object ...>,
 'other_parameters': <generator object ...>,
 'point': <generator object ...>,
 'polygon': <generator object ...>,
 'polygon_pattern': <generator object ...>,
 'raster': <generator object ...>,
 'shield': <generator object ...>,
 'symbolizers': <generator object ...>,
 'text': <generator object ...>,
 'torque_properties': <generator object ...>,
 'values': <generator object ...>}
```

All properties contains the attributes

- **`default`** Default value.
- **`description`** Description.
- **`id`** Identificator.
- **`link`** Link to the property on documentation.
- **`name`** Name of the property.
- **`sample`** Example of use.
- **`type`** Value data type. For a complete list see
 [cartocss_data_types](#cartocss_data_types).

and if the data type is `keyword` contains an additional attribute

- **`variants`** Possible values for the property.

```python
>>> pprint(list(doc["polygon"]))
[{'default': 'gray',
  'description': 'The fill color assigned to a polygon.',
  'id': 'polygon-fill-color',
  'link': 'https://carto.com/developers/styling/cartocss/#polygon-fill-color',
  'name': 'polygon-fill',
  'sample': 'polygon-fill: rgba(128, 128, 128, 1);',
  'type': 'color'},
 {'default': '1',
  'description': 'The opacity of the polygon.',
  'id': 'polygon-opacity-float',
  'link': 'https://carto.com/developers/styling/cartocss/#polygon-opacity-float',
  'name': 'polygon-opacity',
  'sample': 'polygon-opacity: 1;',
  'type': 'float'},
 ...,
 {'default': 'power',
  'description': 'An anti-grain geometry method that represents a 2D rendering '
                 'library, specific to controlling the quality of antialiasing '
                 'and used to calculate pixel gamma (pow(x,gamma), which '
                 'produces slightly smoother line and polygon antialiasing '
                 "than the 'linear' method.",
  'id': 'polygon-gamma-method-keyword',
  'link': 'https://carto.com/developers/styling/cartocss/#polygon-gamma-method-keyword',
  'name': 'polygon-gamma-method',
  'sample': 'polygon-gamma-method: power;',
  'type': 'keyword',
  'variants': ['power', 'linear', 'none', 'threshold', 'multiply']},
 ...
]
```

All data types can be requested with [cartocss_data_types](#cartocss_data_types) function:

```python
>>> from cartocss_doc_parser import cartocss_data_types
>>> pprint(list(cartocss_data_types()))
['color',
 'float',
 'uri',
 'string',
 'boolean',
 'expression',
 'numbers',
 'number',
 'percentages',
 'percentage',
 'functions',
 'function',
 'keyword',
 'unsigned',
 'tags']
```

## Documentation

<a name="cartocss_doc" href="#cartocss_doc">#</a> <b>cartocss_doc</b>(<i>url="https://carto.com/developers/styling/cartocss/"</i>, <i>user_agent="cartocss_doc_parser vX.Y.Z"</i>) ⇒ `dict`

Provides information for almost every section of CartoCSS documentation.

- **url** (str) URL to the documentation page. Can be a local file, in which
 case any HTTP request would be performed, instead the file would be read. 
- **user_agent** (str) User agent performing the HTTP request to documentation
 page. As default is `cartocss_doc_parser (v%(version)s)`.

<a name="cartocss_data_types" href="#cartocss_data_types">#</a> <b>cartocss_data_types</b>(<i>url="https://carto.com/developers/styling/cartocss/"</i>, <i>user_agent="cartocss_doc_parser vX.Y.Z"</i>) ⇒ `gen`

Lists all available data types for properties for CartoCSS.

- **url** (str) URL to the documentation page. Can be a local file, in which
 case any HTTP request would be performed, instead the file would be read. 
- **user_agent** (str) User agent performing the HTTP request to documentation
 page. As default is `cartocss_doc_parser (v%(version)s)`.

[pypi-link]: https://pypi.org/project/cartocss-doc-parser
[pypi-version-image]: https://img.shields.io/pypi/v/cartocss-doc-parser
[pypi-pyversions-image]: https://img.shields.io/pypi/pyversions/cartocss-doc-parser
[tests-image]: https://img.shields.io/github/workflow/status/mondeja/cartocss-doc-parser/Test
[tests-link]: https://github.com/mondeja/cartocss-doc-parser/actions?query=workflow%3ATest
[coverage-image]: https://coveralls.io/repos/github/mondeja/cartocss-doc-parser/badge.svg
[coverage-link]: https://coveralls.io/github/mondeja/cartocss-doc-parser
[cartocss-doc-link]: https://carto.com/developers/styling/cartocss
