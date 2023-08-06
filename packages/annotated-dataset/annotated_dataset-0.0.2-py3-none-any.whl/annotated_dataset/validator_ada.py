from annotated_dataset.annotation_schema import AnnotationSchema
from annotated_dataset.validator_base import ValidatorBase
from networkx import DiGraph
from annotated_dataset.nested_annotation import NestedAnnotation
from annotated_dataset.annotated_text_validation_error_report import AnnotatedTextValidationErrorReport


class ValidatorAda(ValidatorBase):
    def __init__(self):
        # Create the annotation_schema
        g = DiGraph()
        g.add_node('ROOT')
        g.add_edge('ROOT', 'PERSON')
        g.add_edge('ROOT', 'LOCATION')
        g.add_edge('ROOT', 'DATE')
        g.add_edge('ROOT', 'AMOUNT')
        g.add_edge('ROOT', 'EMAIL')
        g.add_edge('ROOT', 'PHONE-NUMBER')
        g.add_edge('ROOT', 'URL')
        g.add_edge('ROOT', 'ORGANISATION')
        g.add_edge('ROOT', 'TIME')
        g.add_edge('ROOT', 'ID')
        g.add_edge('ROOT', 'ORG')
        g.add_edge('PERSON', 'person-title')
        g.add_edge('PERSON', 'person-given-name')
        g.add_edge('PERSON', 'person-given-name-male')
        g.add_edge('PERSON', 'person-given-name-female')
        g.add_edge('PERSON', 'person-family-name')
        g.add_edge('PERSON', 'person-family-name-male')
        g.add_edge('PERSON', 'person-family-name-female')
        g.add_edge('LOCATION', 'location-place')
        g.add_edge('LOCATION', 'location-street')
        g.add_edge('LOCATION', 'location-postcode')
        g.add_edge('LOCATION', 'location-city')
        g.add_edge('LOCATION', 'location-territory')
        g.add_edge('DATE', 'date-day')
        g.add_edge('DATE', 'date-day-of-week')
        g.add_edge('DATE', 'date-month')
        g.add_edge('DATE', 'date-year')
        g.add_edge('DATE', 'date-standard-abbreviation')
        g.add_edge('DATE', 'date-calendar-event')
        g.add_edge('AMOUNT', 'amount-unit')
        g.add_edge('AMOUNT', 'amount-value')
        g.add_edge('location-place', 'PERSON')
        g.add_edge('ORG', 'PERSON')

        annotation_schema = AnnotationSchema(g)
        super().__init__(annotation_schema)

    def validate_nested_annotation(self, annotation: NestedAnnotation, error_report: AnnotatedTextValidationErrorReport) -> None:
        # Label
        if annotation.label in {'PERSON', 'LOCATION', 'DATE', 'AMOUNT'}:
            with error_report.catch_assertion_error():
                assert len(annotation.children) >= 1, \
                    f"`{annotation.label}` is expected to have at least one child"
            if annotation.label == 'AMOUNT':
                has_value = False
                for sub_annotation in annotation.children:
                    if sub_annotation.label == 'amount-value':
                        has_value = True
                        break
                with error_report.catch_assertion_error():
                    assert has_value, f'AMOUNT is expected to have a sub-annotation amount-value'









