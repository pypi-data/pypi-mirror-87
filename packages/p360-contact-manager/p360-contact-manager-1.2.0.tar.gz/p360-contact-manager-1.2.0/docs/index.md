![test](https://github.com/greenbird/p360-contact-manager/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/greenbird/p360-contact-manager/branch/master/graph/badge.svg)](https://codecov.io/gh/greenbird/p360-contact-manager)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

# P360 Contact Manager

**[Documentation](https://greenbird.github.io/p360-contact-manager/) |
[Source Code](https://github.com/greenbird/p360-contact-manager) |
[Task Tracker](https://github.com/greenbird/p360-contact-manager/issues)**

While there are existing solutions to synchronize with systems such as brønnøysundregisteret. They can be used via GUI only and are slow to enrich and update the data. Some of the tools can create duplicates that are not accepted among all the systems.

This project addresses the following issues:

* Creates simple and easy to use CLI interface
* Runs faster than existing solutions
* Removes duplicates
* Multi-platform


## Quickstart

Installing the package
> `p360-contact-manager` is on [pypi](https://pypi.org/project/p360-contact-manager/) and can be installed with pip

```sh
pip install p360-contact-manager
```

This installs the `p360` CLI command. If you have installed it in a virtualenv, then remember to activate it before usng `p360`. If you have used `poetry` to install it, run it with `poetry run p360`.


!!! note
    In the examples replace `your_key` with your api authkey and `your_url` with the url to your api.


Start with testing the connection
```sh
p360 --authkey your_key --p360_base_url your_url test
```


Find duplicates
```sh
p360 --authkey your_key --p360_base_url your_url duplicates
```
> Check the file `duplicate_worklist.json` thats created if everything looks okay. The filename can also be configured by using `--output my_duplicate_worklist.json`.

Run update
```sh
p360 -ak your_key -pbu your_url --worklist duplicates_worklist.json update
```

This creates a file called `result_update.json` in your current working directory. This file contains a list of all enterprises which have been updated by recno. If there are any errors then those can be found in the same file with an error message and the payload that caused the error.
