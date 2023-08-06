from typing import List
from pathlib import Path
import zipfile
from pycaprio import Pycaprio
from pycaprio.mappings import InceptionFormat
from annotated_dataset.annotated_resource_uima_cas_xmi import AnnotatedResourceUimaCasXmi
from annotated_dataset.annotated_resource_base import AnnotatedResourceBase
import logging


class ProjectNotFound(Exception):
    def __init__(self, project_name: str, inception_client: Pycaprio):
        super().__init__(f'Project `{project_name}` in {inception_client} ')


class InceptionProject:
    def __init__(self, path):
        self.path = Path(path)
        if not self.path.is_dir():
            raise ValueError(f'Dir `{path}` not found')

    def extract_resources(self, restore_segmentation_by_newline=False) -> List[AnnotatedResourceBase]:
        resources = []
        for path in sorted(self.path.glob('annotation/*/*.zip')):
            resource_id = self.path.name + '/' + path.parent.name
            resources.append(AnnotatedResourceUimaCasXmi(
                str(path),
                resource_id=resource_id,
                restore_segmentation_by_newline=restore_segmentation_by_newline))
        return resources

    @staticmethod
    def create_from_remote(project_name: str, inception_client: Pycaprio, location: str):
        # Get project id
        project_id = None
        projects = inception_client.api.projects()
        for project in projects:
            if project.project_name == project_name:
                project_id = project.project_id
                break

        if project_id is None:
            raise ProjectNotFound(project_name, inception_client)

        # Download project zip
        logging.info(f'Download project `{project_name}`')
        zip_file = Path(location).joinpath(f"{project_name}.zip")
        with open(zip_file, 'wb') as z:
            zip_content = inception_client.api.export_project(
                project_id,
                project_format=InceptionFormat.XMI)
            z.write(zip_content)

        # Unzip project
        project_dir = Path(location).joinpath(project_name)
        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(project_dir)

        # Create the project
        project = InceptionProject(str(Path(location).joinpath(project_name)))
        logging.info(f' ---> Done')

        return project

