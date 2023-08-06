from dkist_fits_specifications.spec214 import (load_full_spec214,
                                               load_spec214,
                                               expand_index_k,
                                               expand_index_d,
                                               load_expanded_spec214)


def test_load_full_214():
    load_full_spec214()


def test_load_214():
    load_spec214()


def test_expand_k():
    spec = load_spec214()['dataset']
    schema = expand_index_k(spec, DAAXES=2, DEAXES=1)
    assert "DINDEX3" in schema


def test_expand_d():
    spec = load_spec214()['dataset']
    schema = expand_index_d(spec, NAXIS=2, DNAXIS=5)
    assert "DTYPE5" in schema


def test_expanded_schema():
    schemas = load_expanded_spec214(DAAXES=2, DEAXES=1, NAXIS=2, DNAXIS=5, INSTRUME="notthedkist")
    assert "DINDEX3" in schemas['dataset']
    assert "NAXIS1" in schemas['fits']
    assert "DTYPE5" in schemas['dataset']
