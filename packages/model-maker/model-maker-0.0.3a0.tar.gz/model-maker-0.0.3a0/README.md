# ModelMaker

Framework and utilities for creating and validating ML models

## Features

- CLI tool for creation and validation of models
- Choose from predefined templates
- validate model
- write custom tests for each model

## Install the tool

This will install the modelmaker CLI tool

```bash
git clone https://github.com/shirecoding/ModelMaker.git
cd ModelMaker
pip3 install ./
```

alternatively install from pypi

```
pip3 install model-maker
```

## List Templates

```bash
modelmaker templates
```

## Create a New Project

```bash
modelmaker new --path MyNewProject --name mynewmodel --template default
```

This will create the python package *mynewmodel* inside directory *MyNewProject*

**Current Templates**

- default (simple classification model using mnist dataset example)