from dkpro_cassis_tools import load_cas_from_zip_file
from dkpro_cassis_tools import restore_cas_segmentation_by_newline
from dkpro_cassis_tools import SENTENCE_NS


def test_dump_cas_to_zip_file():
    with open('data/cas_restore_segmentation_by_newline.zip', 'rb') as f:
        cas = load_cas_from_zip_file(f)
        assert len(list(cas.select(SENTENCE_NS))) == 1

        re_segmented_cas = restore_cas_segmentation_by_newline(cas)
        assert len(list(re_segmented_cas.select(SENTENCE_NS))) == 2

