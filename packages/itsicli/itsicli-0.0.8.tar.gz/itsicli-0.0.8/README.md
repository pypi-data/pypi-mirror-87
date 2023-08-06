# The ITSI Command Line Interface (CLI)

## Setup Virtualenv

```
python3 -m venv /path/to/new/virtual/environment

source /path/to/new/virtual/environment/bin/activate
```

## Install the Python package

```
pip install itsicli
```


## Using "itsi-use-case"

The itsi-use-case command that is shipped with the Python package assists in creating and
managing ITSI Use Cases.

The general end-to-end workflow is as follows:
1. Initialize a Use Case workspace
1. Create a Use Case (or optionally import from an ITSI backup file)
1. Continue to add, remove, or edit content from the Use Case
1. Add any supporting Splunk knowledge objects (lookups, transforms, props, etc.)
1. Validate the Use Case through the `validate` command 
1. Submit the Use Case to either:
    - Splunkbase (must first run the `build` command)
    - The ITSI Use Case Library via a pull request on Github


### An example of creating an ITSI Use Case

TODO

## Build the distribution archive

Install the build dependencies:
```
pip install --upgrade setuptools wheel
```

### Generate the Python package

Run this command to generate the Python distribution archive:
```
make
```

### Upload to the Python Package Index

Install the dependencies required for uploading to the index:

```
pip install --upgrade twine
```

Upload to PyPI:

```
make upload
```
