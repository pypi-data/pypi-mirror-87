# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensoundscape', 'opensoundscape.torch']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'ipykernel>=5.2.0,<6.0.0',
 'jupyterlab>=2.1.4,<3.0.0',
 'librosa>=0.7.0,<0.8.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numba==0.48.0',
 'pandas>=1.0.3,<2.0.0',
 'ray>=0.8.5,<0.9.0',
 'schema>=0.7.2,<0.8.0',
 'scikit-image>=0.17.2,<0.18.0',
 'torch==1.5.0',
 'torchvision==0.6.0']

entry_points = \
{'console_scripts': ['build_docs = opensoundscape.console:build_docs',
                     'opensoundscape = opensoundscape.console:entrypoint']}

setup_kwargs = {
    'name': 'opensoundscape',
    'version': '0.4.6',
    'description': 'Open source, scalable acoustic classification for ecology and conservation',
    'long_description': '[![CI Status](https://github.com/kitzeslab/opensoundscape/workflows/CI/badge.svg)](https://github.com/kitzeslab/opensoundscape/actions?query=workflow%3ACI)\n[![Documentation Status](https://readthedocs.org/projects/opensoundscape/badge/?version=latest)](http://opensoundscape.org/en/latest/?badge=latest)\n\n# OpenSoundscape\n\nOpenSoundscape is a utility library for analyzing bioacoustic data.\nIt consists of command line scripts for tasks such as preprocessing audio data,\ntraining machine learning models to classify vocalizations, estimating the\nspatial location of sounds, identifying which species\' sounds are present in\nacoustic data, and more.\n\nThese utilities can be strung together to create data analysis pipelines.\nOpenSoundscape is designed to be run on any scale of computer:\nlaptop, desktop, or computing cluster.\n\nOpenSoundscape is currently in active development. If you find a bug, please submit an issue. If you have another question about OpenSoundscape, please email Sam Lapp (`sam.lapp` at `pitt.edu`) or Tessa Rhinehart (`tessa.rhinehart` at `pitt.edu`).\n\nFor examples of some of the utilities offered, please see the "Tutorials" section of the [documentation](https://opensoundscape.org). Included are instructions on how to download and use a pretrained machine learning model from our publicly available set of models. We plan to add additional tutorials soon.\n\n# Installation\n\nOpenSoundscape can be installed either via pip (for users) or poetry (for\ndevelopers contributing to the code). Either way, Python 3.7 or higher is required.\n\n## Installation via pip (most users)\n\n### Just give me the pip command!\n\nAlready familiar with installing python packages via pip? The pip command to install OpenSoundscape is `pip install opensoundscape==0.4.6`.\n\n### Detailed instructions\n\nPython 3.7 is required to run OpenSoundscape. Download it from [this website](https://www.python.org/downloads/).\n\nWe recommend installing OpenSoundscape in a virtual environment to prevent dependency conflicts. Below are instructions for installation with Python\'s included virtual environment manager, `venv`, but feel free to use another virtual environment manager (e.g. `conda`, `virtualenvwrapper`) if desired.\n\nRun the following commands in your bash terminal:\n* Check that you have installed Python 3.7.\\_: `python3 --version`\n* Change directories to where you wish to store the environment: `cd [path for environments folder]`\n    * Tip:  You can use this folder to store virtual environments for other projects as well, so put it somewhere that makes sense for you, e.g. in your home directory.\n* Make a directory for virtual environments and `cd` into it: `mkdir .venv && cd .venv`\n* Create an environment called `opensoundscape` in the directory: `python3 -m venv opensoundscape`\n* **For Windows computers:** activate/use the environment: `opensoundscape\\Scripts\\activate.bat`\n* **For Mac computers:** activate/use the environment `source opensoundscape/bin/activate`\n* Install OpenSoundscape in the environment: `pip install opensoundscape==0.4.6`\n* Once you are done with OpenSoundscape, deactivate the environment: `deactivate`\n* To use the environment again, you will have to refer to absolute path of the virtual environments folder. For instance, if I were on a Mac and created `.venv` inside a directory `/Users/MyFiles/Code` I would activate the virtual environment using: `source /Users/MyFiles/Code/.venv/opensoundscape/bin/activate`\n\nFor some of our functions, you will need a version of `ffmpeg >= 0.4.1`. On Mac machines, `ffmpeg` can be installed via `brew`.\n\n## Installation via poetry (contributors and advanced users)\nPoetry installation allows direct use of the most recent version of the code.\nThis workflow allows advanced users to use the newest features in OpenSoundscape,\nand allows developers/contributors to build and test their contributions.\n\nTo install via poetry, do the following:\n* Download [poetry](https://poetry.eustace.io/docs/#installation)\n* Download\n  [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html)\n* Link `poetry` and `virtualenvwrapper`:\n  - Figure out where the virtualenvwrapper.sh file is: `which virtualenvwrapper.sh`\n  - Add the following to your `~/.bashrc` and source it.\n    ```\n    # virtualenvwrapper + poetry\n    export PATH=~/.local/bin:$PATH\n    export WORKON_HOME=~/Library/Caches/pypoetry/virtualenvs\n    source [insert path to virtualenvwrapper.sh, e.g. ~/.local/bin/virtualenvwrapper_lazy.sh]\n    ```\n* **Users**: clone this github repository to your machine:\n`git clone https://github.com/kitzeslab/opensoundscape.git`\n* **Contributors**: fork this github repository and clone the fork to your machine\n* Ensure you are in the top-level directory of the clone\n* Switch to the development branch of OpenSoundscape: `git checkout develop`\n* Build the virtual environment for opensoundscape: `poetry install`\n  - If poetry install outputs the following error, make sure to download Python 3.7:\n    ```\n    Installing build dependencies: started\n    Installing build dependencies: finished with status \'done\'\n    opensoundscape requires Python \'>=3.7,<4.0\' but the running Python is 3.6.10\n    ```\n    If you are using `conda`, install Python 3.7 using `conda install python==3.7`\n  - If you are on a Mac and poetry install fails to install `numba`, contact one\n    of the developers for help troubleshooting your issues.\n* Activate the virtual environment with the name provided at install e.g.: `workon opensoundscape-dxMTH98s-py3.7` or `poetry shell`\n* Check that OpenSoundscape runs: `opensoundscape -h`\n* Run tests (from the top-level directory): `poetry run pytest`\n* Go back to your system\'s Python when you are done: `deactivate`\n\n### Jupyter\nTo use OpenSoundscape within JupyterLab, you will have to make an `ipykernel`\nfor the OpenSoundscape virtual environment.\n\n- Activate poetry virtual environment, e.g.: `workon opensoundscape-dxMTH98s-py3.7`\n    - Use `poetry env list` if you\'re not sure what the name of the environment is\n- Create ipython kernel: `python -m ipykernel install --user --name=[name of poetry environment] --display-name=OpenSoundscape`\n- Now when you make a new document on JupyterLab, you should see a Python kernel available called OpenSoundscape.\n- Contributors: if you include Jupyter\'s `autoreload`, any changes you make to the source code\n  installed via poetry will be reflected whenever you run the `%autoreload` line magic in a cell:\n    ```\n    %load_ext autoreload\n    %autoreload\n    ```\n\n### Contributing to code\n\nMake contributions by editing the code in your fork. Create branches\nfor features using `git checkout -b feature_branch_name` and push these\nchanges to remote using `git push -u origin feature_branch_name`. To merge a\nfeature branch into the development branch, use the GitHub\nweb interface to create a merge request.\n\nWhen contributions in your fork are complete, open a pull request using the\nGitHub web interface. Before opening a PR, do the following to\nensure the code is consistent with the rest of the package:\n* Run tests: `poetry run pytest`\n* Format the code with `black` style (from the top level of the repo): `poetry run black .`\n  * To automatically handle this, `poetry run pre-commit install`\n* Additional libraries to be installed should be installed with `poetry add`, but\n  in most cases contributors should not add libraries.\n\n### Contributing to documentation\n\nBuild the documentation using either poetry or sphinx-build\n- With poetry: `poetry run build_docs`\n- With sphinx-build: `sphinx-build doc doc/_build`\n',
    'author': 'Justin Kitzes',
    'author_email': 'justin.kitzes@pitt.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jkitzes/opensoundscape',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
