================
notebook2script
================

.. start short_desc

**Convert Jupyter Notebooks to Python Scripts.**

.. end short_desc

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor| |pre_commit_ci|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/notebook2script/latest?logo=read-the-docs
	:target: https://notebook2script.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/notebook2script/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/notebook2script/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://github.com/domdfcoding/notebook2script/workflows/Linux%20Tests/badge.svg
	:target: https://github.com/domdfcoding/notebook2script/actions?query=workflow%3A%22Linux+Tests%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/notebook2script/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/notebook2script/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/notebook2script/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/notebook2script/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Test Status

.. |requires| image:: https://requires.io/github/domdfcoding/notebook2script/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/notebook2script/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/notebook2script/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/notebook2script?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/notebook2script?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/notebook2script
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/notebook2script
	:target: https://pypi.org/project/notebook2script/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/notebook2script?logo=python&logoColor=white
	:target: https://pypi.org/project/notebook2script/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/notebook2script
	:target: https://pypi.org/project/notebook2script/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/notebook2script
	:target: https://pypi.org/project/notebook2script/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/notebook2script
	:target: https://github.com/domdfcoding/notebook2script/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/notebook2script
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/notebook2script/v0.2.0
	:target: https://github.com/domdfcoding/notebook2script/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/notebook2script
	:target: https://github.com/domdfcoding/notebook2script/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/notebook2script/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/notebook2script/master
	:alt: pre-commit.ci status

.. end shields

|

Installation
--------------

``pkgname`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install pkgname

To install with ``conda``:

.. code-block:: bash

	$ conda config --add channels http://conda.anaconda.org/domdfcoding
	$ conda install pkgname
