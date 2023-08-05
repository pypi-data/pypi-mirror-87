
# mito-sheet

[![Build Status](https://travis-ci.org/mito/mito.svg?branch=master)](https://travis-ci.org/mito/mito)
[![codecov](https://codecov.io/gh/mito/mito/branch/master/graph/badge.svg)](https://codecov.io/gh/mito/mito)


The Mito Spreadsheet

## Installation for Development

Run all the following commands in the Mito folder. 

First create an enter a python venv, for replicability
```bash
python3 -m venv venv;
source venv/bin/activate;
```

Once the virtual enviornment is running, then install Jupyter and Jupyterlab and pandas and analytics python
```bash
pip install -r requirements.txt;
```

Then install the python package. This will also build the JS packages.
```bash
pip install -e ".[test, examples]";
```

When developing your extensions, you need to manually enable your extensions with the
notebook / lab frontend. For lab, this is done by the command:
```
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build
jupyter labextension install .
```

Here, it is reccomended to clean your Yarn cache, which for some reason fills up after the above command (eventually bricking your computer, lol).
```
yarn cache clean
```

For classic notebook, you can run:
```
jupyter nbextension install --sys-prefix --symlink --overwrite --py mitosheet
jupyter nbextension enable --sys-prefix --py mitosheet
```

Note that the `--symlink` flag doesn't work on Windows, so you will here have to run
the `install` command every time that you rebuild your extension. For certain installations
you might also need another flag instead of `--sys-prefix`, but we won't cover the meaning
of those flags here.

### All as one command

Make sure you run this from the Mito folder!

```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pip install -e ".[test, examples]" && jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build && jupyter labextension install . && yarn cache clean && jupyter lab --watch
```

### How to see your changes
#### Typescript:
To continuously monitor the project for changes and automatically trigger a rebuild, start Jupyter in watch mode:
```bash
jupyter lab --watch
```
And in a separate session, begin watching the source directory for changes:
```bash
npm run watch:lib
```

When you make a change to the code and save it, the `npm run watch:lib` command will cause TypeScript to compile, resulting in a message that says "Found 0 errors." Then, the `jupyter lab --watch` command will recompile Jupyter, and generate some yellow success text.

Then refresh your browser and the changes should take effect. If you changed the Python code, you will have to restart your kernel as well. 

#### Python:
If you make a change to the python code then you will need to restart the notebook kernel to have it take effect.

### Testing

There are both manual tests and automated tests. 

#### Automated Tests

Run automated tests with
```
pytest
```
Automated tests can be found in  `mitosheet/test`. These are tests written using standard `pytest` tools, and include tests like testing the evaluate function, the MitoWidget, and all other pure Python code. 

#### Manual Tests

Run manual tests by opening `examples/manual_tests` in `jupyter lab`, and selecting each workbook. Each workbook contains instructions on how to run the test and the expected outputs. 

To write a manual test of your own, simply create a new notebook in the `examples/manual` folder and write a test here - or in a subfolder, if it fits better there. 

These tests should be run _before releases_ - but need not be run to merge things into the dev branch. 

### Linting

This project has linting set up for both (Python)[https://flake8.pycqa.org/en/latest/index.html] and (typescript)[https://github.com/typescript-eslint/typescript-eslint]. 

Run typescript linting with the command 
```
npx eslint . --ext .tsx --fix
```

### Documentation

To learn more about writing documentation, see the README in the `/docs` folder!

## Installing the Extension

TODO! These instructions will apply in the future.

You can install using `pip`:

```bash
pip install mitosheet
```

Or if you use jupyterlab:

```bash
pip install mitosheet
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] mitosheet
```

