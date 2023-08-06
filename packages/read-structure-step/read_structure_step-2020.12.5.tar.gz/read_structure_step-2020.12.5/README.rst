===================
Read Structure Step
===================

.. image:: https://img.shields.io/travis/molssi-seamm/read_structure_step.svg
   :target: https://travis-ci.org/molssi-seamm/read_structure_step
   :alt: Build Status

.. image:: https://codecov.io/gh/molssi-seamm/read_structure_step/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/molssi-seamm/read_structure_step
   :alt: Code Coverage

.. image:: https://img.shields.io/lgtm/grade/python/g/molssi-seamm/read_structure_step.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/molssi-seamm/read_structure_step/context:python
   :alt: Code Quality

.. image:: https://readthedocs.org/projects/read_structure-step/badge/?version=latest
   :target: https://read_structure-step.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://pyup.io/repos/github/molssi-seamm/read_structure_step/shield.svg
   :target: https://pyup.io/repos/github/molssi-seamm/read_structure_step/
   :alt: Updates for Dependencies

.. image:: https://img.shields.io/pypi/v/read_structure_step.svg
   :target: https://pypi.python.org/pypi/read_structure_step
   :alt: PyPi VERSION

Description
===========

A SEAMM plugin to read common formats found in computational chemistry. The current version
uses OpenBabel as an engine to parse various formats such as PDB, Mol2 or XYZ and transform
them into the SEAMM structure format for further use in SEAMM flowcharts. 

Features
========

- Emphasis in ease-of-use and simplicity. The public interface consists of a single function.
- Automatic file type recognition.
- OpenBabel as an engine to parse formats, but other engines can be easily implemented.
- Easily extensible to new formats.
- Current support for PDB, Mol2 and XYZ files. 
- Free software: BSD-3-Clause
- Documentation: https://read-structure-step.readthedocs.io.

Example
-------

.. code:: python

 import read_structure_step
 seamm_structure = read_structure_step.read("spc.xyz")

Credits
---------

This package was created with Cookiecutter_ and the `molssi-seamm/cookiecutter-seamm-plugin`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`molssi-seamm/cookiecutter-seamm-plugin`: https://github.com/molssi-seamm/cookiecutter-seamm-plugin

Developed by the Molecular Sciences Software Institute (MolSSI_),
which receives funding from the `National Science Foundation`_ under
award ACI-1547580

.. _MolSSI: https://www.molssi.org
.. _`National Science Foundation`: https://www.nsf.gov
