# pylint: disable=unnecessary-pass,too-few-public-methods
"""
CSV-to-file static mapper:
maps file paths taken from a CVS column to a data files in a remote storage
"""
import os
import glob
import csv
import re
from typing import List
from .static_file_mapper import StaticFileMapper


class CSVToFileMapper(StaticFileMapper):
    """
    CSV to File Mapper

    Attributes
    ----------
    csv_column : str
        CSV column index to get file paths from (starts from 0)
    skip_header : bool
        skip first line in CSV (usually column header)
    labels_pattern : str
        pattern for using with glob.iglob when getting CSV files

    Methods
    -------
    map_files():
        Performs file mapping.
    """
    def __init__(self, cache_dir: str, labels_dir: str, labels_pattern: str, csv_column: int = 0, skip_header: bool = True):
        """
        Initializes file mapper

        Args:
            cache_dir (str): data cache directory
            labels_dir (str): labels directory
            labels_pattern (str): labels pattern
            csv_column (int, optional): CVS column index for getting file paths from. Defaults to 0.
            skip_header (bool, optional): Whether to skip CVS header (first line). Defaults to True.
        """
        super().__init__(cache_dir, labels_dir)
        self.csv_column = csv_column
        self.skip_header = skip_header
        self.labels_pattern = labels_pattern

    def map_files(self) -> List[str]:
        """
        Performes file mapping. Derived classes must override it.

        Returns:
            List[str]: list of mapped files
        """
        paths = []
        last_file = ""  # we preserve last file name as a simple way to avoid duplicates
        for filepath in glob.iglob(os.path.join(self.labels_dir, self.labels_pattern), recursive=True):
            with open(filepath, "r") as csvfile:
                datareader = csv.reader(csvfile)
                try:
                    if self.skip_header:
                        next(datareader)  # skip the header row
                    for row in datareader:
                        file = str(row[self.csv_column]).strip()

                        # removing filename "tails" with and after '#' and '?'
                        # (e.g. timestamps in VoTT, filename.mp4#timestamp)
                        file = re.split('#|\\?', file)[0]

                        if file not in ("", last_file):
                            paths.append(file)
                            last_file = file
                except StopIteration:
                    pass
        return paths
