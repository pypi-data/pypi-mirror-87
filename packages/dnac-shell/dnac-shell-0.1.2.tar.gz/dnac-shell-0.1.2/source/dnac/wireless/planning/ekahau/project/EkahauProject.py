from dnac.utils.package.Packager import Packager
from dnac.exception.BadProjectFileException import InvalidProjectFileException


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com
from dnac.utils.os.FileSystem import FileSystem


class EkahauProject:
    def __init__(self, project_file):
        self.__project_file__ = project_file
        self.__valid__ = False

    @property
    def project_file(self):
        return self.__project_file__

    @property
    def is_valid(self):
        return self.__valid__

    @is_valid.setter
    def is_valid(self, validity):
        self.__valid__ = validity

    def initialize(self):
        #self.is_valid(False)

        try:
            project_root = Packager.unpack(self.project_file)
        except InvalidProjectFileException:
            print('The specified Ekahau project file is invalid - aborting')
            return False

        if not self.validate(project_root):
            print('The specified Ekahau project file has invalid format or is malformed')
            return False

        return self.is_valid

    def validate(self, project_root):
        self.is_valid = False
        ekahau_elements = ['version', 'project.json', 'floorPlans.json', 'tagKeys.json']
        for next_file in ekahau_elements:
            if not FileSystem.is_valid_file(project_root, next_file):
                print(' file ', project_root, next_file, ' is invalid')
                return
        self.is_valid = True
        return self.is_valid
