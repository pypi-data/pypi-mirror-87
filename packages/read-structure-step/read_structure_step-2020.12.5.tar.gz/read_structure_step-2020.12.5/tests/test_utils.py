#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `utils` module."""

import pytest  # noqa: F401
import read_structure_step  # noqa: F401
from . import build_filenames

from molsystem.systems import Systems

systems = Systems()
system = systems.create_system('seamm', temporary=True)

bond_string = """\
   i  j  bondorder
1  1  2          1
2  1  3          1"""


@pytest.mark.parametrize("file_name", ["spc.xyz", "spc"])
@pytest.mark.parametrize("extension", [None, ".xyz", "xyz", "XYZ", "xYz"])
def test_extensions(file_name, extension):

    xyz_file = build_filenames.build_data_filename(file_name)
    read_structure_step.read(xyz_file, system, extension=extension)

    assert system.n_atoms() == 3
    assert all(atom in ["O", "H", "H"] for atom in system.atoms.symbols())

    coordinates = system.atoms.coordinates()
    assert len(coordinates) == 3
    assert all(len(point) == 3 for point in coordinates)

    assert system.bonds.n_bonds() == 2
    assert str(system.bonds) == bond_string


def test_sanitize_file_format_regex_validation():

    with pytest.raises(NameError):
        read_structure_step.read("spc.xyz", system, extension=".xy-z")
