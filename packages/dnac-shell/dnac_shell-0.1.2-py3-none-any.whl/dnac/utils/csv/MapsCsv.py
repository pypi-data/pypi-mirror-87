#
# This entity provides commonly used utils for processing
# Maps CSV files.
#
# copyright (c) 2020 cisco Systems Inc., All righhts reseerved
# @author rks@cisco.com
#
import csv
import re
import mimetypes
from typing import Dict, Union, Tuple, List


class MapsCsv:
    def __init__(self, csvfile):
        self._csv_ = csvfile

    @property
    def csv_file(self):
        return self._csv_

    @csv_file.setter
    def csv_file(self, newcsv):
        self._csv_ = newcsv

    @staticmethod
    def is_number(s):
        return re.match(r"[-+]?\d+$", s) is not None

    @staticmethod
    def is_csv_tuple(csv_tuple):
        return isinstance(csv_tuple, tuple) and len(csv_tuple) > 1

    @staticmethod
    def split(word):
        return [char for char in word]

    @staticmethod
    def is_text_file(the_file):
        mime_type_tuple = mimetypes.guess_type(the_file)
        mime_type = mime_type_tuple[0] if mime_type_tuple and len(mime_type_tuple) > 1 else None
        return mime_type and mime_type.lower() == 'text/csv'

    def load_floor_indexes(self):
        if not MapsCsv.is_text_file(self.csv_file):
            return True, -2, None

        fin = csv.DictReader(open(self.csv_file))
        results = list()
        for floor in fin:
            tuple_list = list(floor.items())
            if not MapsCsv.is_csv_tuple(tuple_list[0]) or not MapsCsv.is_csv_tuple(tuple_list[1]):
                return True, -2, None

            key1 = tuple_list[0][0]
            val1 = tuple_list[0][1]
            key1 = key1.strip().lower() if key1 else key1

            key2 = tuple_list[1][0]
            val2 = tuple_list[1][1]
            key2 = key2.strip().lower() if key2 else key2

            if key1.endswith('floorhierarchy') and key2.endswith('floorindex'):
                value = val2.strip()
                val = int(value) if MapsCsv.is_number(value) else value
                floor_attr = (val1, val2)
                results.append(floor_attr)
            else:
                return True, -1, results

        return False, 0, results

    # Map site A onto Site B
    #
    def load_site_mapper(self) -> Tuple[bool, int, dict]:

        #if not MapsCsv.is_text_file(self.csv_file):
            #return True, -2, dict()

        with open(self.csv_file) as csvfile:
            fin = csv.DictReader(csvfile, delimiter=";")
            mapper = dict()
            for mapelement in fin:
                tuple_list = list(mapelement.items())
                if not MapsCsv.is_csv_tuple(tuple_list[0]) or not MapsCsv.is_csv_tuple(tuple_list[1]):
                    return True, -2, dict()

                key1 = tuple_list[0][0]
                val1 = tuple_list[0][1]
                key1 = key1.strip().lower() if key1 else key1

                key2 = tuple_list[1][0]
                val2 = tuple_list[1][1]
                key2 = key2.strip().lower() if key2 else key2

                if key1.endswith('sourcesite') and key2.endswith('targetsite'):
                    value = val2.strip()
                    val = int(value) if MapsCsv.is_number(value) else value
                    floor_attr = (val1, val2)
                    mapper[val1] = val2
                else:
                    return True, -1, mapper

        return False, 0, mapper