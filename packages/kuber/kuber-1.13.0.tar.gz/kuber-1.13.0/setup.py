# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kuber',
 'kuber.interface',
 'kuber.latest',
 'kuber.management',
 'kuber.pre',
 'kuber.v1_15',
 'kuber.v1_16',
 'kuber.v1_17',
 'kuber.v1_18',
 'kuber.v1_19',
 'kuber.v1_20',
 'kuber.v1_21']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'kubernetes>=12.0.1,<13.0.0',
 'requests>=2.25.0,<3.0.0',
 'semver>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'kuber',
    'version': '1.13.0',
    'description': 'Accelerated Kubernetes configuration and package management with Python.',
    'long_description': '[![PyPI version](https://img.shields.io/pypi/v/kuber.svg)](https://pypi.python.org/pypi/kuber)\n[![Documentation Status](https://readthedocs.org/projects/kuber/badge/?version=latest)](https://kuber.readthedocs.io/en/latest/?badge=latest)\n[![build status](https://gitlab.com/swernst/kuber/badges/master/build.svg)](https://gitlab.com/swernst/kuber/commits/master)\n[![coverage report](https://gitlab.com/swernst/kuber/badges/master/coverage.svg)](https://gitlab.com/swernst/kuber/commits/master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Code style: flake8](https://img.shields.io/badge/code%20style-flake8-white)](https://gitlab.com/pycqa/flake8)\n[![Code style: mypy](https://img.shields.io/badge/code%20style-mypy-white)](http://mypy-lang.org/)\n\n# Kuber\n\nkuber is Python library for the management of Kubernetes resources. It\'s\nideal for for collectively managing groups of resources throughout their\nlifecycle. Resource definitions can be created and managed entirely in Python\ncode (the pure-Python approach), but kuber is most effective when used in a\nhybrid fashion that combines configuration files and Python code.\nkuber also integrates and maintains compatibility with the lower-level official\n[Kubernetes Python client](https://github.com/kubernetes-client/python),\nwhile abstracting basic CRUD operations into higher level constructs\nmore inline with the behaviors of tools like *kubectl* and *helm*.\n\n## Key Functionality\n\nHere are some key things that kuber does well:\n\n- A flexible workflow for managing Kubernetes resource configuration in Python\n  code.\n- The ability to load resources directly from YAML or JSON configuration files,\n  modify them in code and then use them or save them back to YAML/JSON files.\n- Resource bundling for managing groups of resource configurations collectively.\n- CRUD operations exposed directly on the resource objects to reduce the\n  overhead in managing low-level clients.\n- Convenience functions that simplify common operations, e.g. managing\n  containers within pods from the root resource.\n- Very thorough type-hinting and object structure to support creating accurate\n  resource configurations and catch errors before runtime.\n- All resources and sub-resources support used in `with` blocks as context\n  managers to simplify making multiple changes to a sub-resource.\n- Simultaneous support for multiple Kubernetes API versions. Manage multiple\n  Kubernetes API versions (e.g. while promoting new versions from development\n  to production) without having to pin and switch Python environments.\n\n## Installation\n\nkuber available for installation with [pip](https://pypi.org/project/pip/):\n\n```bash\n$ pip install kuber\n```\n \n## Quickstart\n\nkuber can be used to manage individual resources or a group of resources\ncollectively. kuber is also very flexible about how resources are created - \neither directly from Python or by loading and parsing YAML/JSON configuration\nfiles. The first example shows the multi-resource management path:\n\n```python\nimport kuber\nfrom kuber.latest import apps_v1\n\n# Create a bundle and load all resource definitions from the\n# `app_configs` directory as well as the `app-secret.yaml`\n# configuration file from the local `secrets` directory.\nresource_bundle = (\n    kuber.create_bundle()\n    .add_directory("app_configs")\n    .add_file("secrets/app-secret.yaml")\n)\n\n# Modify the metadata labels on all resources in the bundle.\nfor resource in resource_bundle.resources:\n    resource.metadata.labels.update(environment="production")\n\n# Update the replica count of the loaded deployment named\n# "my-app" to the desired initial count.\nd: apps_v1.Deployment = resource_bundle.get(\n    name="my-app",\n    kind="Deployment"\n)\nd.spec.replicas = 20\n\n# Load the current `kubeconfig` cluster configuration into\n# kuber for interaction with the cluster.\nkuber.load_access_config()\n\n# Turn this bundle script into a file that can be called from\n# the command line to carry out CRUD operations on all the\n# resources contained within it collectively. For example,\n# to create the resources in this bundle, call this script\n# file with a create argument.\nresource_bundle.cli()\n```\n\nOr managing resources individually:\n\n```python\nfrom kuber.latest import batch_v1\n\njob = batch_v1.Job()\n\n# Populate metadata using context manager syntax for brevity.\nwith job.metadata as md:\n    md.name = "my-job"\n    md.namespace = "jobs"\n    md.labels.update(\n        component="backend-tasks",\n        environment="production"\n    )\n\n# Add a container to the job spec.\njob.spec.append_container(\n    name="main",\n    image="my-registry.com/projects/my-job:1.0.1",\n    image_pull_policy="Always",\n    env=[batch_v1.EnvVar("ENVIRONMENT", "production")]\n)\n\n# Print the resulting YAML configuration for display. This\n# could also be saved somewhere to use later as the\n# configuration file to deploy to the cluster in cases\n# like a multi-stage CI pipeline.\nprint(job.to_yaml())\n```\n\nCheck out the [kuber documentation](https://kuber.readthedocs.io/en/latest/)\nfor more details and examples.\n',
    'author': 'Scott Ernst',
    'author_email': 'swernst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sernst/kuber',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
