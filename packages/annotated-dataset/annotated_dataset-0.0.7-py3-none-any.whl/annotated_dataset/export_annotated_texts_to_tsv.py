from typing import List
from annotated_dataset.annotated_text import AnnotatedText
from web_anno_tsv.web_anno_tsv import AnnotatedSentence, Annotation, Span, open_web_anno_tsv


def export_annotated_texts_to_tsv(
        annotated_texts: List[AnnotatedText],
        file: str):

    sentences = []
    for annotated_text in annotated_texts:
        tokens = [Span(
            text=annotated_text.text[token.start: token.stop],
            start=token.start,
            stop=token.stop,
            is_token=True
        ) for token in annotated_text.tokens]
        annotations = [Annotation(
            label=a.label,
            start=a.start,
            stop=a.stop,
            text=annotated_text.text[a.start: a.stop]) for a in annotated_text.annotations]

        sentence = AnnotatedSentence(
            text=annotated_text.text,
            tokens=tokens,
            annotations=annotations
        )
        sentences.append(sentence)

    with open_web_anno_tsv(file, 'w') as f:
        for sentence in sentences:
            f.write(sentence)


