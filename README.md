# probam
Data for UBAM

## Description

This is a tool for analyzing UBAM products and finding multiple related products.

## Requirements

- Anaconda Python distribution
- Pipenv

## To set up

- Open Anaconda prompt
- Open the path to this repository
- run pipenv install

## Run

These python files are run in order:
- pipenv run python usborne.py
- pipenv run python products.py
- pipenv run python vectorizer.py
- pipenv run python search.py

## Troubleshoot

If you have issues with the nltk, read the errors to download the correct nltk packages.

If you get an error related to "images/whatever.svg" doesn't exist, create an images folder in the project directory and re-run vectorizer.py.
