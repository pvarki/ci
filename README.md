![Build Status](https://github.com/pvarki/ci/actions/workflows/main.yml/badge.svg)

pvarki/ci
=========

A GitHub action to run [pvarki](https://github.com/pvarki) related and common ci steps.

### Using this action

To use this action, make a file `.github/workflows/main.yml`.  Here's a template to get started:

```yaml
on:
  pull_request:
  push:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
    - uses: pvarki/ci@main
      with:
        dockerfile-name: <dockerfile name> (default: Dockerfile)
        dockerfile-target: <target name> (mandatory)
        image-tag: <image tag name> (mandatory)

```

This does the following:

- clones/checkout the code (action)
- Runs: 
```
eval "$(ssh-agent -s)" && export DOCKER_BUILDKIT=1 && docker build -f ${{inputs.dockerfile-name}} --ssh default --target ${{inputs.dockerfile-target}} -t ${{inputs.image-tag}} .
```
- Runs:
```
docker run --rm -v ${{ github.workspace }}:/app -v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK ${{inputs.image-tag}}
```
