from setuptools import setup, find_packages

name: str = "SourceRank"
version: str = "1.0.4"
license: str = "MIT"
author: str = "David Martin-Gutierrez"
author_email: str = "dmargutierrez@gmail.com"

setup(name=name,
      version=version,
      packages=find_packages(),
      license=license,
      author=author,
      author_email=author_email,
      python_requires='>=3.6',
      install_requires=['requests','tldextract',
                        'tweepy','newsapi-python',
                        'numpy',
                        'GetOldTweets3',
                        'coloredlogs',
                        'fuzzywuzzy',
                        'scipy',
                        'pycountry',
                        'python-dateutil',
                        'pandas',
                        'aiodns',
                        'aiohttp-socks',
                        'aiohttp',
                        'cchardet',
                        'elasticsearch',
                        'fake-useragent',
                        'geopy',
                        'googletransx',
                        'schedule',
                        'googlesearch-python',
                        'python-restcountries',
                        'twine',
                        'bumpversion',
                        'botometer',
                        'dataclasses',
                        'langdetect',
                        'more_itertools',
                        'python-Levenshtein'])