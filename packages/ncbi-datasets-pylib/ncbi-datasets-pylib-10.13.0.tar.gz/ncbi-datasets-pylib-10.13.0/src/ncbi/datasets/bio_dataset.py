import json
import logging
import os
import re

from Bio.SeqIO.FastaIO import FastaIterator
from google.protobuf.json_format import Parse as JsonPbParse
import yaml

import ncbi.datasets.v1alpha1.catalog_pb2 as catalog_pb2
import ncbi.datasets.v1alpha1.assembly_report_pb2 as assembly_report_pb2

from ncbi.datasets.components.sequence import Sequence
logger = logging.getLogger(__name__)


class Assembly():
    """Assembly class
    """

    def __init__(self, bdbag_dir, assembly):
        self._bdbag_dir = bdbag_dir
        self._assembly = assembly

    def _files_of_type(self, file_type):
        for file in self._assembly.files:
            if file.file_type == file_type:
                yield file.file_path

    def accession(self):
        return self._assembly.accession

    def assembly_report(self):
        """Assumes there is only one assembly report in the data catalog
        """
        for assembly_report_file in self._files_of_type(catalog_pb2.File.ASSEMBLY_REPORT):
            with open(os.path.join(self._bdbag_dir, 'data', assembly_report_file)) as fh:
                raw_data = json.dumps(yaml.safe_load(fh.read()))
            assembly_report = JsonPbParse(raw_data, assembly_report_pb2.AssemblyReport())
            return assembly_report

    def fastas(self):
        for fasta_file in self._files_of_type(catalog_pb2.File.FASTA):
            with open(os.path.join(self._bdbag_dir, 'data', fasta_file), 'rt') as handle:
                for record in FastaIterator(handle):
                    yield record

    def gff3s(self, filt=None):
        for gff3_file in self._files_of_type(catalog_pb2.File.GFF3):
            if filt and filt in gff3_file or not filt:
                yield os.path.join(self._bdbag_dir, 'data', gff3_file)

    def sequences(self):
        for sequence in self.fastas():
            defline = sequence.description
            # TODO: Awful hack b/c the catalog doesn't pair gff with fna
            m = re.search('chromosome (\\d+)', defline)
            if not m:
                filt = 'genomic_MT'
            else:
                filt = f'genomic_{m.group(1)}'
            gff3s = []
            for gff3 in self.gff3s(filt=filt):
                gff3s.append(gff3)
            yield Sequence(self.assembly_report(), sequence, gff3s[0])


class BioDataset():
    """BioDataset class
    """

    def __init__(self, bdbag_dir):
        self._bdbag_dir = bdbag_dir
        raw_data = open(os.path.join(
            bdbag_dir, 'data/dataset_catalog.json'), 'r').read()
        self._catalog = JsonPbParse(raw_data, catalog_pb2.Catalog())

    def assemblies(self):
        for assembly in self._catalog.assemblies:
            yield Assembly(self._bdbag_dir, assembly)
