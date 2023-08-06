from typing import List
from annotated_dataset.annotated_text import AnnotatedText


class AnnotatedResourceBase:
    def __init__(self, resource_id: str):
        self.resource_id = resource_id

    def get_annotated_texts(self) -> List[AnnotatedText]:
        raise ValueError("get_annotated_texts should be implemented")
