# copyright (c) 2020 cisco Systems Inc., All rights reserved
import tempfile
import argparse
import os
import sys
import json

from zipfile import ZipFile
from zipfile import BadZipFile
from dnac.exception.BadProjectFileException import InvalidProjectFileException
from dnac.utils.os.FileSystem import FileSystem

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class Packager:
    def __init__(self):
        pass

    @staticmethod
    def unpack(projectfile):
        root = FileSystem.maketempdir()
        try:
            # opening the zip file in READ mode
            with ZipFile(projectfile, 'r') as zip:

                # extracting all the files
                zip.extractall(root)
                return root
        except BadZipFile:
            print('??This is not a zip file - ignored')
            raise InvalidProjectFileException
        except Exception as e:
            print('??Unknown failure ' + str(e))

        raise InvalidProjectFileException


