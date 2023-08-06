# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigquery_erd']

package_data = \
{'': ['*']}

install_requires = \
['ERAlchemy>=1.2.10,<2.0.0', 'google-cloud-bigquery>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'bigquery-erd',
    'version': '0.1.0',
    'description': 'Building Entity Relationship Diagrams for Google BigQuery.',
    'long_description': '# bigquery-erd\n\nEntity Relationship Diagram (ERD) Generator for Google BigQuery, based upon [eralchemy](https://github.com/Alexis-benoist/eralchemy).\n\n## Examples\n\nERD for a NewsMeme database schema (taken from the original project).\n\n![NewsMeme Example](./examples/newsmeme.png)\n\n## Installation\n\n```sh\npip install bigquery-erd\n```\n\n`eralchemy` requires [GraphViz](http://www.graphviz.org/download) to generate the graphs and Python. Both are available for Windows, Mac and Linux.\n\n## Usage\n\n### Usage from Python\n\nFind an example notebook [here](./notebooks/example.py).\n\n## But Wait, BigQuey is not a Relation Database?\n\nThat\'s right. You cannot enforce primary or foreign key constraints in BigQuery. However, that doesn\'t mean that you should not be able to have logical dependencies between tables.\n\n### Defining Relations through Column Descriptions\n\nWe use the column description field in BigQuery to define relations between columns in a format that we can later parse programmatically.\n\nLet\'s assume we have a table `a` with a column `id` and another table `a` with a column `a_id` that serves as a foreign key relation to `a.id`.\nWe then add the following description to `b.a_id`:\n\n```\n-> b.id\n```\n\n### Defining Relations to Datasets Explicitly\n\nPer default, we assume that the related tables are located inside the same dataset. However, you can also define the datasets explicitly. This is especially useful if the two related tables are not located within the same dataset.\n\nLet\'s assume that table `a` is located in dataset `d1` and table `b` is located in `d2`.\nThe description in `b.a_id` would then be:\n\n```\n-> d1.a.id\n```\n\n### Defining Cardinality Explicitly\n\nCardinality defines the relationship between two tables. This package understands four different cardinalities:\n\n- `*`, meaning "0..N"\n- `?`, meaning "{0,1}"\n- `+`, meaning "1..N"\n- `1`, meaning "1"\n\nPer default, we assume a cardinality of `*:1`. You can also define the relation\'s cardinality explicitly.\n\nLet\'s assume that every record in `a` has at least 1 related record in `b`.\nthe description in `b.a_id` would be:\n\n```\n-> +:1 a.id\n```\n\n### Example\n\nYou can find a example Google BigQuery project for the NewsMeme schema with annotated descriptions [here](https://console.cloud.google.com/bigquery?project=test-project-jjagusch&p=test-project-jjagusch&d=newsmeme&page=dataset).\n\n### Defining Custom Description RegEx\n\nThe default RegEx for relations in column descriptions is `->\\s([?*+1 ]:[?*+1 ]\\s)?(.*\\.)?(.*)\\.(.*)$`. You can define a custom RegEx by setting the `GBQ_RELATION_PATTERN` environment variable.\nThe RegEx should match four capture groups, where:\n\n- The first group is the cardinality (which is optional)\n- The second group is the dataset id (which is optional)\n- The third group is the table id\n- The fourth group is the column\n',
    'author': 'Jan-Benedikt Jagusch',
    'author_email': 'jan.jagusch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
