from typing import List
from contextlib import contextmanager
from annotated_dataset.annotated_text import AnnotatedText
import enum


class ErrorType(enum.Enum):
    Error = 1
    Warning = 2


class AnnotationError:
    def __init__(self, error_type: ErrorType, message):
        self.type = error_type
        self.message = message

    def __repr__(self):
        return f'{str(self.type)}: {self.message}'


class AnnotatedTextValidationErrorReport:
    def __init__(self, annotated_text: AnnotatedText):
        self.annotated_text = annotated_text
        self.errors: List[AnnotationError] = []

    @contextmanager
    def catch_assertion_error(self, error_type: ErrorType = ErrorType.Error, raise_error=False):
        try:
            yield
        except AssertionError as e:
            self.errors.append(AnnotationError(error_type, str(e)))
            if raise_error:
                raise
