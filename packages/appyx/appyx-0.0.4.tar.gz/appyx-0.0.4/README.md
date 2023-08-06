# Appyx

## To upload an Appyx version to PyPi
First, change the version number in file setup.py

To generate the distribution:
```
python3 setup.py sdist bdist_wheel
```

To upload:
```
python3 -m twine upload dist/*
```