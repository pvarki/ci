![Build Status](https://github.com/pvarki/ci/actions/workflows/main.yml/badge.svg)

pvarki/ci
=========

A GitHub action to run [pvarki](https://github.com/pvarki) related and common ci steps.

### using this action

To use this action, make a file `.github/workflows/main.yml`.  Here's a template to get started:

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
    - uses: pvarki/ci@main
```

This does the following:

- clones/checkout the code
- installs python
- runs [pre-commit/action](https://github.com/pre-commit/action)
