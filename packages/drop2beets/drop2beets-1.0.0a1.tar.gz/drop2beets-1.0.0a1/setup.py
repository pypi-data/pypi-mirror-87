# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beetsplug', 'examples']

package_data = \
{'': ['*']}

install_requires = \
['inotify>=0.2.10,<0.3.0']

setup_kwargs = {
    'name': 'drop2beets',
    'version': '1.0.0a1',
    'description': 'Import singles to Beets as soon as they are dropped in a folder',
    'long_description': '# drop2beets\n\nA [Beets](http://beets.io/) plug-in that imports singles as soon as they are dropped in a folder.\n\nYou can provide a function to set meta-data\nor custom attributes depending on the sub-folder in which the file has been dropped.\nThe [examples](https://github.com/martinkirch/drop2beets/tree/master/examples)\nfolder contains some examples of `on_item` functions you may\nadapt to your needs.\n\nWe use Beets\' auto-tagger in quiet mode,\nand [inotify](https://pypi.org/project/inotify/) to detect dropped files.\n\n## Get started\n\nYou\'ll need Python3 on a Linux box, and obviously an existing Beets library.\nRun:\n\n```bash\npip install drop2beets\n```\n\nEnable and configure the plug-in by running `beet config -e` and set at least\nthe path to the "dropbox" folder.\n\n```yaml\nplugins: drop2beets\ndrop2beets:\n    dropbox_path: ~/beets-dropbox\n```\n\nWe advise you configure Beets to always move files out of the Dropbox,\nand set `quiet_fallback`:\n\n```yaml\nimport:\n    move: yes\n    copy: no\n    quiet_fallback: asis\n```\n\n`quiet_fallback` tells Beets what to do when the auto-tagger is not sure about\nthe song\'s identifiaction.\nSet it to `skip` to abort the importation in case of ambiguity,\nor `asis` to import using tags as they are in the incoming file.\nThis will avoid surprises in case of ambiguous matches,\nbecause this script invokes Beet\'s auto-tagger in quiet mode (as `beet import -q`)\nafter your custom function.\n\nThis function is `on_item`. It is written in Python,\nand lets you set some tags depending of which sub-folder the file is dropped in.\nIf you want one, define it in the configuration from this template:\n\n```yaml\ndrop2beets:\n    on_item: |\n        def on_item(item, path):\n            """\n            Parameters:\n                item: the beets Item that we\'re about to import\n                path: its sub-folders path in our dropbox ; if the items has been dropped at the root, then it\'s empty.\n            Returns:\n                A dict of custom attributes (according to path, maybe) ; return None if you don\'t want to import the file right now.\n            """\n            return {}\n```\n\nNow you\'re ready to test by calling `beet dropbox` on the command line and\ndropping a few files in the folder.\nHit Ctrl+C to close the script.\n\nFor a longer-term installation, configure a log file path\n\n```yaml\ndrop2beets:\n    log_path: ~/drop2beets/log.log\n```\n\nAnd install this as a user-lever systemd service by running `beet install_dropbox`\n(in a shell where the virtual environment is activated).\n\nNote that you\'ll have to restart the service when you update the `on_item` function.\n\n\n## Examples wanted !\n\nI\'d be happy to include your own variations of this script or the `on_item` function\nin the [examples](https://github.com/martinkirch/drop2beets/tree/master/examples) folder, \nfeel free to post them in\n[Issues](https://github.com/martinkirch/drop2beets/issues) or\n[Pull Requests](https://github.com/martinkirch/drop2beets/pulls).\n',
    'author': 'Martin Kirchgessner',
    'author_email': 'martin.kirch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/martinkirch/drop2beets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
