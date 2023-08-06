# Tools for glenda

This is some tools for glenda projects

## How to build
```
# Build new version 
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel

# For publish new version
python3 -m pip install --user --upgrade twine
python3 -m twine upload dist/*

```