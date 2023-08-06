from typing import NamedTuple, List, Tuple, Optional
from pathlib import Path
from annotated_dataset.annotated_resource_base import AnnotatedResourceBase
from annotated_dataset.annotated_text import AnnotatedText
from annotated_dataset.validator_base import ValidatorBase
from annotated_dataset.annotation_schema import AnnotationSchema
from collections import defaultdict
from bokeh.io import output_file, show, save
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import d3
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Paragraph, Div
from annotated_dataset.annotated_text_validation_error_report import AnnotationError
from itertools import groupby
from annotated_dataset.export_annotated_texts_to_xmi import export_annotated_texts_to_xmi
import logging


class GoldCorpusGroup:
    def __init__(self, annotated_texts: List[AnnotatedText]):
        self.annotated_texts = annotated_texts

    def get_annotated_texts(self):
        return self.annotated_texts

    def get_annotated_text_ids(self) -> List[Tuple[Optional[str], Optional[int]]]:
        return list(map(lambda a: a.get_id(), self.annotated_texts))


class GoldCorpus:
    def __init__(self, groups: List[GoldCorpusGroup]):
        self.groups = groups
        self.index = dict()
        for group in self.groups:
            for annotated_text_id in group.get_annotated_text_ids():
                self.index[annotated_text_id] = group

    @staticmethod
    def create_from_dataset(dataset: "AnnotatedDataset"):
        groups = []
        annotated_texts = list()
        for resource in dataset.resources:
            annotated_texts.extend(resource.get_annotated_texts())
        sorted_by_text = sorted(annotated_texts, key=lambda annotated_text: annotated_text.text)

        for _, group in groupby(sorted_by_text, key=lambda annotated_text: annotated_text.text):
            group = list(group)
            if len(group) > 1:
                groups.append(GoldCorpusGroup(group))
        return GoldCorpus(groups)

    def get_groups(self) -> List[GoldCorpusGroup]:
        return self.groups

    def is_gold(self, annotated_text: AnnotatedText) -> bool:
        return annotated_text.get_id() in self.index

    def get_group(self, annotated_text: AnnotatedText):
        annotated_text_id = annotated_text.get_id()
        if annotated_text_id in self.index:
            return self.index[annotated_text_id]
        return None


class GoldCorpusPreferredResources:
    def __init__(self, preferred_resources: List[str]):
        self.preferred_resources = preferred_resources

    def get_preferred_in_group(self, group: GoldCorpusGroup):
        for annotated_text in group.get_annotated_texts():
            for preferred_resource in self.preferred_resources:
                if annotated_text.resource_id == preferred_resource:
                    return annotated_text

        for annotated_text in group.get_annotated_texts():
            for preferred_resource in self.preferred_resources:
                if annotated_text.resource_id.find(preferred_resource):
                    return annotated_text

        return group.get_annotated_texts()[0]


class ValidationError(NamedTuple):
    annotated_text: AnnotatedText
    error: AnnotationError


class AnnotatedDataset:
    def __init__(self, name: str, annotated_resources: List[AnnotatedResourceBase]):
        self.name = name
        self.resources = annotated_resources
        self.gold_corpus: GoldCorpus = GoldCorpus.create_from_dataset(self)

    def validate(self, validator: ValidatorBase):
        errors = []
        for resource in self.resources:
            annotated_texts = resource.get_annotated_texts()
            for i, annotated_text in enumerate(annotated_texts):
                report = validator.validate_annotated_text(annotated_text)
                for error in report.errors:
                    errors.append(ValidationError(
                        annotated_text=annotated_text,
                        error=error
                    ))
        return errors

    def get_stats(self, annotation_schema: AnnotationSchema):
        stats = defaultdict(dict)
        for category, labels in annotation_schema.get_labels_by_category().items():
            for label in labels:
                stats[category][label] = 0
        for resource in self.resources:
            annotated_texts = resource.get_annotated_texts()
            for annotated_text in annotated_texts:
                for annotation in annotated_text.annotations:
                    if annotation_schema.is_valid_label(annotation.label):
                        category = annotation_schema.get_label_category(annotation.label)
                        stats[category][annotation.label] += 1
        return stats

    def create_report(self, validator: ValidatorBase, file="report.txt"):
        widgets = list()

        # Main title
        widgets.append(Div(text=f'<h1>Dataset analysis for {self.name}</h1>'))

        # Resource widget
        widgets.extend(self._get_resource_widget())

        # Annotation label distribution widget
        widgets.extend(self._get_annotation_label_distribution_widget(validator))

        # Annotation errors widget
        widgets.extend(self._get_annotation_error_widget(validator))

        # Gold
        widgets.extend(self._get_gold_widget())

        # Save
        output_file(file)
        save(column(*widgets), file)

    def _get_resource_widget(self):
        resources = []
        num_annotated_texts = []
        num_annotations = []

        for resource in self.resources:
            resources.append(resource.resource_id)
            annotated_texts = resource.get_annotated_texts()
            num_annotated_texts.append(len(annotated_texts))
            num_annotations.append(sum([len(at.annotations) for at in annotated_texts]))

        data = dict(
            resource=resources,
            sentences=num_annotated_texts,
            annotations=num_annotations
        )
        source = ColumnDataSource(data)

        columns = [
            TableColumn(field="resource", title="Resource", width=500),
            TableColumn(field="sentences", title="Sentences", width=70),
            TableColumn(field="annotations", title="Annotations", width=880),
        ]

        data_table = DataTable(
            source=source,
            columns=columns,
            min_height=100,
            max_height=1000,
            height=(len(resources) + 1) * 28,
            width=1500,
            autosize_mode="none",
            sizing_mode="scale_both")

        return [Div(text='<h2>Resources</h2>'), data_table ]

    def _get_annotation_label_distribution_widget(self, validator):
        stats = self.get_stats(validator.annotation_schema)

        labels = []
        occurrences = []
        categories = []
        max_value = 0
        category_and_label = []
        for category, stats_by_label in stats.items():
            if category != 'root':
                categories.append(category)
                for label, num in stats_by_label.items():
                    label = f"{label} ({num})"
                    labels.append(label)
                    occurrences.append(num)
                    if num > max_value:
                        max_value = num
                    category_and_label.append((category, label))

        palette = d3['Category20'][len(categories)]

        source = ColumnDataSource(data=dict(category_and_label=category_and_label, occurrences=occurrences))

        tag_set_graph = figure(
            x_range=FactorRange(*category_and_label),
            plot_width=1500,
            plot_height=600,
            title="Dataset",
            toolbar_location=None,
            tools="")

        tag_set_graph.vbar(
            x='category_and_label',
            top='occurrences',
            width=0.9,
            source=source,
            line_width=0,
            line_color="white",
            fill_color=factor_cmap('category_and_label', palette=palette, factors=categories, start=0, end=1))

        tag_set_graph.y_range.start = 0
        tag_set_graph.x_range.range_padding = 0.1
        tag_set_graph.xaxis.major_label_orientation = 'vertical'
        tag_set_graph.xaxis.major_label_text_font_size = "12px"
        tag_set_graph.xaxis.group_label_orientation = 'vertical'
        tag_set_graph.xaxis.group_text_font_size = "12px"

        return [Div(text=f'<h2>Tag distribution</h2>'), tag_set_graph]

    def _get_annotation_error_widget(self, validator):
        widgets = [Div(text=f'<h2>Annotation errors</h2>')]

        # Validate dataset
        for resource, errors in groupby(self.validate(validator), key=lambda e: e.annotated_text.resource_id):
            widgets.append(Paragraph(text=f"Error in {resource}"))
            line_numbers = []
            texts = []
            error_types = []
            error_messages = []
            for error in errors:
                line_numbers.append(error.annotated_text.resource_index)
                texts.append(error.annotated_text.text)
                error_types.append(str(error.error.type).replace('ErrorType.', ''))
                error_messages.append(error.error.message)

            data = dict(
                line_numbers=line_numbers,
                texts=texts,
                error_types=error_types,
                error_messages=error_messages
            )
            source = ColumnDataSource(data)

            columns = [
                TableColumn(field="line_numbers", title="Line nº", width=50),
                TableColumn(field="error_types", title="Error type", width=70),
                TableColumn(field="error_messages", title="Error", width=400),
                TableColumn(field="texts", title="Text", width=940)
            ]

            data_table = DataTable(
                source=source,
                columns=columns,
                min_height=100,
                max_height=1000,
                height=(len(line_numbers) + 1) * 28,
                width=1500,
                autosize_mode="none",
                sizing_mode="scale_both")

            widgets.append(data_table)

        return widgets

    def _get_gold_widget(self):
        widgets = [Div(text='<h2>Gold annotations</h2>')]

        # Compare annotations
        column_groups = []
        column_resource_ids = []
        column_resource_indices = []
        column_diffs = []
        column_texts = []

        compare_id = 0
        for group in self.gold_corpus.get_groups():
            annotation_signatures_in_annotated_texts = []
            for annotated_text in group.get_annotated_texts():
                annotation_signatures_in_annotated_texts.append(
                    annotated_text.get_annotation_signatures())
            common_annotations_signatures = set.intersection(*annotation_signatures_in_annotated_texts)

            has_diff = False
            diff_in_annotated_texts = []
            for annotation_signatures_in_annotated_text in annotation_signatures_in_annotated_texts:
                diffs = []
                for signature in annotation_signatures_in_annotated_text:
                    if signature not in common_annotations_signatures:
                        has_diff = True
                        diffs.append(signature)
                diff_in_annotated_texts.append(diffs)

            if has_diff:
                for annotated_text, diffs in zip(
                        group.get_annotated_texts(),
                        diff_in_annotated_texts):
                    column_groups.append(f'#{compare_id}')
                    column_resource_ids.append(annotated_text.resource_id)
                    column_resource_indices.append(annotated_text.resource_index)
                    column_texts.append(annotated_text.text)
                    column_diffs.append(", ".join([f'{d[0]}[{d[1]}:{d[2]}]' for d in diffs]))
                compare_id += 1

        data = dict(
            group=column_groups,
            resource_ids=column_resource_ids,
            resource_indices=column_resource_indices,
            texts=column_texts,
            diffs=column_diffs
        )
        source = ColumnDataSource(data)

        columns = [
            TableColumn(field="group", title="Group", width=50),
            TableColumn(field="resource_ids", title="Resource", width=250),
            TableColumn(field="resource_indices", title="Line nº", width=50),
            TableColumn(field="diffs", title="Diff", width=400),
            TableColumn(field="texts", title="Text", width=400)
        ]

        data_table = DataTable(
            source=source,
            columns=columns,
            min_height=100,
            max_height=1000,
            height=(len(column_groups) + 1) * 28,
            width=1500,
            autosize_mode="none",
            sizing_mode="scale_both")

        widgets.append(data_table)

        return widgets

    def get_gold_and_not_gold(self, gold_corpus_preferred_resources: GoldCorpusPreferredResources):
        gold = list()
        not_gold = list()

        for resource in self.resources:
            for annotated_text in resource.get_annotated_texts():
                if self.gold_corpus.is_gold(annotated_text):
                    gold_group = self.gold_corpus.get_group(annotated_text)
                    preferred = gold_corpus_preferred_resources.get_preferred_in_group(gold_group)
                    if preferred == annotated_text:
                        gold.append(annotated_text)
                else:
                    not_gold.append(annotated_text)
        return gold, not_gold

    def create_bundle(self,
                      bundle_dir: str,
                      validator: ValidatorBase,
                      gold_corpus_preferred_resources: GoldCorpusPreferredResources
                      ):

        if not self.resources:
            raise ValueError('No resource found')

        bundle_dir = Path(bundle_dir.replace(' ', '_'))
        bundle_dir.mkdir()

        # Create report

        report_file = bundle_dir.joinpath(f'{bundle_dir.name}_report.html')
        self.create_report(validator, str(report_file))

        # Export
        logging.info('Create report')
        type_system = self.resources[0].type_system
        gold, not_gold = self.get_gold_and_not_gold(gold_corpus_preferred_resources)
        logging.info(' ---> done')

        logging.info('Export data')
        data_file = bundle_dir.joinpath(f'{bundle_dir.name}_data.zip')
        export_annotated_texts_to_xmi(
            not_gold, type_system, data_file, xmi_file=f'{bundle_dir.name}_data.xmi')
        logging.info(' ---> done')

        logging.info('Export gold')
        gold_file = bundle_dir.joinpath(f'{bundle_dir.name}_data_gold.zip')
        export_annotated_texts_to_xmi(
            gold, type_system, gold_file, xmi_file=f'{bundle_dir.name}_data_gold.xmi')
        logging.info(' ---> done')

        logging.info(f'Exportation finished `{bundle_dir}`', )