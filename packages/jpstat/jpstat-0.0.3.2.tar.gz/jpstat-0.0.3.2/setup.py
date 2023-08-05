# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jpstat',
 'jpstat.estat',
 'jpstat.estat.util',
 'jpstat.estatFile',
 'jpstat.util']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0,<2.0', 'requests>=2.0,<3.0', 'requests_html>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'jpstat',
    'version': '0.0.3.2',
    'description': 'A python library for accessing official statistics of Japan.',
    'long_description': '# jpstat\n\nA python package for accessing the official statistics of Japan.\n\n## Features\n\n- [estat api](#estat-api)\n- [estat file](#estat-file)\n\n## Install\n\n```sh\npip install jpstat\n```\n\n## estat API\n\n[estat](https://www.e-stat.go.jp/) is the official site for government statistics in Japan. Its api service offers data of over 250+ statistics in Japan. You need to register an api key to access to the statistics.\n\n### Functions\n\nAll functions return one or multiple pandas DataFrames.\n\nTo see a list of statistics offered by estat api\n\n```python\nimport jpstat\nstat = jpstat.estat.get_stat(key=YOUR_API_KEY)\n```\n\nTo search data by either the code of a statistic or some key words\n\n```python\ndata = jpstat.estat.get_list(statsCode="00400001")\ndata = jpstat.estat.get_list(searchWord="企業")\n```\n\nTo dowload data\n\n```python\ndata, note = jpstat.estat.statsDataId(statsCode="0000040001")\n```\n\n### Configuration\n\nYou can pass the estat api key to each function. Or you can set a configuration\n\n```python\njpstat.options["estat.api_key"] = "MY_API_KEY"\n```\n\nYou can also set the language from Japanese (default, "J") to English\n\n```python\njpstat.options["estat.lang"] = "E"\n```\n\nTo see a list of valid configuration options\n\n```python\njpstat.config.describe_options()\n```\n\n## estat File\n\nMany statistics and datasets in estat can not be accessed through API, but are excel, csv, or pdf files and can be downloaded. Here jpstat provides the functions that scrapes the information of statistics and download the files. Api key for estat is not needed, and the result is in Japanese only.\n\n### Functions\n\nTo see a list of all statistics in estat that have downloadable files\n\n```python\ndata = jpstat.estatFile.get_stat()\n```\n\nIt will take some time to scraping the website of estat at the first time and then save the list to `options["estat.data_dir"]`. From then on, the function would first try to read the local file. You can force to scrape again by setting `update=True`.\n\nTo search data files by code of a statistic and the survey year (optional)\n\n```python\ndata = jpstat.estatFile.get_list(statsCode="00400001")\ndata = jpstat.estatFile.get_list(statsCode="00400001", year="1950")\n```\n\nAgain, you can save the result by setting `save=True`, and from next time jpstat would first check if the result already exists.\n\nTo download the file by using the information of data id and file type ("EXCEL"/"CSV"/"PDF") gotten from the result of `estatFile.get_list`\n\n```python\njpstat.estatFile.get_file(statsDataId="000029094935", file_type="EXCEL")\n```\n\nThe file would be downloaded to current folder by default.\n',
    'author': 'Xuanli Zhu',
    'author_email': 'akaguro.koyomi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alalalalaki/jpstat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
