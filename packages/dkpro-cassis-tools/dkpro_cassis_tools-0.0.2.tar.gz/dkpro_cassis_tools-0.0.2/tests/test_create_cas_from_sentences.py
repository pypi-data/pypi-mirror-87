from dkpro_cassis_tools.create_cas_from_sentences import create_cas_from_sentences
from dkpro_cassis_tools.load_cas_from_zip_file import load_cas_from_zip_file
from dkpro_cassis_tools import SENTENCE_NS, TOKEN_NS, NAMED_ENTITY_NS


def test_create_cas_from_sentences():
    with open('data/cas.zip', 'rb') as f:
        cas = load_cas_from_zip_file(f)

    sentences = list(cas.select(SENTENCE_NS))

    even_sentences = []
    for i, sentence in enumerate(sentences):
        if i % 2 == 0:
            even_sentences.append((cas, sentence))
    even_cas = create_cas_from_sentences(even_sentences)

    for i, sentence in enumerate(list(even_cas.select(SENTENCE_NS))):
        assert sentence.get_covered_text() == sentences[i*2].get_covered_text()

        # Check token
        for token1, token2 in zip(
                even_cas.select_covered(TOKEN_NS, sentence),
                cas.select_covered(TOKEN_NS, sentences[i*2])):
            assert token1.get_covered_text() == token2.get_covered_text()

        # Check entity
        for entity1, entity2 in zip(
                even_cas.select_covered(NAMED_ENTITY_NS, sentence),
                cas.select_covered(NAMED_ENTITY_NS, sentences[i*2])):
            assert entity1.get_covered_text() == entity2.get_covered_text()
            assert entity1.value == entity2.value


