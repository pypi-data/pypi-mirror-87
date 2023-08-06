==============
formelsammlung
==============

+---------------+----------------------------------------------------------------------+
| **General**   | |maintenance| |license| |black| |rtd|                                |
+---------------+----------------------------------------------------------------------+
| **Pipeline**  | |azure_pipeline| |azure_coverage|                                    |
+---------------+----------------------------------------------------------------------+
| **Tools**     | |poetry| |tox| |pytest| |sphinx|                                     |
+---------------+----------------------------------------------------------------------+
| **VC**        | |vcs| |gpg| |semver| |pre-commit|                                    |
+---------------+----------------------------------------------------------------------+
| **Github**    | |gh_release| |gh_commits_since| |gh_last_commit|                     |
|               +----------------------------------------------------------------------+
|               | |gh_stars| |gh_forks| |gh_contributors| |gh_watchers|                |
+---------------+----------------------------------------------------------------------+
| **PyPI**      | |pypi_release| |pypi_py_versions| |pypi_implementations|             |
|               +----------------------------------------------------------------------+
|               | |pypi_status| |pypi_format| |pypi_downloads|                         |
+---------------+----------------------------------------------------------------------+


**Collection of different multipurpose functions.**

This library is a collection of different functions I developed which I use in different
projects so I put them here. New features are added when I need them somewhere.


Functionality
=============

- ``getenv_typed()``: is a wrapper around ``os.getenv`` returning the value of the environment variable in the correct python type.
- ``calculate_string()``: takes an arithmetic expression as a string and calculates it.
- ``SphinxDocServer``: is a flask plugin to serve the repository's docs build as HTML (by sphinx). Needs ``flask`` extra to be also installed to work.
- ``env_exe_runner()``: is a function to call a given ``tool`` from the first venv/tox/nox environment that has it installed in a list of venv/tox/nox environments.
- ``get_venv_path()``: is a function to get the path to the current venv.
- ``get_venv_bin_dir()``: is a function to get the path to the bin/Scripts dir of a given venv.
- ``get_venv_tmp_dir()``: is a function to get the path to the tmp/temp dir of a given venv.
- ``get_venv_site_packages_dir()``: is a function to get the path to the site-packages dir of a given venv.
- ``where_installed()``: is a function to find the installation places in and outside a venv.


Prerequisites
=============

*Works only with python version >= 3.6*

A new version of ``pip`` that supports PEP-517/PEP-518 is required.
When the setup fails try updating ``pip``.


Disclaimer
==========

No active maintenance is intended for this project.
You may leave an issue if you have a questions, bug report or feature request,
but I cannot promise a quick response time.


.. .############################### LINKS ###############################


.. General
.. |maintenance| image:: https://img.shields.io/badge/No%20Maintenance%20Intended-X-red.svg?style=flat-square
    :target: http://unmaintained.tech/
    :alt: Maintenance - not intended

.. |license| image:: https://img.shields.io/github/license/Cielquan/formelsammlung.svg?style=flat-square&label=License
    :alt: License
    :target: https://github.com/Cielquan/formelsammlung/blob/master/LICENSE.txt

.. |black| image:: https://img.shields.io/badge/Code%20Style-black-000000.svg?style=flat-square
    :alt: Code Style - Black
    :target: https://github.com/psf/black

.. |rtd| image:: https://img.shields.io/readthedocs/formelsammlung/latest.svg?style=flat-square&logo=read-the-docs&logoColor=white&label=Read%20the%20Docs
    :alt: Read the Docs - Build Status (latest)
    :target: https://formelsammlung.readthedocs.io/en/latest/


.. Pipeline
.. |azure_pipeline| image:: https://img.shields.io/azure-devops/build/cielquan/05507266-5d2e-4862-80f9-9f2b439814c8/8?style=flat-square&logo=azure-pipelines&label=Azure%20Pipelines
    :target: https://dev.azure.com/cielquan/formelsammlung/_build/latest?definitionId=8&branchName=master
    :alt: Azure DevOps builds

.. |azure_coverage| image:: https://img.shields.io/azure-devops/coverage/cielquan/formelsammlung/8?style=flat-square&logo=azure-pipelines&label=Coverage
    :target: https://dev.azure.com/cielquan/formelsammlung/_build/latest?definitionId=8&branchName=master
    :alt: Azure DevOps Coverage


.. Tools
.. |poetry| image:: https://img.shields.io/badge/Packaging-poetry-brightgreen.svg?style=flat-square
    :target: https://python-poetry.org/
    :alt: Poetry

.. |tox| image:: https://img.shields.io/badge/Automation-tox-brightgreen.svg?style=flat-square
    :target: https://tox.readthedocs.io/en/latest/
    :alt: tox

.. |pytest| image:: https://img.shields.io/badge/Test%20framework-pytest-brightgreen.svg?style=flat-square
    :target: https://docs.pytest.org/en/latest/
    :alt: Pytest

.. |sphinx| image:: https://img.shields.io/badge/Doc%20builder-sphinx-brightgreen.svg?style=flat-square
    :target: https://www.sphinx-doc.org/
    :alt: Sphinx


.. VC
.. |vcs| image:: https://img.shields.io/badge/VCS-git-orange.svg?style=flat-square&logo=git
    :target: https://git-scm.com/
    :alt: VCS

.. |gpg| image:: https://img.shields.io/badge/GPG-signed-blue.svg?style=flat-square&logo=gnu-privacy-guard
    :target: https://gnupg.org/
    :alt: Website

.. |semver| image:: https://img.shields.io/badge/Versioning-semantic-brightgreen.svg?style=flat-square
    :alt: Versioning - semantic
    :target: https://semver.org/

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=flat-square&logo=pre-commit&logoColor=yellow
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit


.. Github
.. |gh_release| image:: https://img.shields.io/github/v/release/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :alt: Github - Latest Release
    :target: https://github.com/Cielquan/formelsammlung/releases/latest

.. |gh_commits_since| image:: https://img.shields.io/github/commits-since/Cielquan/formelsammlung/latest.svg?style=flat-square&logo=github
    :alt: Github - Commits since latest release
    :target: https://github.com/Cielquan/formelsammlung/commits/master

.. |gh_last_commit| image:: https://img.shields.io/github/last-commit/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :alt: Github - Last Commit
    :target: https://github.com/Cielquan/formelsammlung/commits/master

.. |gh_stars| image:: https://img.shields.io/github/stars/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :alt: Github - Stars
    :target: https://github.com/Cielquan/formelsammlung/stargazers

.. |gh_forks| image:: https://img.shields.io/github/forks/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :alt: Github - Forks
    :target: https://github.com/Cielquan/formelsammlung/network/members

.. |gh_contributors| image:: https://img.shields.io/github/contributors/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :alt: Github - Contributors
    :target: https://github.com/Cielquan/formelsammlung/graphs/contributors

.. |gh_watchers| image:: https://img.shields.io/github/watchers/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :alt: Github - Watchers
    :target: https://github.com/Cielquan/formelsammlung/watchers


.. PyPI
.. |pypi_release| image:: https://img.shields.io/pypi/v/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072
    :alt: PyPI - Package latest release
    :target: https://pypi.org/project/formelsammlung/

.. |pypi_py_versions| image:: https://img.shields.io/pypi/pyversions/formelsammlung.svg?style=flat-square&logo=python&logoColor=FBE072
    :alt: PyPI - Supported Python Versions
    :target: https://pypi.org/project/formelsammlung/

.. |pypi_implementations| image:: https://img.shields.io/pypi/implementation/formelsammlung.svg?style=flat-square&logo=python&logoColor=FBE072
    :alt: PyPI - Supported Implementations
    :target: https://pypi.org/project/formelsammlung/

.. |pypi_status| image:: https://img.shields.io/pypi/status/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072
    :alt: PyPI - Stability
    :target: https://pypi.org/project/formelsammlung/

.. |pypi_format| image:: https://img.shields.io/pypi/format/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072
    :alt: PyPI - Format
    :target: https://pypi.org/project/formelsammlung/

.. |pypi_downloads| image:: https://img.shields.io/pypi/dm/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072
    :target: https://pypi.org/project/formelsammlung/
    :alt: PyPI - Monthly downloads
