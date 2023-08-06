# Catmeow simple python package

This repo serves as an instruction on how to publish packaged to PyPI

## Steps

### configuring env
If you want to avoid entering your username, you can configure TestPyPI in your `$HOME/.pypirc`:

```
[testpypi]
username = <USER>
password = <PASS>
```

### build
`python -m pep517.build .`

### upload to test pypi
`twine upload --repository testpypi dist/*`

### download from test pypi
`pip install --index-url https://test.pypi.org/simple/ catmeow`

### uninstall
`pip uninstall catmeow`

## References
[Instruction @medium](https://zjor.medium.com/packaging-a-runnable-python-module-de43ac12148)
