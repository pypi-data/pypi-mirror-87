from dnac.exception import DnacException
from dnac.exception import InvalidCriterionException
from dnac.maglev.security.role.ResourceType import ResourceType
from dnac.maglev.security.role.Role import Role
from dnac.maglev.security.SecurityManager import SecurityManager
from dnac.service.maps.CalibrationModel import CalibrationModel
from dnac.service.maps.Floor import Floor
from dnac.service.maps.FloorGeometry import FloorGeometry
from dnac.maglev.task.TaskManager import TaskManager
from dnac.maglev.task.Task import Task


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved

class FileService:
    def __init__(self, services):
        self._services_ = services

    @property
    def maglev(self):
        return self._services_.maglev

    #
    @property
    def dnacSecurityManager(self):
        return self.maglev.security_manager

    def urlFile(self, fileid):
        return '/api/v1/file/' + fileid.strip() if fileid else None

    # Save specified file id on file service into specified file
    def download_file(self, fileid, filename):
        return self.dnacSecurityManager.download_as( self.urlFile(fileid), filename)
