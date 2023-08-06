from networkx import DiGraph
from annotated_dataset.annotation_schema import AnnotationSchema
from annotated_dataset.validator_base import ValidatorBase
from annotated_dataset.nested_annotation import NestedAnnotation
from annotated_dataset.annotated_text_validation_error_report import AnnotatedTextValidationErrorReport
from annotated_dataset.find_email import find_email
from annotated_dataset.find_url import find_url


class ValidatorMapa(ValidatorBase):
    def __init__(self):
        # Create the annotation_schema
        g = DiGraph()

        # Root
        g.add_node('ROOT', category='root')

        # Amount
        g.add_edge('ROOT', 'AMOUNT')
        g.nodes['AMOUNT']['category'] = 'amount'
        for n in [
            'unit',
            'value',
            'other:amount',
            'unresolved:amount'
        ]:
            g.add_edge('AMOUNT', n)
            g.nodes[n]['category'] = 'amount'

        # Date
        g.add_edge('ROOT', 'DATE')
        g.nodes['DATE']['category'] = 'date'
        for n in [
            'day',
            'day of week',
            'month',
            'year',
            'standard abbreviation',
            'calendar event',
            'other:date',
            'unresolved:date'
        ]:
            g.add_edge('DATE', n)
            g.nodes[n]['category'] = 'date'

        g.add_edge('ROOT', 'TIME')
        g.nodes['TIME']['category'] = 'time'

        # Person
        g.add_edge('ROOT', 'PERSON')
        g.nodes['PERSON']['category'] = 'person'
        for n in [
            'title',
            'given name',
            'given name - male',
            'given name - female',
            'family name',
            'family name - male',
            'family name - female',
            'initial name',
            'other:name',
            'unresolved:name',
            'ROLE',
            'PROFESSION'
        ]:
            g.add_edge('PERSON', n)
            g.nodes[n]['category'] = 'person'

        # Address
        g.add_edge('ROOT', 'ADDRESS')
        g.nodes['ADDRESS']['category'] = 'address'
        for n in [
            'street',
            'building',
            'city',
            'place',
            'postcode',
            'territory',
            'country',
            'other:address',
            'unresolved:address'
        ]:
            g.add_edge('ADDRESS', n)
            g.nodes[n]['category'] = 'address'

        # Personal information
        for n in [
            'AGE',
            'ETHNIC CATEGORY',
            'MARITAL STATUS',
            'NATIONALITY',
            'FINANCIAL'
        ]:
            g.add_edge('ROOT', n)
            g.nodes[n]['category'] = 'personal data'

        # Organisation
        g.add_edge('ROOT', 'ORGANISATION')
        g.nodes['ORGANISATION']['category'] = 'organisation'

        # ID
        for n in [
            'id document number',
            'health insurance number',
            'social security number',
            'other:id',
            'unresolved:id',
            'medical record number'
        ]:
            g.add_edge('ROOT', n)
            g.nodes[n]['category'] = 'id'

        # Contact
        for n in [
            'email',
            'telephone number',
            'url',
            'other:contact',
            'unresolved:contact'
        ]:
            g.add_edge('ROOT', n)
            g.nodes[n]['category'] = 'contact'

        # Vehicles
        for n in [
            'build year',
            'colour',
            'licence plate number',
            'model',
            'other:vehicle',
            'type'
        ]:
            g.add_edge('ROOT', n)
            g.nodes[n]['category'] = 'vehicle'

        annotation_schema = AnnotationSchema(g)
        super().__init__(annotation_schema)

    def validate_nested_annotation(self, annotation: NestedAnnotation, error_report: AnnotatedTextValidationErrorReport) -> None:
        # Label
        if annotation.label in {'AMOUNT', 'DATE', 'PERSON', 'ADDRESS'}:
            with error_report.catch_assertion_error():
                assert len(annotation.children) >= 1, \
                    f"{_a(annotation)} is expected to have at least one child"

        if annotation.label == 'AMOUNT':
            has_value = False
            for sub_annotation in annotation.children:
                if sub_annotation.label in {'value',  'other:amount', 'unresolved:amount'}:
                    has_value = True
                    break
            with error_report.catch_assertion_error():
                assert has_value, f'{_a(annotation)} is expected to have a sub-annotation ' \
                                  f'`value` or `other:amount` or `unresolved:amount`'

        elif annotation.label == 'PERSON':
            counts = self._count_sub(annotation)
            num_family_name = counts['family name'] + counts['family name - male'] + counts['family name - female']
            with error_report.catch_assertion_error():
                assert num_family_name in {0, 1}, f"{num_family_name} `family name` has been found"

            num_given_name = counts['given name'] + counts['given name - male'] + counts['given name - female']
            with error_report.catch_assertion_error():
                assert num_given_name in {0, 1}, f"{num_given_name} `given name` has been found"

            with error_report.catch_assertion_error():
                assert num_family_name + num_given_name + counts['initial name'] > 0,\
                    f'{_a(annotation)} should have at least a `family name` , ' \
                    f'a `given name` or an `initials name` tag'

        elif annotation.label == 'email':
            emails = find_email(annotation.text)
            found = False
            for email in emails:
                if email.start == annotation.start and email.stop == annotation.stop:
                    found = True
                    break
            assert found, f'Incorrect `{_a(annotation)}`'

        elif annotation.label == 'url':
            urls = find_url(annotation.text)
            found = False
            for url in urls:
                if url.start == annotation.start and url.stop == annotation.stop:
                    found = True
                    break
            assert found, f'Incorrect `{_a(annotation)}`'

    def _count_sub(self, annotation: NestedAnnotation):
        d = dict()
        for child in self.annotation_schema.get_children(annotation.label):
            d[child] = 0
        for sub_annotation in annotation.children:
            if sub_annotation.label in d:
                d[sub_annotation.label] += 1
        return d


def _a(annotation: NestedAnnotation):
    return f'`{annotation.label}[{annotation.start}:{annotation.stop}]`'
