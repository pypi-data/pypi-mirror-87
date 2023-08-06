from typing import List, Tuple, Optional
from dataclasses import dataclass
from annotated_dataset.annotation import Annotation


@dataclass
class AnnotatedTextToken:
    start: int
    stop: int


@dataclass
class AnnotatedText:
    text: str
    annotations: List[Annotation]
    resource_id: Optional[str] = None
    resource_index: Optional[int] = None
    tokens: Optional[List[AnnotatedTextToken]] = None

    def get_annotation_signatures(self):
        s = set()
        for annotation in self.annotations:
            s.add(annotation.signature())
        return s

    def get_id(self) -> Tuple[Optional[str], Optional[int]]:
        return self.resource_id, self.resource_index


@dataclass
class AnnotatedTextToken:
    start: int
    stop: int
