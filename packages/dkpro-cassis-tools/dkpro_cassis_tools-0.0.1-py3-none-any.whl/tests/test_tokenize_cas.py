from typing import List
from dkpro_cassis_tools import load_cas_from_zip_file
from dkpro_cassis_tools import tokenize_cas
from dkpro_cassis_tools import SENTENCE_NS, TOKEN_NS
import MeCab


def test_tokenize_cas():

    wakati = MeCab.Tagger("-Owakati")

    def tokenize(text: str) -> List[str]:
        return wakati.parse(text).split()

    with open('data/cas_tokenize.zip', 'rb') as f:
        cas = load_cas_from_zip_file(f)
        mecab_tokenized_cas = tokenize_cas(cas, tokenize)
        for sentence in mecab_tokenized_cas.select(SENTENCE_NS):
            text = sentence.get_covered_text()
            tokens = tokenize(text)
            tokens_in_cas = list(mecab_tokenized_cas.select_covered(TOKEN_NS, sentence))
            assert len(tokens) == len(tokens_in_cas)

