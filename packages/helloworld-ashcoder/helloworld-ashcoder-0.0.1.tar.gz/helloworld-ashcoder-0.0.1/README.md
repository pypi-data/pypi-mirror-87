# Hello World 
This is an example project demonstrating how to publish a python module to PyPI.

## Installtion
Run the following to install:

```python
pip install helloworld
```

## Usage
```python
from helloworld import say_hello
# Generate "Hello, World!"
say_hello()
# Generate "Hello, Everbody!"
say_hello("Everybody")
```
# Developing Hello World
To install helloworld, along with the tools you need to develop and run tests, run the following in your virtualenv:
```bash
pip install -e .[dev]
```