# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grid2viz',
 'grid2viz.src',
 'grid2viz.src.episodes',
 'grid2viz.src.kpi',
 'grid2viz.src.macro',
 'grid2viz.src.micro',
 'grid2viz.src.overview',
 'grid2viz.src.simulation',
 'grid2viz.src.utils',
 'tests']

package_data = \
{'': ['*'],
 'grid2viz': ['assets/*',
              'assets/screenshots/*',
              'data/agents/do-nothing-baseline/*',
              'data/agents/do-nothing-baseline/000/*',
              'data/agents/do-nothing-baseline/001/*',
              'data/agents/greedy-baseline/*',
              'data/agents/greedy-baseline/000/*',
              'data/agents/greedy-baseline/001/*',
              'data/agents_dev/do-nothing-baseline/*',
              'data/agents_dev/do-nothing-baseline/000/*',
              'data/agents_dev/do-nothing-baseline/001/*',
              'data/agents_dev/do-nothing-baseline/002/*',
              'data/agents_dev/greedy-baseline/*',
              'data/agents_dev/greedy-baseline/000/*',
              'data/agents_dev/greedy-baseline/001/*',
              'data/agents_dev/multiTopology-baseline/*',
              'data/agents_dev/multiTopology-baseline/000/*',
              'data/agents_dev/redispatching-baseline/*',
              'data/agents_dev/redispatching-baseline/000/*',
              'data/agents_multi_topo/multiTopology-baseline/*',
              'data/agents_multi_topo/multiTopology-baseline/000/*',
              'data/agents_test_env_1.2.3/do-nothing-baseline/*',
              'data/agents_test_env_1.2.3/do-nothing-baseline/test_chronic/*'],
 'tests': ['data/agents/do-nothing-baseline/*',
           'data/agents/do-nothing-baseline/000/*',
           'data/agents/greedy-baseline/*',
           'data/agents/greedy-baseline/000/*',
           'data/agents/multiTopology-baseline/*',
           'data/agents/multiTopology-baseline/000/*',
           'data/agents/redispatching-baseline/*',
           'data/agents/redispatching-baseline/000/*']}

install_requires = \
['Grid2Op>=1.3.1,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'dash-antd-components>=0.0.1-rc.2,<0.0.2',
 'dash-bootstrap-components>=0.10.7,<0.11.0',
 'dash>=1.17.0,<2.0.0',
 'dill>=0.3.3,<0.4.0',
 'imageio>=2.9.0,<3.0.0',
 'jupyter-dash>=0.3.1,<0.4.0',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy==1.19.3',
 'pandapower>=2.4.0,<3.0.0',
 'pathos>=0.2.7,<0.3.0',
 'seaborn>=0.11.0,<0.12.0']

entry_points = \
{'console_scripts': ['grid2viz = grid2viz.main:main']}

setup_kwargs = {
    'name': 'grid2viz',
    'version': '1.0.0a0',
    'description': 'Grid2Op Visualization companion app',
    'long_description': None,
    'author': 'Mario Jothy',
    'author_email': 'mario.jothy@artelys.com>, Vincent Renault <vincent.renault@artelys.com>, Antoine Marot <antoine.marot@rte-france>, Maxime Mohandi <maxime.mohandi@artelys.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
