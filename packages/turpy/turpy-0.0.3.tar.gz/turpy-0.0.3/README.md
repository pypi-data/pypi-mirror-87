# Turpy

This is an example project aim to collect useful code published as python module to PyPi.

It is unstable and API could change without a warning. 

## Installation

Run the following to install:

```python
pip install turpy
```

## Usage

```python
from turpy.io import load_yaml

# load a `yaml` file
my_dict = load_yaml(filepath='filepath/to/myfile.yaml>')

```

# Developing `turpy`

To install `turpy`, along with the tools you need to develop and run tests, rin the following in your virtualenv:

```bash
$ pip install -e .[dev]
``` 