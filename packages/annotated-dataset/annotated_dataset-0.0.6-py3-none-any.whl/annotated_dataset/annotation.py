from typing import NamedTuple


class Annotation(NamedTuple):
    label: str
    start: int
    stop: int

    def __hash__(self):
        return self.signature()

    def signature(self):
        return self.label, self.start, self.stop

