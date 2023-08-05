# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cas_manifest']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9.201,<2.0.0', 'hashfs>=0.7.2,<0.8.0', 'pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'cas-manifest',
    'version': '0.3.3',
    'description': 'cas-manifest allows developers to store artifacts in a _content-addressable_ store using a self-describing _manifest_',
    'long_description': "# CAS-Manifest\n\nThis package facilitates storing artifacts in Content Addressable Storage via the `hashfs` library. In a CAS regime, the hash of the artifact's contents is used as the key.\n\nIt further requires that artifacts are `pydantic` models - this allows for stable serialization of the artifacts, and for data to be self-describing.\n\nConsider an example usage profile: let's say that your application works with datasets, some of which are serialized as csv files, others of which are serialized as tsv files. Some have header rows, and some do not. Rather than write data-loading code that tries to infer the correct way to deserialize a dataset file, `cas-manifest` serializes all relevant\nattributes of the dataset along with the data file itself. Your code might look like this:\n```python\nfrom hashfs import HashFS\nfrom cas_manifest.registry import Registry\nfrom my_classes import CSVDataset, TSVDataset\n\nfs = HashFS('/path/to/data')\ndataset_hash = '5fef4a'\nregistry = Registry(fs, [CSVDataset, TSVDataset])\nobj = registry.load(dataset_hash)\n# obj is an instance of either CSVDataset or TSVDataset\n```\n\n## Why CAS?\n\nIn short, CAS enforces immutability. When using CAS, a key's contents can never be changed. The following comes naturally:\n* No more `data_final__2_new` files - all objects are uniquely specified\n* No cache invalidation - cache objects freely, knowing that their contents will never change upstream\n* No more provenance questions - models can be robustly linked to the datasets used to train them\n\n## Why manifests?\n\nIn a CAS regime, keys are deliberately opaque. By using manifests, artifacts can be _self-descriptive_. It can include instructions for deserialization, links to other artifacts, and any other metadata you can think up. In combination with CAS, you can ensure that your metadata and underlying data never go out of sync, since your metadata will refer to an immutable reference to underlying data.\n",
    'author': 'Dan Frank',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danielhfrank/cas-manifest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
