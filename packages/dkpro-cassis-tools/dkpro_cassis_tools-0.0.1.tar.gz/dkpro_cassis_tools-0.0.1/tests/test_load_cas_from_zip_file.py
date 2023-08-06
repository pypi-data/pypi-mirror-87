import pytest
from dkpro_cassis_tools.load_cas_from_zip_file import load_cas_from_zip_file


def test_load_cas_from_zip_file():
    with open('data/cas.zip', 'rb') as f:
        cas = load_cas_from_zip_file(f)
    assert 1 == 1

