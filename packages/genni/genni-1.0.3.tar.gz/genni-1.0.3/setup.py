# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genni', 'genni.griding', 'genni.nets']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.1.4,<2.0.0',
 'plotly>=4.12.0,<5.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'ray[tune]>=1.0.0,<2.0.0',
 'seaborn>=0.11.0,<0.12.0',
 'tensorboard>=2.3.0,<3.0.0',
 'torch>=1.7.0,<2.0.0',
 'torchvision>=0.8.1,<0.9.0',
 'tqdm>=4.51.0,<5.0.0',
 'umap_learn>=0.4.6,<0.5.0']

setup_kwargs = {
    'name': 'genni',
    'version': '1.0.3',
    'description': 'GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability',
    'long_description': '# [GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability](https://drive.google.com/file/d/1mGO-rLOZ-_TXu_-8KIfSUiFEqymxs2x5/view)\n\n## Disclaimer\n\nThis is code associated with the paper ["GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability,"](https://drive.google.com/file/d/1mGO-rLOZ-_TXu_-8KIfSUiFEqymxs2x5/view) published in the [NeurIPS](https://nips.cc/) Workshop on [Differential Geometry meets Deep Learning 2020](https://sites.google.com/view/diffgeo4dl/).\n\nIf you have any questions, please feel free to reach out to us or make an issue.\n\n## Installing\n\nGenni is available from PyPI [here](https://pypi.org/project/genni/). In order\nto install simply use `pip`\n\n```sh\npip install genni\n```\n\n## Usage\n\nIn order to use the package, please set `genni.yml` in the top directory of your\nproject and add / set the variable `genni_home` pointing to where genni should keep\nall of the generated files.\n\n### Generating a run\n\nIn order to calculate the approximate equivalence classes of parameters of your\nnetwork architecture that leads to the same function you first need to create an\nexperiment. An example file of how to do this can be found in\n`scripts/experiment.py` which has some architectures predefined, but you can add\nyour own if you want to by looking at how the file is designed.\n\nGenerating an experiment can be done by calling\n\n```\npython scripts/experiment.py\n```\n\n### Getting directories and run IDs\n\nAfter generating an experiment this will populate `${GENNI_HOME}/experiment`\nwith a directory having as a name the timestamp of when it was run. An easy way\nto look at the generated experiments is use the `tree` command. Below is an\nexample output when running this after generating a couple of experiments\n\n```sh\ntree $GENNI_HOME/experiments -d -L 3\n```\n\nwith the output\n\n```sh\nexperiments\n└── Nov09_19-52-12_isak-arch\n    ├── models\n    │\xa0\xa0 └── 1604947934.637504\n    └── runs\n        └── 1604947934.637504\n```\n\nwhere `Nov09_19-52-12_isak-arch` is the identifier of the experiment and\n`1604947934.637504` is an ID of a hyperparameter setting of this experiment.\n\n## Plotting\n\nWe have prepared a notebook called `notebooks/SubspaceAnalysis.ipynb` showing\nhow to\n\n- Load your experiment together with necessary paths and experiment ids\n- Compute grids and values for plotting\n- Different ways of visualising the approximate equivalence classes in the form\n  of a\n  - Contour plot\n  - 3d iso-surface plot\n  - UMAP projected 2d plot of 3d iso-surface\n\n## Citing\n\nIf you use GENNI anywhere in your work, please cite use using\n\n```\n@article{2020,\n    title={GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability},\n    author={Lengyel, Daniel and Petangoda, Janith and Falk, Isak and Highnam, Kate and Lazarou, Michalis and Kolbeinsson, Arinbjörn and Deisenroth, Marc Peter and Jennings, Nicholas R.},\n    booktitle={NeurIPS Workshop on Differential Geometry meets Deep Learning},\n    year={2020}\n}\n```\n',
    'author': 'Arinbjörn Kolbeinsson',
    'author_email': None,
    'maintainer': 'Isak Falk',
    'maintainer_email': 'ucabitf@ucl.ac.uk',
    'url': 'https://github.com/Do-Not-Circulate/GENNI_public',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
