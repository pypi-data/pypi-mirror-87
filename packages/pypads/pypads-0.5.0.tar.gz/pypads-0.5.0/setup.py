# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypads',
 'pypads.app',
 'pypads.app.backends',
 'pypads.app.injections',
 'pypads.app.misc',
 'pypads.bindings',
 'pypads.bindings.resources',
 'pypads.bindings.resources.mapping',
 'pypads.importext',
 'pypads.importext.semver',
 'pypads.importext.wrapping',
 'pypads.injections',
 'pypads.injections.analysis',
 'pypads.injections.loggers',
 'pypads.injections.loggers.mlflow',
 'pypads.injections.setup',
 'pypads.model',
 'pypads.parallel',
 'pypads.utils']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=19.3.0,<20.0.0',
 'cloudpickle>=1.3.0,<2.0.0',
 'jsonpath-rw-ext>=1.2.2,<2.0.0',
 'jsonpath-rw>=1.4.0,<2.0.0',
 'loguru>=0.4.1,<0.5.0',
 'mlflow>=1.12.1,<2.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'pymongo==3.11.0']

setup_kwargs = {
    'name': 'pypads',
    'version': '0.5.0',
    'description': 'PyPaDS aims to to add tracking functionality to machine learning libraries.',
    'long_description': '# PyPads\nBuilding on the [MLFlow](https://github.com/mlflow/mlflow/) toolset this project aims to extend the functionality for MLFlow, increase the automation and therefore reduce the workload for the user. The production of structured results is an additional goal of the extension.\n\n[![Documentation Status](https://readthedocs.org/projects/pypads/badge/?version=latest)](https://pypads.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/pypads.svg)](https://badge.fury.io/py/pypads)  \n\n<!--- ![Build status](https://gitlab.padim.fim.uni-passau.de/RP-17-PaDReP/ontopads/badges/master/pipeline.svg) --->\n\n# Intalling\nThis tool requires those libraries to work:\n\n    Python (>= 3.6),\n    cloudpickle (>= 1.3.3),\n    mlflow (>= 1.6.0),\n    boltons (>= 19.3.0),\n    loguru (>=0.4.1)\n    \nPyPads only support python 3.6 and higher. To install pypads run this in you terminal\n\n**Using source code**\n\nFirst, you have to install **poetry** \n\n    pip install poetry\n    poetry build (in the root folder of the repository pypads/)\n\nThis would create two files under pypads/dist that can be used to install,\n\n    pip install dist/pypads-X.X.X.tar.gz\n    OR\n    pip install dist/pypads-X.X.X-py3-none-any.whl\n    \n \n**Using pip ([PyPi release](https://pypi.org/project/pypads/))**\n\nThe package can be found on PyPi in following [project](https://pypi.org/project/pypads/).\n\n    pip install pypads\n\n### Tests\nThe unit tests can be found under \'test/\' and can be executed using\n\n    poetry run pytest test/\n\n# Documentation\n\nFor more information, look into the [official documentation of PyPads](https://pypads.readthedocs.io/en/latest/).\n\n# Getting Started\n         \n### Usage example\npypads is easy to use. Just define what is needed to be tracked in the config and call PyPads.\n\nA simple example looks like the following,\n```python\nfrom pypads.app.base import PyPads\n# define the configuration, in this case we want to track the parameters, \n# outputs and the inputs of each called function included in the hooks (pypads_fit, pypads_predict)\nhook_mappings = {\n    "parameters": {"on": ["pypads_fit"]},\n    "output": {"on": ["pypads_fit", "pypads_predict"]},\n    "input": {"on": ["pypads_fit"]}\n}\n# A simple initialization of the class will activate the tracking\nPyPads(hooks=hook_mappings)\n\n# An example\nfrom sklearn import datasets, metrics\nfrom sklearn.tree import DecisionTreeClassifier\n\n# load the iris datasets\ndataset = datasets.load_iris()\n\n# fit a model to the data\nmodel = DecisionTreeClassifier()\nmodel.fit(dataset.data, dataset.target) # pypads will track the parameters, output, and input of the model fit function.\n# get the predictions\npredicted = model.predict(dataset.data) # pypads will track only the output of the model predict function.\n```\n        \n        \nThe used hooks for each event are defined in the mapping file where each hook represents the functions to listen to.\nUsers can use regex for goruping functions and even provide paths to hook functions.\nIn the [sklearn mapping](pypads/bindings/resources/mapping/sklearn_0_19_1.yml) YAML file, an example entry would be:\n```yaml\nfragments:\n  default_model:\n    !!python/pPath __init__:\n      hooks: "pypads_init"\n    !!python/rSeg (fit|.fit_predict|fit_transform)$:\n      hooks: "pypads_fit"\n    !!python/rSeg (fit_predict|predict|score)$:\n      hooks: "pypads_predict"\n    !!python/rSeg (fit_transform|transform)$:\n      hooks: "pypads_transform"\n\nmappings:\n  !!python/pPath sklearn:\n    !!python/pPath base.BaseEstimator:\n      ;default_model: ~\n```\nFor instance, "pypads_fit" is an event listener on any fit, fit_predict and fit_transform call made by the tracked model class which is in this case **BaseEstimator** that most estimators inherits from.\n\nUsing no custom yaml types and no fragments the mapping file would be equal to following definition:\n```yaml\nmappings:\n  :sklearn:\n    :base.BaseEstimator:\n        :__init__:\n          hooks: "pypads_init"\n        :{re:(fit|.fit_predict|fit_transform)$}:\n          hooks: "pypads_fit"\n        :{re:(fit_predict|predict|score)$}:\n          hooks: "pypads_predict"\n        :{re:(fit_transform|transform)$}:\n          hooks: "pypads_transform"\n```\n\n# Acknowledgement\nThis work has been partially funded by the **Bavarian Ministry of Economic Affairs, Regional Development and Energy** by means of the funding programm **"Internetkompetenzzentrum Ostbayern"** as well as by the **German Federal Ministry of Education and Research** in the project **"Provenance Analytics"** with grant agreement number *03PSIPT5C*.\n',
    'author': 'Thomas Weißgerber',
    'author_email': 'thomas.weissgerber@uni-passau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.padre-lab.eu/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
