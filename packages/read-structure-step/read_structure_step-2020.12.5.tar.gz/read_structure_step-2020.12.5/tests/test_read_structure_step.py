#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `read.py` module."""

import pytest  # noqa: F401
import read_structure_step  # noqa: F401
from . import build_filenames

from molsystem.systems import Systems

systems = Systems()
system = systems.create_system('seamm', temporary=True)


@pytest.mark.parametrize('file_name', [1, [], {}, 1.0])
def test_read_filename_type(file_name):

    with pytest.raises(TypeError):
        read_structure_step.read(file_name, system)


def test_empty_filename():

    with pytest.raises(NameError):
        read_structure_step.read('', system)


def test_unregistered_reader():

    with pytest.raises(KeyError):

        xyz_file = build_filenames.build_data_filename('spc.xyz')
        read_structure_step.read(xyz_file, system, extension='.mp3')
