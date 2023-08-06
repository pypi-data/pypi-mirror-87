import contextlib
import json
import logging
import os
from typing import Any, Dict
import zipfile

from ncbi.datasets.reports.report_reader import DatasetsReportReader
import ncbi.datasets.v1alpha1.reports.assembly_pb2 as assembly_report_pb2
import ncbi.datasets.v1alpha1.reports.gene_pb2 as gene_report_pb2

logger = logging.getLogger()


def GetDatasetFromFile(zip_file_or_directory, dataset_type: str):  # pylint:disable=invalid-name
    if dataset_type == 'ASSEMBLY':
        return AssemblyDataset(zip_file_or_directory)
    elif dataset_type == 'GENE':
        return GeneDataset(zip_file_or_directory)
    elif dataset_type == 'VIRUS':
        return VirusDataset(zip_file_or_directory)
    raise ValueError(dataset_type)


def _get_files_of_type(elt: Dict[str, Any], file_type, results):
    if isinstance(elt, dict):
        for k, v in elt.items():
            if k == 'files' and isinstance(v, list):
                results.extend([f['filePath'] for f in v if f['fileType'] == file_type])
            else:
                _get_files_of_type(v, file_type, results)
    elif isinstance(elt, list):
        for v in elt:
            _get_files_of_type(v, file_type, results)


def _get_file_types(elt: Dict[str, Any], results):
    if isinstance(elt, dict):
        for k, v in elt.items():
            if k == 'files' and isinstance(v, list):
                results.update([f['fileType'] for f in v])
            else:
                _get_file_types(v, results)
    elif isinstance(elt, list):
        for v in elt:
            _get_file_types(v, results)


class Dataset():
    """Base class to extract files from datasets package

    Various low-level functions to extract files from a datasets package
    """

    def __init__(self, zipfile_or_directory):
        self.report_reader = DatasetsReportReader()
        # Zip file object - is 'None' if dataset is not stored in a zip file
        self.dataset_zip = None
        # Top-level directory for files. If data is stored in a zip file this is the data
        # directory in the zip file (ncbi_dataset/data), otherwise it's the full data directory path.
        self.dataset_dir = None

        if os.path.isdir(zipfile_or_directory):
            self.dataset_dir = os.path.join(zipfile_or_directory, 'data')
        elif os.path.isfile(zipfile_or_directory):
            try:
                self.dataset_zip = zipfile.ZipFile(zipfile_or_directory)
                self.dataset_dir = 'ncbi_dataset/data'
            except zipfile.BadZipFile as e:
                logger.error('Bad zipfile: %s', e)
        else:
            logger.error('Invalid file or directory %s', zipfile_or_directory)

    # True if Dataset is reading directly from a zip file
    def is_zipped(self):
        return bool(self.dataset_zip)

    # Return top-level data directory
    def get_file_root_dir(self):
        return self.dataset_dir

    # return json catalog from zip file
    def get_catalog(self) -> Dict[str, Any]:
        dataset_catalog: Dict[str, Any]
        catalog_file = self.get_file_content('dataset_catalog.json')
        if catalog_file:
            try:
                dataset_catalog = json.loads(catalog_file)
            except json.JSONDecodeError as e:
                logger.error('Error decoding dataset_catalog file to json: %s', e)
        return dataset_catalog

    # return names of all files of type 'file_type', eg. 'PROTEIN_FASTA'
    def get_file_names_by_type(self, file_type):
        results = []
        catalog = self.get_catalog()
        _get_files_of_type(catalog, file_type, results)
        return results

    # generator to return all files of type 'file_type' along with their names
    def get_files_by_type(self, file_type):
        names = self.get_file_names_by_type(file_type)
        for name in names:
            yield self.get_file_content(name), name

    # generator to return file handles for all files of type 'file_type' along with their names
    def get_file_handles_by_type(self, file_type):
        names = self.get_file_names_by_type(file_type)
        for name in names:
            # yield self.get_file_handle(name), name
            with self.get_file_handle(name) as fh:
                yield fh, name

    # return all file types available in the current dataset
    def get_file_types(self):
        results = set()
        catalog = self.get_catalog()
        _get_file_types(catalog, results)
        return results

    # Return full text of file 'file_name'
    def get_file_content(self, file_name):
        with self.get_file_handle(file_name) as fh:
            if not fh:
                return ''
            return fh.read()

    # Get handle of file using name within dataset directory 'ncbi_dataset/data'.
    # These are the names returned by 'get_file_names_by_type'
    @contextlib.contextmanager
    def get_file_handle(self, file_name):
        if self.dataset_zip:
            try:
                zinfo = self.dataset_zip.getinfo(os.path.join(self.dataset_dir, file_name))
                # return io.TextIOWrapper(self.dataset_zip.open(zinfo))
                with self.dataset_zip.open(zinfo)as fh:
                    yield fh
            except KeyError as e:
                logger.error('File %s not found in zipfile: %s', file_name, e)
        elif self.dataset_dir:
            file_path = os.path.join(self.dataset_dir, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r') as fh:
                    yield fh
            else:
                logger.error('File not found in datasets directory: %s', file_path)
        else:
            logger.error('Dataset not available - unable to load: %s', file_name)


class AssemblyDataset(Dataset):
    """Retrieve Assembly reports

    Methods to read Assembly reports
    """

    # returns protobuf for single report
    def get_report(self, report_file):
        """Retrieve assembly reports

        Returns:
          A single AssemblyDataReport protobuf object
        """

        with self.get_file_handle(report_file) as fh:
            return self.report_reader.assembly_report_from_file(fh)
        return assembly_report_pb2.AssemblyDataReport()

    def get_reports(self):
        """Retrieve assembly reports

        Returns:
          Yields a set of AssemblyDataReport protobuf object
        """

        report_files = self.get_file_names_by_type('DATA_REPORT')
        for file in report_files:
            with self.get_file_handle(file) as fh:
                yield self.report_reader.assembly_report_from_file(fh)
        return assembly_report_pb2.AssemblyDataReport()


class GeneDataset(Dataset):
    """Retrieve Gene reports

    Methods to read Gene reports
    """

    def get_report(self):
        """Retrieve a gene report object

        Returns:
          A single GeneDescriptors protobuf object
        """

        report_files = self.get_file_names_by_type('DATA_REPORT')
        # gene datasets also have '.csv' files of type DATA_REPORT, but these
        # can't be converted to protobuf
        file = next(file for file in report_files if file.endswith('yaml'))
        if file:
            with self.get_file_handle(file) as fh:
                return self.report_reader.gene_report_from_file(fh)
        return gene_report_pb2.GeneDescriptors()


class VirusDataset(Dataset):
    """Retrieve Virus reports

    Methods to read Virus reports
    """

    def get_report_assemblies(self):
        """Retrieve virus assembly objects

        Returns:
          Yields a set of virus assembly report protobuf objects
        """
        report_files = self.get_file_names_by_type('DATA_REPORT')
        if report_files:
            with self.get_file_handle(report_files[0]) as fh:
                for virus_assm_pb in self.report_reader.read_virus_report(fh):
                    yield virus_assm_pb
