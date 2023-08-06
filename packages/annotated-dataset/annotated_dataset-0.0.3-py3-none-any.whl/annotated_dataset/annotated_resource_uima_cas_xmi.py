from typing import List
from annotated_dataset.annotated_text import AnnotatedText, AnnotatedTextToken
from annotated_dataset.annotation import Annotation
from annotated_dataset.annotated_resource_base import AnnotatedResourceBase
from dkpro_cassis_tools import load_cas_from_zip_file, \
    restore_cas_segmentation_by_newline, \
    SENTENCE_NS, \
    NAMED_ENTITY_NS, \
    TOKEN_NS


class AnnotatedResourceUimaCasXmi(AnnotatedResourceBase):
    def __init__(self, path, restore_segmentation_by_newline=False, resource_id=None):
        self.path = path
        self.restore_segmentation_by_newline = restore_segmentation_by_newline
        if not resource_id:
            resource_id = path

        super().__init__(resource_id)

        # Open Resource
        with open(self.path, 'rb') as f:
            self.cas, self.type_system = load_cas_from_zip_file(f, return_type_system=True)

        # Extract annotated texts
        self.annotated_texts = []
        if self.restore_segmentation_by_newline:
            self.cas = restore_cas_segmentation_by_newline(self.cas)
        for i, sentence in enumerate(self.cas.select(SENTENCE_NS)):
            # Text
            text = sentence.get_covered_text()

            # Annotations
            annotations = []
            for a in self.cas.select_covered(NAMED_ENTITY_NS, sentence):
                annotations.append(Annotation(
                    label=a.value,
                    start=a.begin - sentence.begin,
                    stop=a.end - sentence.begin

                ))

            # Tokens
            tokens = []
            for token in self.cas.select_covered(TOKEN_NS, sentence):
                tokens.append(AnnotatedTextToken(
                    start=token.begin-sentence.begin,
                    stop=token.end-sentence.begin
                ))
            not_spaces = set()
            for token in tokens:
                for j in range(token.start, token.stop):
                    not_spaces.add(j)
            for j, char in enumerate(text):
                if j not in not_spaces:
                    if not text[j].isspace():
                        # TODO
                        print("Tokenizing Error")

            self.annotated_texts.append(AnnotatedText(
                text=text,
                annotations=annotations,
                resource_id=self.resource_id,
                resource_index=i + 1,
                tokens=tokens
            ))

    def get_annotated_texts(self) -> List[AnnotatedText]:
        return self.annotated_texts

