import copy
from typing import Callable, List
from dkpro_cassis_tools.ns import SENTENCE_NS, TOKEN_NS
from cassis import Cas
from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.magic_transfer import MagicTransfer


def tokenize_cas(cas: Cas, tokenize_fn: Callable[[str], List[str]]) -> Cas:
    cas = copy.deepcopy(cas)

    # Remove tokens
    for token in list(cas.select(TOKEN_NS)):
        cas.remove_annotation(token)

    # Create new tokens
    for sentence in cas.select(SENTENCE_NS):
        text = sentence.get_covered_text()
        tokens = tokenize_fn(text)

        text_sequence = CharSequence.new(text)  # Sequence of chars
        token_sequence = TokenSequence.new(tokens)

        transfer = MagicTransfer(token_sequence, text_sequence)

        for token in token_sequence:
            span = transfer.apply(token)
            if span:
                begin = span.start
                end = span.stop
                annotation = cas.typesystem.get_type(TOKEN_NS)(
                    begin=begin + sentence.begin,
                    end=end + sentence.begin)
                cas.add_annotation(annotation)
    return cas

