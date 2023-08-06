# xsanta

Secret Santa sender / receiver generator

[![PyPI version](https://img.shields.io/pypi/v/xsanta.svg)](https://badge.fury.io/py/xsanta)
[![Actions Status](https://github.com/alpha-xone/xsanta/workflows/Auto%20CI/badge.svg)](https://github.com/alpha-xone/xsanta/actions)
[![PyPI version](https://img.shields.io/pypi/pyversions/xsanta.svg)](https://badge.fury.io/py/xsanta)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/xsanta)](https://pypistats.org/packages/xsanta)

[![Coffee](https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png)](https://www.buymeacoffee.com/Lntx29Oof)

## Installation

```commandline
pip install xsanta
```

## Example

In python:

```
>>> from secret import santa
>>> invited = [
...     'Iron Man', 'Captain America', 'Thanos', 'Hulk',
...     'Black Widow', 'Thor', 'Loki', 'Wanda Maximoff',
... ]
>>> excluded = [
...     ('Iron Man', 'Captain America'),
...     ('Thor', 'Loki'),
...     ('Black Widow', 'Hulk'),
... ]
>>> santa.run(invited, excluded)
Thor 🎁 >> Thanos 🎁 >> Loki 🎁 >> Hulk 🎁 >> Iron Man 🎁 >> Thor
Captain America 🎁 >> Black Widow 🎁 >> Wanda Maximoff 🎁 >> Captain America
```

In command line:

```cmd
python santa.py "['Iron Man', 'Captain America', 'Thanos']" --emoji=False
Captain America >> Thanos >> Iron Man >> Captain America
```
