from typing import Callable
from annotated_dataset.annotation_schema import AnnotationSchema
from annotated_dataset.nested_annotation import NestedAnnotation
from annotated_dataset.annotated_text import AnnotatedText
from annotated_dataset.nested_annotation import iterate
from annotated_dataset.annotated_text_validation_error_report import AnnotatedTextValidationErrorReport


class ValidatorBase:
    def __init__(self, annotation_schema: AnnotationSchema):
        self.annotation_schema = annotation_schema

    def validate_annotated_text(self, annotated_text: AnnotatedText) -> AnnotatedTextValidationErrorReport:
        error_report = AnnotatedTextValidationErrorReport(annotated_text)
        try:
            # Check annotations offsets
            for annotation in annotated_text.annotations:
                with error_report.catch_assertion_error(raise_error=True):
                    assert annotation.start >= 0, 'Annotation start < 0'

                with error_report.catch_assertion_error(raise_error=True):
                    assert annotation.stop <= len(annotated_text.text), 'Annotation stop > len(sentence)'

            # Check labels
            for annotation in annotated_text.annotations:
                with error_report.catch_assertion_error():
                    assert self.annotation_schema.schema.has_node(annotation.label),\
                        f"Invalid label {annotation.label}"

            # Check hierarchy
            nested = self.annotation_schema.nest_annotations(annotated_text)
            self.annotation_schema.valid_children(nested, error_report)

            # Check validator
            for nest_annotation in iterate(nested):
                self.validate_nested_annotation(nest_annotation, error_report)

        except AssertionError:
            pass

        return error_report

    def validate_nested_annotation(self, annotation: NestedAnnotation, error_report: AnnotatedTextValidationErrorReport):
        raise ValueError('Should be implemented')