# copyright (c) 2020 cisco Systems Inc., ALl rights reserved
# @author rks@cisco.com
from dnac.exception.BadProjectFileException import Error


class DuplicateFloorException(Error):
    """Raised when a floor is listed more than once in an archive while importing """
    def __init__(self, building_name, floor_name):
        self.__building_name__ = building_name
        self.__floor_name__ = floor_name

    @property
    def building(self):
        return self.__building_name__

    @property
    def floor(self):
        return self.__floor_name__
