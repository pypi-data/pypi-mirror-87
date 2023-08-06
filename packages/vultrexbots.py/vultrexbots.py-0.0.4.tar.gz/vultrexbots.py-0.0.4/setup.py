from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = 'vultrexbots.py',
    version = '0.0.4',
    url = 'https://github.com/wezacon/vultrexbots.py',
    download_url = 'https://github.com/wezacon/vultrexbots.py/tarball/master',
    license = 'AGPL',
    author = 'Team Wezacon',
    author_email = 'wezacon.com@gmail.com',
    description = 'API wrapper for vultrexbots',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = [
        'vultrex',
        'bots-py',
        'wezacon'
    ],
    install_requires = [
        'setuptools',
        'requests',
        'six',
        'ujson'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)
