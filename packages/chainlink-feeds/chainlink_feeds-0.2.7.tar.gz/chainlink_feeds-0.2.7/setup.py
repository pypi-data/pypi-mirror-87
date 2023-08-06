from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
short_description = 'Python module to get price and other data from the decentralized chainlink community resources'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    # How you named your package folder (MyLib)  # Chose the same as "name"
    name='chainlink_feeds',
    version='0.2.7',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Patrick Collins',                   # Type in your name
    author_email='patrick@alphachain.io',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/alphachainio',
    # Keywords that define your package best
    keywords=['decentralized', 'data', 'chainlink',
              'cryptocurrency', 'blockchain'],
    install_requires=[            # I get to this in a second
        'configparser',
        'pandas',
        'web3'
    ],
    test_requires=[
        'pytest',
        'configparser'
        'pandas',
        'web3'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(
        exclude=['test_chainlink_feeds', 'workflows', 'images']),
    # package_data={
    #     'chainlink_feeds': [],
    # }
)
