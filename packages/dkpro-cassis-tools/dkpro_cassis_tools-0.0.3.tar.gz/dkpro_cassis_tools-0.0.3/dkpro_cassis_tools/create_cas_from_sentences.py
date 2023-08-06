from typing import List, Tuple
from cassis import Cas
from cassis.typesystem import FeatureStructure
from dkpro_cassis_tools.ns import TOKEN_NS, SENTENCE_NS, NAMED_ENTITY_NS


def create_cas_from_sentences(sentences: List[Tuple[Cas, FeatureStructure]], type_system=None) -> Cas:
    """
    :param type_system: The type system of the new cas and all the cas in the sentences list
    :param sentences: a list of tuple of 2 elements: a cas and a sentence annotation assiociated with this cas)
    :return: a new Cas object
    """

    if not sentences:
        raise ValueError('Sentence list is empty')

    if type_system is None:
        type_system = sentences[0][0].typesystem

    # Create text for new cas
    text = ''
    starts = []
    for i, (cas, sentence_annotation) in enumerate(sentences):
        sentence = sentence_annotation.get_covered_text()
        if i != 0:
            text += '\n'
        starts.append(len(text))
        text += sentence

    # Create new cas
    new_cas = Cas(type_system)
    new_cas.sofa_string = text

    # Transfer annotations
    for i, (cas, sentence_annotation) in enumerate(sentences):
        sentence = sentence_annotation.get_covered_text()

        # Sentence annotation
        new_cas.add_annotation(
            annotation=type_system.get_type(SENTENCE_NS)(
                begin=starts[i],
                end=+ starts[i] + len(sentence)))

        # Token annotation
        for token in cas.select_covered(TOKEN_NS, sentence_annotation):
            begin = token.begin - sentence_annotation.begin + starts[i]
            end = token.end - sentence_annotation.begin + starts[i]
            new_cas.add_annotation(
                annotation=type_system.get_type(TOKEN_NS)(
                    begin=begin,
                    end=end
                    ))
            assert text[begin:end] == token.get_covered_text()

        # Entity annotation
        for entity in cas.select_covered(NAMED_ENTITY_NS, sentence_annotation):
            begin = entity.begin - sentence_annotation.begin + starts[i]
            end = entity.end - sentence_annotation.begin + starts[i]
            new_cas.add_annotation(
                annotation=type_system.get_type(NAMED_ENTITY_NS)(
                    begin=begin,
                    end=end,
                    value=entity.value))
            assert text[begin:end] == entity.get_covered_text()

    return new_cas

