import codecs
import csv

import apache_beam as beam
from apache_beam.io import filesystem
from apache_beam.options.pipeline_options import PipelineOptions


class CsvFileSource(beam.io.filebasedsource.FileBasedSource):
    def __init__(
        self,
        file_pattern,
        compression_type=filesystem.CompressionTypes.UNCOMPRESSED,
        delimiter=",",
        header=True,
        dictionary_output=True,
        validate=True,
    ):
        self.delimiter = delimiter
        self.header = header
        self.dictionary_output = dictionary_output
        beam.io.filebasedsource.FileBasedSource.__init__(
            self,
            file_pattern,
            compression_type=compression_type,
            validate=validate,
            splittable=False,
        )

        if not self.header and dictionary_output:
            raise ValueError(
                "header is required for the CSV reader to provide dictionary output"
            )

    def read_records(self, file_name, range_tracker):
        # logging.info('debug read rec')
        headers = None
        self._file = self.open_file(file_name)

        reader = csv.reader(
            codecs.iterdecode(self._file, "utf-8"), delimiter=self.delimiter
        )

        for i, rec in enumerate(reader):
            if (self.header or self.dictionary_output) and i == 0:
                headers = rec
                continue

            if self.dictionary_output:
                res = {header: val for header, val in zip(headers, rec)}
            else:
                res = rec
            yield res


class _Fileobj2Iterator:
    def __init__(self, obj):
        self._obj = obj

    def __iter__(self):
        return self

    def __next__(self):
        line = self._obj.readline()
        if line == None or line == "":
            raise StopIteration
        return line


if __name__ == "__main__":
    pass
