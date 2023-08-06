from typing import List
from annotated_dataset.annotated_text import AnnotatedText
from cassis import Cas
from dkpro_cassis_tools import TOKEN_NS, SENTENCE_NS, NAMED_ENTITY_NS
from dkpro_cassis_tools import dump_cas_to_zip_file


def export_annotated_texts_to_xmi(annotated_texts: List[AnnotatedText], type_system, file: str):
    cas = Cas(typesystem=type_system)

    current_start = 0
    starts = []
    sofa_string = ''

    # Create sofa string
    for annotated_text in annotated_texts:
        starts.append(current_start)
        text = annotated_text.text
        if not text.endswith('\n'):
            text += '\n'
        sofa_string += text
        current_start += len(text)

    cas.sofa_string = sofa_string

    # Tokens
    for annotated_text, start in zip(annotated_texts, starts):
        for token in annotated_text.tokens:
            annotation = cas.typesystem.get_type(TOKEN_NS)(
                begin=start + token.start,
                end=start + token.stop)
            cas.add_annotation(annotation)

    # Sentences
    for annotated_text, start in zip(annotated_texts, starts):
        annotation = cas.typesystem.get_type(SENTENCE_NS)(
            begin=start,
            end=start + len(annotated_text.text))
        cas.add_annotation(annotation)

    # Annotations
    for annotated_text, start in zip(annotated_texts, starts):
        for annotation in annotated_text.annotations:
            annotation = cas.typesystem.get_type(NAMED_ENTITY_NS)(
                value=annotation.label,
                begin=start + annotation.start,
                end=start + annotation.stop)
            cas.add_annotation(annotation)

    # write
    with open(file, 'wb') as f:
        dump_cas_to_zip_file(cas, f)