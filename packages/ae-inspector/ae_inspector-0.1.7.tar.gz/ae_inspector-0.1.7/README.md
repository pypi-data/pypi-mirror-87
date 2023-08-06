<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
  All changes will be deployed automatically to all the portions of this namespace package.
-->
# inspector portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_inspector/master?logo=python)](
    https://gitlab.com/ae-group/ae_inspector)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_inspector)](
    https://pypi.org/project/ae-inspector/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes for to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_inspector/coverage.svg)](
    https://ae-group.gitlab.io/ae_inspector/coverage/ae_inspector_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_inspector/mypy.svg)](
    https://ae-group.gitlab.io/ae_inspector/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_inspector/pylint.svg)](
    https://ae-group.gitlab.io/ae_inspector/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_inspector)](
    https://pypi.org/project/ae-inspector/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_inspector)](
    https://pypi.org/project/ae-inspector/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_inspector)](
    https://pypi.org/project/ae-inspector/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_inspector)](
    https://pypi.org/project/ae-inspector/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_inspector)](
    https://libraries.io/pypi/ae-inspector)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_inspector)](
    https://pypi.org/project/ae-inspector/#files)


## installation


Execute the following command for to use the ae.inspector module in your
application. It will install ae.inspector into your python (virtual) environment:
 
```shell script
pip install ae-inspector
```

If you instead want to contribute to this portion then first fork
[the ae_inspector repository at GitLab](https://gitlab.com/ae-group/ae_inspector "ae.inspector code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_inspector):

```shell script
pip install -e .[dev]
```

The last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or for to extend the portion documentation.
For to contribute only to the unit tests or the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

More info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.inspector.html#module-ae.inspector
"ae_inspector documentation").

<!-- Common files version 0.0.60 deployed version 0.1.1 (with 0.0.60)
     to https://gitlab.com/ae-group as ae_inspector module as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project/ae-inspector as namespace portion ae-inspector.
-->
