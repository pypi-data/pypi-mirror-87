# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['homepage']

package_data = \
{'': ['*'], 'homepage': ['static/*', 'templates/*']}

install_requires = \
['Flask', 'easyparse', 'gevent', 'youtube_dl']

entry_points = \
{'console_scripts': ['homepage = homepage:main']}

setup_kwargs = {
    'name': 'homepage',
    'version': '0.5.2',
    'description': 'A simple flask webapp to download the audio track from almost any internet video.',
    'long_description': '# HomePage\n\nHomePage is a trivial flask web app that pulls the audio track from almost any internet video.\nIt is intended to be deployed inside a private network for private use.\n\nHomePage relies on trustworthy `youtube_dl` to download the videos, so quite a few sites are supported. Playlists are also supported.\n\n![HomePage](homepage/static/HomePage.png)\n\n## Prerequsites\n\n- `python 3.6` or above with `pip`\n- Superuser access (for port 80)\n- `pyenv` and `poetry` (not required with PyPi)\n- Ubuntu, Debian, Mint or Arch.\n\n## Install\n\nThe basic installation is very simple.\n\n```bash\n$ python3 -m pip install --user homepage\n\n# Normal desktop\n$ homepage -i\n\n# Server without x11\n$ homepage -ic\n```\n\n> If you are using Arch, please ensure you have an up-to-date version and package list\n\nThen, you can deploy with:\n\n```bash\n$ homepage -dfp\n```\n\nAlternatively, if your system is running an older version of python or you wish to run this project inside\na virtual environment, you can do that too.\n\nFirst, go ahead and install [pyenv](https://github.com/pyenv/pyenv#basic-github-checkout). Then install [poetry](https://github.com/sdispater/poetry).\nOnce you\'ve installed those, we just to install a few more things.\n\n```bash\n$ git clone https://github.com/Sh3llcod3/HomePage.git\n$ cd HomePage/\n$ pyenv install 3.9.0\n$ pyenv local 3.9.0\n$ poetry poetry self update --preview\n$ poetry update\n$ poetry install # Add --no-dev if you don\'t want dev deps\n$ poetry shell\n$ homepage -ip\n$ homepage -df\n```\n\nAfter installing `pyenv`, the lines you add to your `~/.bashrc`/`.bash_profile` may need to be different, please see the [FAQ](#faq--troubleshooting).\n\n## Uninstall\n\nIf you installed using `pip`:\n\n```shell\npython3 -m pip uninstall -y homepage easyparse Flask youtube_dl gevent\n```\n\nand it will remove this completely from your system. You can vary this command based on what you want to keep.\n\nOtherwise, if you\'ve installed using poetry and assuming you\'re inside the current directory:\n\n```shell\n$ exit # Exit virtualenv or press Ctrl-d\n$ poetry env remove 3.9\n$ poetry cache clear --all pypi\n$ cd .. && rm -rf HomePage/\n```\n\n## Usage\n\nOnce deployed, if you\'re using this on the device which is hosting it, fire up your\nfavourite web browser and head to `http://localhost:5000/`. If you\'re on another device,\nsimply head to the IP address of the host node.\n\nIf you have Superuser access, use the `-f` switch. This will add an iptables rule forwarding port 80 to 5000.\n\n> Playlists are supported and all sites that will with ytdl will also work here.\n\n## Troubleshooting\n\n#### I\'m having problems with the env\n\nYou may have inserted the wrong lines in your `~/.bashrc` or `.bash_profile` (if using arch).\nThe initialization lines shown on the pyenv repo don\'t work\nwell with poetry. Instead, add these lines to the end of the file\nand remove any previous lines you may have added before\n(taking care to ensure you don\'t remove anything else).\n\n```bash\n# Pyenv installation\n\nif [[ -z "$VIRTUAL_ENV" ]]; then\n    export PATH="$HOME/.pyenv/bin:$PATH"\n    eval "$(pyenv init -)"\nfi\n```\n\n#### Can I change the background?\n\nTo change the background, swap out `homepage/static/bg.webp` with any image you like,\nbut keep the same name and use `WEBP` format.\n\n#### Pyenv fails to install 3.9.0\n\nYou may have forgotten to install the crucial `pyenv` dependencies.\nCheck [here](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) for their wiki page.\n\nThen retry the `pyenv` installation.\n\n#### Why does this exist?\n\nI wanted a simple no-frills web-app to pull audio tracks on private network devices,\nwithout having access to a command line version of `youtube_dl` or resorting to using external sites or apps.\n\n#### Why is it not working?\n\nYour version of `youtube_dl` may be out of date. Having a version of `youtube_dl`\nthat is even one version old can mean your tracks may fail to download. Fortunately,\nthe repo is updated frequently and you can pull in the updates very easily.\n\nIf you\'re using it from PyPi, then:\n```shell\n$ python3 -m pip install --upgrade youtube_dl gevent Flask --user\n$ youtube-dl --rm-cache-dir\n```\n\nIf you\'re using it from Poetry, then go to your cloned repo and run:\n```shell\n$ poetry update\n$ poetry shell\n```\n\n#### Does this scale to multiple users asynchronously?\n\nNo. It was never intended to scale in the first place. Neither is it secure in any way.\nTherefore, I should stress that you should __NOT__ deploy this to anywhere except your\nRFC1918 private/internal network range with caution.\n\n#### Does it have Windows support?\n\nYes. If you can get the latest executables for `lame`, `atomicparsley`, `faac`, `ffmpeg` and\nplace them inside the project\'s directory, it should work.\n\n## To-do\n\n- [ ] Add auth\n- [ ] Replace xhr with websocket\n- [ ] Save user preferences using cookies\n- [ ] Display past tracks only for that user\n- [ ] Add management card\n- [ ] Make it work on windows and generate executables\n',
    'author': 'Sh3llcod3',
    'author_email': '28938427+Sh3llcod3@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Sh3llcod3/HomePage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
