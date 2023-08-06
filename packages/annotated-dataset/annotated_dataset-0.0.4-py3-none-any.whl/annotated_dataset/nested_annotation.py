from typing import List
from dataclasses import dataclass, field


@dataclass
class NestedAnnotation:
    text: str
    label: str
    start: int
    stop: int
    children: List["NestedAnnotation"] = field(default_factory=list)

    def debug(self, level: int = 0, lines=None):
        if level == 0:
            lines = list()
            lines.append(f'Annotated text: {self.text}')
        indent = '\t'*level
        lines.append(f'{indent}{self.label} [{self.start}:{self.stop}]')
        for child in self.children:
            child.debug(level+1, lines)
        if level == 0:
            return "\n".join(lines)


def iterate(nested_annotation: NestedAnnotation, yield_annotation=False):
    if yield_annotation:
        yield nested_annotation
    for child in nested_annotation.children:
        yield from iterate(child, True)
