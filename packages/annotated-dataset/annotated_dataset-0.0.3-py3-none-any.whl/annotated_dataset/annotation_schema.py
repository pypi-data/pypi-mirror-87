from typing import List, Tuple, Dict
from networkx import DiGraph, shortest_path_length, NetworkXNoPath
from annotated_dataset.annotation import Annotation
from annotated_dataset.annotated_text import AnnotatedText
from annotated_dataset.nested_annotation import NestedAnnotation
from annotated_dataset.annotated_text_validation_error_report import AnnotatedTextValidationErrorReport
from _collections import defaultdict


class AnnotationSchema:
    def __init__(self, schema: DiGraph, root_node="ROOT"):
        self.schema = schema
        self.root_node = root_node

        if root_node not in schema:
            raise ValueError(f'Root node `{root_node}` node is missing')

        self.labels: List[str]
        self.shortest_path_from_root: Dict[str, int] = dict()
        for node in schema.nodes:
            if node != root_node:
                try:
                    self.shortest_path_from_root[node] = shortest_path_length(schema, root_node, node)
                except NetworkXNoPath:
                    raise

    def valid_children(self, nested_annotation, error_report: AnnotatedTextValidationErrorReport):
        for child in nested_annotation.children:
            with error_report.catch_assertion_error():
                assert self.schema.has_edge(nested_annotation.label, child.label), \
                    f"Invalid hierarchy {nested_annotation.label}->{child.label}"
            self.valid_children(child, error_report)

    def nest_annotations(self, annotated_text: AnnotatedText) -> NestedAnnotation:
        nested_annotations_index = []
        nested_annotations = []
        sorted_annotations = sorted(annotated_text.annotations, key=self.order_annotations_fn)

        for annotation in sorted_annotations:
            nested_annotation = NestedAnnotation(
                text=annotated_text.text,
                label=annotation.label,
                start=annotation.start,
                stop=annotation.stop
            )

            ancestors = [a for a in nested_annotations_index
                         if a.start <= annotation.start
                         and a.stop >= annotation.stop]
            if not ancestors:
                nested_annotations_index.append(nested_annotation)
                nested_annotations.append(nested_annotation)
            else:
                nested_annotations_index.append(nested_annotation)
                ancestors[-1].children.append(nested_annotation)

        return NestedAnnotation(
            text=annotated_text.text,
            label=self.root_node,
            start=0,
            stop=len(annotated_text.text),
            children=nested_annotations)

    def order_annotations_fn(self, annotation: Annotation) -> Tuple[int, int, int]:
        d = self.shortest_path_from_root[annotation.label] \
            if annotation.label in self.shortest_path_from_root else 1000
        return (
            annotation.start,
            -annotation.stop,
            d)

    def get_children(self, node: str) -> List[str]:
        nodes = []
        for n in self.schema.neighbors(node):
            nodes.append(n)
        return nodes

    def get_labels_by_category(self):
        categories = defaultdict(list)
        for n in self.schema.nodes:
            category = self.schema.nodes[n]['category']
            categories[category].append(n)
        return categories

    def get_label_category(self, label):
        return self.schema.nodes[label]['category']

    def is_valid_label(self, label):
        return label in self.schema.nodes

