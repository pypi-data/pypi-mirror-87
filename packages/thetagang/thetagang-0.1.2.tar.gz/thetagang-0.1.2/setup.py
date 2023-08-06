# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thetagang']

package_data = \
{'': ['*']}

install_requires = \
['click-log>=0.3.2,<0.4.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'ib_insync>=0.9.64,<0.10.0',
 'pandas>=1.1.4,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['thetagang = thetagang.entry:cli',
                     'vscode = vscode:vscode']}

setup_kwargs = {
    'name': 'thetagang',
    'version': '0.1.2',
    'description': 'ThetaGang is an IBKR bot for getting money',
    'long_description': '# Θ ThetaGang Θ\n\nThetaGang is an [IBKR](https://www.interactivebrokers.com/) trading bot for\ncollecting premium by selling options using "The Wheel" strategy. The Wheel\nis a strategy that [surfaced on\nReddit](https://www.reddit.com/r/options/comments/a36k4j/the_wheel_aka_triple_income_strategy_explained/),\nbut has been used by many in the past. This bot implements a slightly\nmodified version of The Wheel, with my own personal tweaks.\n\nI\'ve been streaming most of the work on this project [on Twitch, so follow me\nover there](https://www.twitch.tv/letsmakestuff).\n\n## How it works\n\nYou should start by reading [the Reddit\npost](https://www.reddit.com/r/options/comments/a36k4j/the_wheel_aka_triple_income_strategy_explained/)\nto get some background.\n\nThe strategy, as implemented here, does a few things differently from the one\ndescribed in the post above. For one, it\'s intended to be used to augment a\ntypical index-fund based portfolio with specific asset allocations. For\nexample, you might want to use a 60/40 portfolio with SPY (S&P500 fund) and\nTLT (20 year treasury fund).\n\nYou could use this tool on individual stocks, but I personally don\'t\nrecommend it because I am not smart enough to understand which stocks to buy.\nThat\'s why I just buy index funds.\n\nThetaGang will try to acquire your desired allocation of each stock or ETF\naccording to the weights you specify in the config. To acquire the positions,\nthe script will write puts when conditions are met (adequate buying power,\nacceptable contracts are available, enough shares needed, etc).\n\nThetaGang will continue to roll any open option positions indefinitely, with\nthe only exception being ITM puts. Once puts are in the money, they will be\nignored until they expire and are execised (after which you will own the\nunderlying).\n\nIn the case of deep ITM calls, the bot will prefer to roll the calls to next\nexpiration rather than allowing the underlying to get called away. If you\ndon\'t have adequate buying power available in your account, it\'s possible\nthat the options may get exercised instead of rolling forward and the process\nstarts back at the beginning. Please keep in mind this may have tax\nimplications, but that is outside the scope of this README.\n\nIn normal usage, you would run the script as a cronjob on a daily, hourly, or\nweekly basis according to your preferences.\n\n## Requirements\n\nThe bot is based on the [ib_insync](https://github.com/erdewit/ib_insync)\nlibrary, and uses [IBC](https://github.com/IbcAlpha/IBC) for managing the API\ngateway.\n\nTo use the bot, you\'ll need an Interactive Brokers account with a working\ninstallation of IBC. Additionally, you\'ll need an installation of Python 3.8\nor newer with the [`poetry`](https://python-poetry.org/) package manager.\n\n## Installation\n\n```shell\n$ pip install thetagang\n```\n\n## Usage\n\n```shell\n$ thetagang -h\n```\n\n## Running with Docker\n\nMy preferred way for running ThetaGang is to use a cronjob to execute Docker\ncommands. I\'ve built a Docker image as part of this project, which you can\nuse with your installation.\n\nTo run ThetaGang within Docker, you\'ll need to pass `config.ini` for [IBC\nconfiguration](https://github.com/IbcAlpha/IBC/blob/master/userguide.md) and\n[`thetagang.toml`](/thetagang.toml) for ThetaGang.\n\nThe easiest way to get the config files into the container is by mounting a\nvolume. For example, you can use the following command:\n\n```shell\n$ docker run --rm -it \\\n    -v ~/ibc:/ibc \\\n    docker.pkg.github.com/brndnmtthws/thetagang/thetagang:latest \\\n    --config /ibc/thetagang.toml\n```\n\n## Development\n\nCheck out the code to your local machine and install the Python dependencies:\n\n```shell\n$ poetry install\n$ poetry run thetaging -h\n...\n```\n\nYou are now ready to make a splash! 🐳\n',
    'author': 'Brenden Matthews',
    'author_email': 'brenden@brndn.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brndnmtthws/thetagang',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
