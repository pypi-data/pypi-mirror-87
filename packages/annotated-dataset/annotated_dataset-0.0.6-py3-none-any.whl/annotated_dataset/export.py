import tempfile
from annotated_dataset.annotated_dataset import AnnotatedDataset
from annotated_dataset.validator_mapa import ValidatorMapa
from annotated_dataset.inception_project import InceptionProject
from annotated_dataset.annotated_dataset import GoldCorpusPreferredResources
from pathlib import Path
import logging


def export(config):
    # Extract resource
    resources = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for project_config in config['inception_projects']:
            # Create the project
            project = InceptionProject.create_from_remote(
                project_config['name'],
                project_config['inception_client'],
                str(tmp)
            )

        # Extract resources
        resources.extend(project.extract_resources(
            restore_segmentation_by_newline=project_config['use_segmentation_by_newline']))

    # Create dataset
    dataset_name = config['dataset_name']
    dataset = AnnotatedDataset(
        dataset_name,
        resources)

    # Create validator
    validator = ValidatorMapa()

    # Create gold_corpus_preferred_resources
    gold_corpus_preferred_resources = GoldCorpusPreferredResources(
        config['gold_corpus_preferred_resources']
    )

    # Create bundle
    bundle_dir = Path(config['export_dir']).joinpath('export_' + dataset_name.lower())
    dataset.create_bundle(
        str(bundle_dir),
        validator,
        gold_corpus_preferred_resources
    )




