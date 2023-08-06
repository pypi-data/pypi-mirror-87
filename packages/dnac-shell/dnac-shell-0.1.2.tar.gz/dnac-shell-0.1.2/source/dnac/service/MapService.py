from __future__ import annotations
from typing_extensions import Protocol
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional, Tuple
import json
from dnac.service.maps.CalibrationModel import CalibrationModel
from dnac.maglev.task.Task import Task
from dnac.service.maps.Floor import Floor
from dnac.service.maps.MapArchiveFormat import MapArchiveFormat
from dnac.service.site.Building import Building
from dnac.utils.csv.MapsCsv import MapsCsv

# copyright (c) 2019-20 cisco Systems Inc., All rights reserved
# @author rks@cisco.com


class MapService:
    def __init__(self, services):
        self._services_ = services

    @property
    def maglev(self):
        return self._services_.maglev

    #
    @property
    def dnacSecurityManager(self):
        return self.maglev.security_manager

    #
    @property
    def dnacTaskManager(self):
        return self.maglev.task_manager

    #
    @property
    def groupingService(self):
        return self._services_.groupingService

    #
    @property
    def urlListModels(self) -> str:
        return '/api/v1/dna-maps-service/calibration/rfmodels'

    #
    @property
    def urlListFloors(self) -> str:
        return '/api/v1/dna-maps-service/domains?type=4'

    def urlListFloorAps(self, floorid: str) -> str:
        return '/api/v1/dna-maps-service/domains/' + floorid.strip() + '/aps'

    def urlListFloorPaps(self, floorid: str) -> str:
        return '/api/v1/dna-maps-service/domains/' + floorid.strip() + '/paps'

    #
    @property
    def urlCreateFloor(self) -> str:
        return '/api/v1/dna-maps-service/domains'

    #
    def urlUpdateFloor(self, floorid: str) -> str:
        return '/api/v1/dna-maps-service/domains/' + str(floorid) if floorid else None

    def urlAssignPaps(self, floorid: str) -> str:
        return '/api/v1/dna-maps-service/domains/' + str(floorid) + '/paps' if floorid else None

    def urlExportArchive(self, floorid, output_format: MapArchiveFormat) -> str:
        if output_format == MapArchiveFormat.PRIME_ARCHIVE:
            return '/api/v1/dna-maps-service/archives/export/' + str(floorid) if floorid else None
        if output_format == MapArchiveFormat.EKAHAU:
            return ('/api/v1/dna-maps-service/archives/export/' + str(
                floorid) if floorid else None) + '?exportFormat=ekahauFormat'
        raise ValueError('Invalid parameter: Unsupported export format')

    # Discover package version of DNA Maps Service
    def discover_service_version(self) -> str:
        return self.maglev.kernel.get_package_version('network-visibility')

    #
    #
    def discover_calibration_models(self):
        cbresp = self.dnacSecurityManager.call_dnac(self.urlListModels)
        return CalibrationModel.parseJson(cbresp.text) if cbresp.status_code == 200 else None

    #

    def discover_floor(self, hierarchy):
        return self.groupingService.discover_site_hierarchy(hierarchy) if hierarchy and hierarchy.strip() else None

    #
    # Create a floor with the given parameters
    #
    def create_floor(self, floor):
        if floor:
            # Create the async task...
            response = self.dnacSecurityManager.post_to_dnac(self.urlCreateFloor, floor.dnacJson)
            if response.status_code < 200 or response.status_code > 202:
                return None

            #
            # Expect a task response - follow the taskid to completion
            #
            task = Task.parseJson(response.text)

            # Follow the async task to completion
            floor.id = self.dnacTaskManager.follow_task(task)
            return floor

        raise ValueError('Request to create Invalid floor - ignored')

    #
    # Update an existing floor with the given parameters
    #
    def update_floor(self, floor):
        '''
            Update the specified floor
        '''
        if floor:
            # Create the async task...
            url = self.urlUpdateFloor(floor.id)
            response = self.dnacSecurityManager.post_to_dnac(url, floor.dnacJson, operation='put')
            if response.status_code < 200 or response.status_code > 202:
                return None

            #
            # Expect a task response - follow the taskid to completion
            #
            task = Task.parseJson(response.text)

            # Follow the async task to completion
            floor.id = self.dnacTaskManager.follow_task(task)
            return floor

        raise ValueError('Request to create Invalid floor - ignored')

    def update_floor_indices(self, csvfile):
        mapcsv = MapsCsv(csvfile)
        malformed_csv, malform_type, floor_indexes = mapcsv.load_floor_indexes()
        if malformed_csv:
            return malform_type
        if not floor_indexes or not len(floor_indexes):
            return 0
        count = 0
        for next_floor_index in floor_indexes:
            floor_hierarchy, floor_index = next_floor_index
            if floor_hierarchy and floor_index:
                if not floor_hierarchy.strip().startswith('Global'):
                    floor_hierarchy = ('Global' if floor_hierarchy.startswith('/') else 'Global/') + floor_hierarchy
                floor_list = self.discover_floor(floor_hierarchy.strip())
                next_floor = floor_list[0] if floor_list and len(floor_list) else None
                next_floor.index = floor_index
                self.update_floor(next_floor)
                count += 1
        return count

    def update_floor_backdrop(self, floor, image):
        if floor and floor.backdropImageUrl and image:
            return self.dnacSecurityManager.post_image_to_dnac(floor.backdropImageUrl, image)
        return None

    #
    # Look up a floor by name - since we are not likely to have
    # many floors in a building, O(n) lookup time is acceptable.
    #
    def find_floor_in_building(self, building: Building, floor_name: str) -> Optional[Floor]:
        if not floor_name or not floor_name.trim():
            return None
        for next_floor in self._floors_:
            if next_floor.name and next_floor.name == floor_name:
                return next_floor
        return None

    #
    # Delete the specified floor
    #
    def delete_floor(self, floor):
        '''
            Delete the specified floor
        '''
        if floor and floor.url:

            response = self.dnacSecurityManager.post_to_dnac(url=floor.url, json_payload='', operation='delete')
            if response.status_code < 200 or response.status_code > 202:
                return False

            #
            # Expect a task response - follow the taskid to completion
            #
            self.dnacTaskManager.follow_task(Task.parseJson(response.text))
            return True

        raise ValueError('Request to delete Invalid or non-existant floor')

    #
    # Assign PAPs to the  specified floor
    #
    def assign_paps(self, floorx, pap):

        if not floorx or not pap:
            raise ValueError('Invalid parameter sin PAP assignment request - ignored')

        # Create the async task...
        papJson = '[' + pap.dnacJson + ']'
        response = self.dnacSecurityManager.post_to_dnac(self.urlAssignPaps(floorx.id), papJson)
        if response.status_code < 200 or response.status_code > 202:
            return

        #
        # Expect a task response - follow the taskid to completion
        #
        # print('Pap task ', response.text)
        # task = Task.parseJson(response.text)

        # Follow the async task to completion
        # self.dnacTaskManager.follow_task(task)
        return

    #
    # Export the specified site/building/floor in the specified format: either Prime archive
    # or as Ekahau project file
    #
    def export_site(self, sitex, filenamex, export_format=MapArchiveFormat.EKAHAU):

        if not sitex:
            sitex = self.groupingService.discover_global()
            raise ValueError('Fatal internal error: Failed to identify the global site')

        # Create the async task...
        response = self.dnacSecurityManager.post_to_dnac(self.urlExportArchive(sitex, export_format), filenamex,
                                                         operation='post',
                                                         given_headers={'Content-Type': 'text/plain',
                                                                        'Accept': 'application/json'})

        if response.status_code < 200 or response.status_code > 202:
            response = self.dnacSecurityManager.post_to_dnac(self.urlExportArchive(sitex, export_format), filenamex,
                                                             operation='post',
                                                             given_headers={'Content-Type': 'text/plain',
                                                                            'Accept': '*/*'})
            if response.status_code < 200 or response.status_code > 202:
                return response.status_code, None

        resp_content_type = response.headers['Content-Type']
        if 'application/json' in resp_content_type:
            #
            # Expect a task response - follow the taskid to completion
            #
            task = Task.parseJson(response.text)
            # Follow the async task to completion
            result = self.dnacTaskManager.follow_task(task)
            return response.status_code, resp_content_type, result
        elif 'application/octet-stream' in resp_content_type:
            return response.status_code, resp_content_type, response.content
        else:
            raise ValueError('Fatal error: Unrecognized response from server: ', response.status_code, response.headers,
                             response.headers)

    def discover_floor_aps(self, floorid):
        cbresp = self.dnacSecurityManager.call_dnac(self.urlListFloorAps(floorid))
        if cbresp.status_code == 200:
            cbs = json.loads(cbresp.text)
            return cbs['items']
        return None

    def discover_floor_paps(self, floorid):
        cbresp = self.dnacSecurityManager.call_dnac(self.urlListFloorPaps(floorid))
        if cbresp.status_code == 200:
            cbs = json.loads(cbresp.text)
            return cbs['items']
        return None
