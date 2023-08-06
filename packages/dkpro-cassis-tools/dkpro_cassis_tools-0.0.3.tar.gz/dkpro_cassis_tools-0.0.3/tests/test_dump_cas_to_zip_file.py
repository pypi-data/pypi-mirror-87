from dkpro_cassis_tools import dump_cas_to_zip_file
from dkpro_cassis_tools import load_cas_from_zip_file
from dkpro_cassis_tools import SENTENCE_NS
import tempfile


def test_dump_cas_to_zip_file():
    with open('data/cas.zip', 'rb') as f:
        cas1 = load_cas_from_zip_file(f)

    with tempfile.NamedTemporaryFile() as f:
        dump_cas_to_zip_file(cas1, f)
        cas2 = load_cas_from_zip_file(f)

        for sentence1, sentence2 in zip(
                cas1.select(SENTENCE_NS),
                cas2.select(SENTENCE_NS)):
            assert sentence1.get_covered_text() == sentence2.get_covered_text()