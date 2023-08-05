# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docs',
 'grid2viz',
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
 'docs': ['_static/*', 'views/*'],
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
    'version': '1.0.0a5',
    'description': 'Grid2Op Visualization companion app.',
    'long_description': '\n# Grid2Viz: The Grid2Op Visualization companion app\n\n<!--- #[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mjothy/grid2viz/jupyter_dash?urlpath=lab)#if launching jupyter lab directly-->\nYou can launch a demo in your web navigator by running the Grid2viz_demo notebook through Binder by clicking this button. The dataset used in this demo can be found in the [Grid2viz dataset](https://github.com/marota/Grid2viz-dataset-NeurIPS-Robustness).\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mjothy/grid2viz/master/?urlpath=git-pull?repo=https://github.com/marota/Grid2viz-dataset-NeurIPS-Robustness%26amp%3Burlpath=tree/../%26amp%3Burlpath=tree/Grid2Viz_demo.ipynb%3Fautodecode)<!--- 1rst urlpath to download the dataset from a new github - 2nd urlpath to get back to a parent root directory - 3rd urlpath to directly load the notebook -->\n**WARNING:** we recommend you to use Firefox or Chrome as a web navigator rather than Internet Explorer or Edge.\n---\n\nGrid2Viz is a web application that offers several interactive views into the results of Reinforcement Learning agents that ran on the [Grid2Op](https://github.com/rte-france/Grid2Op) platform.\n\n*   [1 Documentation](#documentation)\n*   [2 Installation](#installation)\n*   [3 Run the application](#run-grid2viz)\n*   [4 Getting Started](#getting-started)\n*   [5 Caching](#caching)\n*   [6 Interface](#interface)\n*   [7 Trouble shooting](#troubleshooting)\n\n## Documentation\ngo to: https://grid2viz.readthedocs.io/en/latest/\n\n## Installation\n### Requirements:\n*   Python >= 3.6\n\n#### (Optional, recommended) Step 1: Create a virtual environment\n```commandline\npip3 install -U virtualenv\npython3 -m virtualenv venv_grid2viz\n```\n\n#### Step 2: Install from pypi\n```commandline\nsource venv_grid2viz/bin/activate\npip install -U grid2viz\n```\n\n## Run Grid2Viz\n```\nusage: grid2viz [-h] [--agents_path AGENTS_PATH] [--env_path ENV_PATH]\n                [--port PORT] [--debug]\n\nGrid2Viz\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --agents_path AGENTS_PATH\n                        The path where the log of the Agents experiences are\n                        stored. (default to None to study the example agents\n                        provided with the package)\n  --env_path ENV_PATH   The path where the environment config is stored.\n                        (default to None to use the provided default\n                        environment)\n  --port PORT           The port to serve grid2viz on. (default to 8050)\n  --debug               Enable debug mode for developers. (default to False)\n```\n\nFor example:\n\n```commandline\nsource venv_grid2viz/bin/activate\ngrid2viz --port 8000\n```\n\n> **_WARNING_** Due to the caching operation the first run can take a while. All the agents present in the configuration files\nwill be computed and then registered in cache. Depending on your agents it could take between 5 to 15min. You can follow the progress in the console.\n\n## Getting started\n\nIn order to use this tool, you need to have serialized the RL process of grid2op. The expected file system is :\n- root_dir\n    - agent_1\n        - scenario_1\n        - scenario_2\n    - agent_2\n        - scenario_1\n        - scenario_2\n        - scenario_3\n\nEach of the scenario_* files have to contain all files given by serialisation of your RL through grid2op.\nIn order to add a new agent to the app, you will have to add the agent\'s folder to this root_dir\nFor the update process of this folder chain, see the section `Caching` (in particular, when you want to overwrite the current\nagents in root_dir with new versions with the same names)\n\nIn the config.ini of this repo:\n - `agents_dir` is the path to your agents logs data directory.\n - `env_dir` is the path to the environment configuration directory. It contains a single file :\n    - coords.csv : The csv file that lists the coordinates of nodes in the network\n\nChanging this config.ini file will require a restart of the server to update.\n\nGrid2Viz provide 2 agents with a scenario for one day and for one month available in `/grid2viz/data/agents` folder:\n\n- do-nothing-baseline\n- greedy-baseline\n\nBy default the config.ini is targeting these agents as well as the environment configuration folders.\n\n##  Caching\n\nThe cache system allows you to only compute long calculations of the app once per agent/scenario.\nThe app will create a folder `_cache` in the `base_dir` of the config.ini which will contain these long calculations serialized.\n\nIf you add a new folder in your `base_dir` (either an agent, or a scenario) you will have to restart the server so the app\nreads the folder tree again.\n\n**_WARNING_** : If you overwrite the agents while they were already cached, you will have to manually reset the cache so the app\nknows to compute everything again with the updated data. To do so, you just need to delete the `_cache` folder.\n\n## Interface\n#### Scenario Selection\nThis page display up to 15 scenarios with for each one a brief summary using the best agent\'s performances.\n\n![scenario selection](https://raw.githubusercontent.com/mjothy/grid2viz/master/grid2viz/assets/screenshots/scenario_selection.png "Scenario Selection")\n\n\n#### Scenario Overview\nOn this page are displayed the best agent\'s kpi to see his performances. It\'s also here that you can select an agent that will\nbe used as reference agent in the other pages to compare to the studied agents.\n\n![scenario overview](https://raw.githubusercontent.com/mjothy/grid2viz/master/grid2viz/assets/screenshots/scenario_overview.png "Scenario Overview")\n\n#### Agent Overview\nHere\'s displayed your reference agent\'s performances. You can select an agent to study to compare it with your reference via the\ndropdown on the page. The study agent selected will be used as study agent on the last page.\n\nIn the *"instant and cumulated reward"* graph you can point timestep that will be use in the next page to study\naction in a specific timestep area.\n\n![agent overview](https://raw.githubusercontent.com/mjothy/grid2viz/master/grid2viz/assets/screenshots/agent_overview.png "Agent Overview")\n\n\n#### Agent Study\nThe Agent Study page will display kpi of your reference agent compared to your study agent on your selected timestep area.\nYou will also see a summary of the previous page\'s kpi.\n\n![agent study](https://raw.githubusercontent.com/mjothy/grid2viz/master/grid2viz/assets/screenshots/agent_study.png "Agent Study")\n\n## Run the tests\n\nTo run the tests, execute the following command:\n\n```commandline\npython3 -m unittest discover --start-directory tests --buffer\n```\n\n## Limitations\nThe app is still missing a couple features, namely a graph for visualising the flow through time, and the last line of the last screen, which will show all informations regarding the actions and observations at the selected timestep.\n\nThe Actions KPIs and the distances as well as the topological action cluster "object changed" is in alpha feature. We will need some new features from the core API to finish these features.\n\n## Troubleshooting\n### MacOS\nSome mac users have been experimenting issues when lauching the app, raising the following message:\n\n`socket.gaierror: [Errno 8] nodename nor servname provided, or not known`\n\nThe following steps might help you to overcome the issue:\n\n1. Open your terminal\n2. Type `echo $HOST` and copy the results\n3. Open the file `/etc/hosts` and make sure you include: <br>\n `127.0.0.1 PASTE RESULTS FROM echo $HOST`\n4. Save it and close it\n5. Launch grid2viz\n\n\n',
    'author': 'Mario Jothy',
    'author_email': 'mario.jothy@artelys.com',
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
