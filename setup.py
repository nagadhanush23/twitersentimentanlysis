from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Read the README file for a long description (if available)
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Twitter Sentiment Analysis',
    version='1.0.0',

    description='A script to analyze the sentiments of tweets related to any topic.',
    long_description=long_description,
    long_description_content_type="text/markdown", 

    author='Chiluveru Nagadhanush',
    author_email='nagadhanush23@gmail.com', 

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='python twitter sentiment-analysis textblob nlp tweepy nltk',

    install_requires=[
        'tweepy',
        'textblob',
        'matplotlib',
        'nltk'
    ],
)
