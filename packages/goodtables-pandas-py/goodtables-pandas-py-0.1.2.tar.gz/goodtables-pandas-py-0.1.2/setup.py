# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['goodtables_pandas']

package_data = \
{'': ['*']}

install_requires = \
['datapackage>=1.9.2,<2.0.0',
 'goodtables>=2.2.1,<3.0.0',
 'pandas>=1.1.3,<2.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'goodtables-pandas-py',
    'version': '0.1.2',
    'description': 'Read and validate Frictionless Data Tabular Data Packages with pandas.',
    'long_description': '# goodtables-pandas-py\n[![tests](https://github.com/ezwelty/goodtables-pandas-py/workflows/tests/badge.svg)](https://github.com/ezwelty/goodtables-pandas-py/actions?workflow=tests)\n[![coverage](https://codecov.io/gh/ezwelty/goodtables-pandas-py/branch/master/graph/badge.svg)](https://codecov.io/gh/ezwelty/goodtables-pandas-py)\n[![pypi](https://img.shields.io/pypi/v/goodtables-pandas-py.svg)](https://pypi.org/project/goodtables-pandas-py/)\n\n_Warning: Not an official [frictionlessdata](https://github.com/frictionlessdata) package_\n\nThis package reads and validates a Frictionless Data [Tabular Data Package](https://frictionlessdata.io/specs/tabular-data-package/) using [pandas](https://github.com/pandas-dev/pandas). It is about ~10x faster than the official [frictionlessdata/frictionless-py](https://github.com/frictionlessdata/frictionless-py), at the expense of higher memory usage.\n\n## Usage\n\n```bash\npip install goodtables-pandas-py\n```\n\n```python\nimport goodtables_pandas as goodtables\n\nreport = goodtables.validate(source=\'datapackage.json\')\n```\n\n## Implementation notes\n\n### Limitations\n\n- Only fields of type `string`, `number`, `integer`, `boolean`, `date`, `datetime`, `year`, and `geopoint` are currently supported. Other types can easily be supported with additional `parse_*` functions in `parse.py`.\n- Memory use could be greatly minimized by reading, parsing, and checking tables in chunks (using `pandas.read_csv(chunksize=)`), and storing only field values for unique and foreign key checks.\n\n### Uniqueness of `null`\n\nPandas chooses to treat missing values (`null`) as regular values, meaning that they are equal to themselves. How uniqueness is defined as a result is illustrated in the following examples.\n\n| unique | not unique |\n| --- | --- |\n| `(1)`, `(null)` | `(1)`, `(null)`, `(null)` |\n| `(1, 1)`, `(1, null)` | `(1, 1)`, `(1, null)`, `(1, null)` |\n\nAs the following script demonstrates, pandas considers the repeated rows `(1, null)` to be duplicates, and thus not unique.\n\n```python\nimport pandas\nimport numpy as np\n\npandas.DataFrame(dict(x=[1, 1, 1], y=[1, np.nan, np.nan])).duplicated()\n```\n\n> 0 False\n1 False\n2 True\ndtype: bool\n\nAlthough this behavior matches some SQL implementations (namely Microsoft SQL Server), others (namely PostgreSQL and SQLite) choose to treat `null` as unique. See this [dbfiddle](https://dbfiddle.uk/?rdbms=postgres_12&fiddle=8b23d68d139a715e003fe4b012e43e6a).\n\n### Field constraints\n\n#### `pattern`\n\nSupport for `pattern` is extended beyond `string` to all field types by testing physical values (e.g. string `"123"`) before they are parsed into their logical representation (e.g. integer `123`). See https://github.com/frictionlessdata/specs/issues/641.\n\n#### `maxLength`, `minLength`\n\nSupport for `maxLength` and `minLength` is extended beyond collections (`string`, `array`, and `object`) to field types using the same strategy as for `pattern`.\n\n### Key constraints\n\n#### `primaryKey`: `primary-key-constraint`\n\nFields in `primaryKey` cannot contain missing values (equivalent to `required: true`).\n\nSee https://github.com/frictionlessdata/specs/issues/593.\n\n#### `uniqueKey`: `unique-key-constraint`\n\nThe `uniqueKeys` property provides support for one or more row uniqueness\nconstraints which, unlike `primaryKey`, do support `null` values. Uniqueness is determined as described above.\n\n```json\n{\n  "uniqueKeys": [\n    ["x", "y"],\n    ["y", "z"]\n  ]\n}\n```\n\nSee https://github.com/frictionlessdata/specs/issues/593.\n\n#### `foreignKey`: `foreign-key-constraint`\n\nThe reference key of a `foreignKey` must meet the requirements of `uniqueKey`: it must be unique but can contain `null`. The local key must be present in the reference key, unless one of the fields is null.\n\n| reference | local: valid | local: invalid |\n| --- | --- | --- |\n| `(1)` | `(1)`, `(null)` | `(2)` |\n| `(1)`, `(null)` | `(1)`, `(null)` | `(2)` |\n| `(1, 1)` | `(1, 1)`, `(1, null)`, `(2, null)` | `(1, 2)`\n\n#### De-duplication of key constraints\n\nTo avoid duplicate key checks, the various key constraints are expanded as follows:\n\n- Reference foreign keys (`foreignKey.reference.fields`) are added (if not already present) to the unique keys (`uniqueKeys`) of the reference resource. The `foreignKey` check only considers whether the local key is in the reference key.\n- The primary key (`primaryKey`) is moved (if not already present) to the unique keys (`uniqueKeys`) and the fields in the key become required (`field.constraints.required: true`) if not already.\n- Single-field unique keys (`uniqueKeys`) are dropped and the fields become unique (`field.constraints.unique: true`) if not already.\n\nThe following example illustrates the transformation in terms of Table Schema descriptor.\n\n**Original**\n\n```json\n{\n  "fields": [\n    {\n      "name": "x",\n      "required": true\n    },\n    {\n      "name": "y",\n      "required": true\n    },\n    {\n      "name": "x2"\n    }\n  ],\n  "primaryKey": ["x", "y"],\n  "uniqueKeys": [\n    ["x", "y"],\n    ["x"]\n  ],\n  "foreignKeys": [\n    {\n      "fields": ["x2"],\n      "reference": {\n        "resource": "",\n        "fields": ["x"]\n      }\n    }\n  ]\n}\n```\n\n**Checked**\n\n```json\n{\n  "fields": [\n    {\n      "name": "x",\n      "required": true,\n      "unique": true\n    },\n    {\n      "name": "y",\n      "required": true\n    },\n    {\n      "name": "x2"\n    }\n  ],\n  "uniqueKeys": [\n    ["x", "y"]\n  ],\n  "foreignKeys": [\n    {\n      "fields": ["x2"],\n      "reference": {\n        "resource": "",\n        "fields": ["x"]\n      }\n    }\n  ]\n}\n```\n',
    'author': 'Ethan Welty',
    'author_email': 'ethan.welty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ezwelty/goodtables-pandas-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
