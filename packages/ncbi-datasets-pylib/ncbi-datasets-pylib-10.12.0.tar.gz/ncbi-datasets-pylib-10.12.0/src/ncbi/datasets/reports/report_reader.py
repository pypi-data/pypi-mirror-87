import yaml
import logging

from google.protobuf.json_format import ParseDict, SerializeToJsonError, ParseError

import ncbi.datasets.v1alpha1.reports.assembly_pb2 as assembly_report_pb2
import ncbi.datasets.v1alpha1.reports.gene_pb2 as gene_report_pb2
import ncbi.datasets.v1alpha1.reports.virus_pb2 as virus_report_pb2


logger = logging.getLogger()


class DatasetsReportReader():
    """Helper functions to read data reports

    Methods to read assembly, gene and virus reports from files or file handles into protobuf objects
    """

    # Load yaml in 'buf' and parse resulting dictionary into protobuf 'schema_pb'
    def _load_and_parse_report(self, buf, schema_pb, from_array=False):
        """Return assembly protobuf report
        Args:
          buf:
            file or file-like object

        Returns:
          An AssemblyDataReport protobuf object
        """
        try:
            report_dict = yaml.safe_load(buf)
            if not report_dict:
                logger.error('Empty report from file')
            try:
                if from_array:
                    ParseDict(report_dict[0], schema_pb, ignore_unknown_fields=False)
                else:
                    ParseDict(report_dict, schema_pb, ignore_unknown_fields=False)
            except (SerializeToJsonError, ParseError) as e:
                logger.error('Error converting yaml to schema: %s', e)
        except yaml.YAMLError as e:
            logger.error('Error while loading yaml: %s', e)
        return schema_pb

    def assembly_report_from_file(self, report_file):
        """Return assembly protobuf report
        Args:
          report_file:
            assembly report file path or file-like object

        Returns:
          An AssemblyDataReport protobuf object
        """

        if isinstance(report_file, str):
            with open(report_file) as fh:
                return self._load_and_parse_report(fh, assembly_report_pb2.AssemblyDataReport())
        return self._load_and_parse_report(report_file, assembly_report_pb2.AssemblyDataReport())

    # return full gene report
    def gene_report_from_file(self, report_file):
        """Return full gene protobuf report
        Args:
          report_file:
            gene report file path or file-like object

        Returns:
          A GeneDescriptors protobuf object
        """

        if isinstance(report_file, str):
            with open(report_file) as fh:
                return self._load_and_parse_report(fh, gene_report_pb2.GeneDescriptors())
        return self._load_and_parse_report(report_file, gene_report_pb2.GeneDescriptors())

    def read_virus_report_from_file(self, report_file):
        """Return virus protobuf report
        Args:
          report_file:
            virus report file path or file-like object

        Returns:
          Yields a set of VirusAssembly protobuf objects
        """

        if isinstance(report_file, str):
            with open(report_file) as fh:
                yield from self.read_virus_report(fh)
        else:
            yield from self.read_virus_report(report_file)

    def read_virus_report(self, report_file_handle):
        """Return VirusAssembly protobuf objects
        Args:
          report_file_handle:
            virus report file handle

        Returns:
          Yields a set of VirusAssembly protobuf objects
        """

        def _create_assembly_pb(buf):
            schema_pb = virus_report_pb2.VirusAssembly()
            self._load_and_parse_report(buf, schema_pb, from_array=True)
            return schema_pb

        # Ignore header lines up to first '- accession:'
        first_accession = True
        assm_buf = ''
        while True:
            line = report_file_handle.readline()
            if not line:
                yield _create_assembly_pb(assm_buf)
                break
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            # Each line that starts with: '- accession:' is a new asembly
            # and (except for the first such line) the end of the previous one
            if line.startswith('- accession:'):
                if not first_accession:
                    yield _create_assembly_pb(assm_buf)
                first_accession = False
                assm_buf = line
            # Lines other than '- accession' with no identation are not part of an
            # assembly, e.g. the count at the end of the report
            elif line[0] == ' ':
                assm_buf += line
