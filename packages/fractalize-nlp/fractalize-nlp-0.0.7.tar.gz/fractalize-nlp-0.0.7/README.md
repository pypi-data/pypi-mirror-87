# Fractalize NLP
A group of Modules encompassing common components that are used in all Fractalize NLP products and deployments

## string_generators
Module that enables encoding of structured domain knowledge into a conditional processing graph. The conditional
processing graph is used to generate random samples of unstructured strings which represent natural language
invocations of the underlying domain knowledge

## Building the package
To build a deployable binary including source files execute:
```console
$ python3 setup.py sdist bdist_wheel
```
This will produce fractalize_nlp/dist/fractalize_nlp-<version>-py3.7.egg

If planning to publish the package, update the version number in setup.py first. 

## Publishing the package
Use PyPi to distribute the package as follows: 

```console
$ twine upload dist/fractalize-nlp-<build version>
```
Note: 
1. Make sure the package has been built with the correct version number. 
2. Make sure all the code changes have been merged before publishing the package.

## Testing the package
To run the test suite, run either:
```console
$ pytest 
```
or
```console
$ coverage run -m pytest
```
To generate the coverage report, the test suite must be invoked via coverage first. Then, run:
```console
$ coverage report -m <module_name>/<relevant_script>.py
```
To generate the full coverage report, run:
```console
$ coverage report -m
```
## License
MIT © fractal-dataminds
