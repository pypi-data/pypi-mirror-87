# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

# Test module for resonance_checks

import pytest
from spectroscpy import is_fermi_resonance, is_11_resonance, add_fermi_resonance

def test_is_fermi_resonance():

    assert is_fermi_resonance(5.0e-21, 2.0e-21, 1) == 0
    assert is_fermi_resonance(2.0e-21, 1.0e-21, 1) == 0

    assert is_fermi_resonance(2.0e-21, 2.0e-21, 1) == 0
    assert is_fermi_resonance(2.0e-21, 3.0e-21, 1) == 1

    assert is_fermi_resonance(2.0e-21, 2.0e-21, 0) == 1
    assert is_fermi_resonance(2.0e-21, 1.0e-21, 0) == 0


def test_add_fermi_resonance():

    fermi = []
    new = [1, 2, 3, 4]

    fermi = add_fermi_resonance(fermi, new)

    assert [[1, 2, 3, 4]] == fermi

    new = [1, 1, 0, 4]
    fermi = add_fermi_resonance(fermi, new)

    assert [[1, 2, 3, 4], [1, 0, 1, 4]] == fermi

    new = [1, 2, 3, 4]
    fermi = add_fermi_resonance(fermi, new)

    assert [[1, 2, 3, 4], [1, 0, 1, 4]] == fermi

    new = [2, 1, 3, 4]
    fermi = add_fermi_resonance(fermi, new)

    assert [[1, 2, 3, 4], [1, 0, 1, 4], [2, 1, 3, 4]] == fermi

    new = [2, 3, 1, 4]
    fermi = add_fermi_resonance(fermi, new)

    assert [[1, 2, 3, 4], [1, 0, 1, 4], [2, 1, 3, 4]] == fermi


def test_is_11_resonance():

    assert is_11_resonance(5.0e-21, 1.0e-22) == 0
    assert is_11_resonance(5.0e-21, 3.0e-22) == 0
    assert is_11_resonance(1.0e-21, 1.0e-65) == 0
    assert is_11_resonance(1.0e-21, 2.0e-65) == 1
    assert is_11_resonance(1.0e-22, 3.0e-22) == 1
