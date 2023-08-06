# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python-readability'}

packages = \
['r2k',
 'r2k.cli',
 'r2k.cli.config',
 'r2k.cli.feed',
 'r2k.cli.kindle',
 'r2k.ebook',
 'r2k.gmail',
 'readability',
 'readability.compat']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.15.8,<0.16.0',
 'beautifulsoup4>=4.9.0,<5.0.0',
 'chardet>=3.0.4,<4.0.0',
 'click>=7.1.1,<8.0.0',
 'cssselect>=1.1.0,<2.0.0',
 'feedparser>=5.2.1,<6.0.0',
 'lxml>=4.5.2,<5.0.0',
 'orjson>=2.6.6,<3.0.0',
 'pick>=0.6.7,<0.7.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.24.0,<3.0.0']

extras_require = \
{'docker': ['docker>=4.2.0,<5.0.0']}

entry_points = \
{'console_scripts': ['r2k = r2k.cli:main']}

setup_kwargs = {
    'name': 'r2k',
    'version': '0.5.15',
    'description': 'A tool that lets you periodically send articles received from an RSS feed to your Kindle',
    'long_description': '# R2K (RSS to Kindle)\n\n`r2k` is a tool that lets you to track your favorite RSS/Atom feeds, and send cleaned-up (i.e. only text\nand images) articles received from them directly to your Kindle.\n\n[Installation](#installation)\n\n[Cleaning up the articles](#cleaning-up-the-articles)\n\n[Usage](#usage)\n\n\n## Installation\nThe best way to get up and running with `r2k` us to use pipx. Simply run:\n```bash\npipx install r2k\n```\n\nIf you\'re not using `pipx` (you should!), `pip install r2k` will also do.\n\nIf you want to add `r2k` to your Poetry project, run `poetry add r2k`.\n\n## Cleaning up the articles\n\nThere are currently 3 ways to clean up articles:\n1. The default is using the `readability` Python implementation. It doesn\'t require any extra steps or \ninstallations, and thus is the easiest to use. It is, however, a bit less precise than the other 2 methods. \n1. Using the [PushToKindle](http://pushtokindle.com/) service. The service works by attaching an email \naddress that forwards cleaned up versions of URLs to your Kindle. It\'s free for a certain amount of articles,\nbut you need to become their supporter afterward.\n1. Using a dockerized version of the [Mercury-Parser](https://github.com/postlight/mercury-parser). \nThis method requires Docker, but is marginally better than the `readability` approach.\n \n## Usage\n\n### Preparations\n\n#### If you\'re using PushToKindle (PTK)\n\nThe free version of PTK only allows for 25 articles to be sent using their service. After this,\nyou\'ll have to become their "sustainer" (for as low as 1$/month) on Patreon \n[here](https://www.patreon.com/bePatron?c=1946606).\n\nBefore using `r2k` with PTK you need to:\n\n1. Know your kindle email address (find it [here](https://www.amazon.com/mycd), under \n"Preferences" -> "Personal Document Settings").\n\n2. Add `kindle@fivefilters.org` to the list of approved email senders (in the same place in \nAmazon\'s settings).\n\n### Set up your configuration file\n\nMost of what `r2k` does involves the configuration file, in which the feeds you\'re subscribed to\nare kept, as well as some other data.\n\nAfter installation, run:\n\n```bash\nr2k config init [-p CONFIG_PATH] \n```\n\nThe default location for the config YAML file is in `~/.r2k/config.yml`.\n\nDuring the init you\'ll be asked several questions (like your kindle email address).\n\nTo see your configuration run:\n\n```bash\nr2k config show [-p CONFIG_PATH]\n```\n\n#### Adding your GMail credentials\n\nCurrently `r2k` relies on the fact that you have a GMail address, and it requires a \n[Google App Password](https://support.google.com/accounts/answer/185833?hl=en&authuser=1).\nThese are useful in cases where you don\'t want to go through 2FA authentication. Go\n[here](https://myaccount.google.com/u/1/apppasswords) to generate an `r2k` App Password, and \nadd it to the configuration.\n\n### Add some RSS subscriptions\n\n#### Using an OPML file\n\nThe [OPML](https://en.wikipedia.org/wiki/OPML) format is widely used in the RSS/Atom world \n(as well as in podcasting and other areas) to represent a collection of feeds. You can export your \nexisting subscriptions from most feed readers into an OPML file.\n\nTo load all of your subscriptions in one move run:\n\n```bash\nr2k feed import PATH_TO_OPML_FILE\n```\n\n#### Manually adding feeds\n\nIf you don\'t have an OPML export, or just want to add a single feed you can run:\n\n```bash\nr2k feed add -t FEED_TITLE -u FEED_URL\n```\n\nIf the `FEED_URL` is a proper RSS feed (i.e. an actual XML feed URL), it will be added as is.\nIf the `FEED_URL` is a regular URL, `r2k` will attempt to find the RSS feed by analyzing the page\nsource. In the case of multiple candidates (e.g. WordPress content feed and comment feed), you will\nbe presented with a list of choices.\n\n### Send updates to your Kindle\n\nRight now the "periodical" part of `r2k` is not yet operational. In order to send updates to your\nKindle you\'ll have to run:\n\n```bash\nr2k kindle send [-f FEED_TITLE]\n```\n\nIf you don\'t pass the `-f/--feed-title` option, updates will be sent for all of your subscriptions.\n\nThe first time that `kindle send` is run for any feed, you will be presented with a list of all the \navailable articles in the feed (note that RSS feeds usually only keep a subset of the most recent\nentries), and will be asked to choose the last one you\'ve already read. This is to avoiding sending\nyou any article you\'ve already consumed.\n ',
    'author': 'Pavel Brodsky',
    'author_email': 'mcouthon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcouthon/r2k',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
