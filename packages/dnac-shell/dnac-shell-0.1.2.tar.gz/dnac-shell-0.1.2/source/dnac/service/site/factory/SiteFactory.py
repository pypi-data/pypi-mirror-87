import json

from dnac.service.maps.Floor import Floor
from dnac.service.site.Building import Building
from dnac.service.site.Site import Site
from dnac.service.site.util.SiteParser import SiteParser


# copyright (c) 2019-20 cisco Systems Inc., ALl righhts reseerved

class SiteFactory:

    # Parse the entity Json returned by DNAC and recreate the object
    #
    @staticmethod
    def makeSite(cbjsonstr):
        '''
            Factory (static) method to discern the type of the site entity and create area, a building or a floor from the DNAC Json from the given Json representatopn
        '''
        site_type = SiteParser.parseSiteAttributes(str(cbjsonstr))
        if not site_type:  # No site found - empty site list
            return None

        cbs = json.loads(cbjsonstr) if isinstance(cbjsonstr, str) else cbjsonstr
        if site_type == 'area':
            return SiteFactory.makeArea(cbs)

        if site_type == 'building':
            return SiteFactory.makeBuilding(cbs)

        return SiteFactory.makeFloor(cbjsonstr) if site_type == 'floor' else None

    @staticmethod
    def makeArea(area):
        '''
            Factory (static) method to create a area from the DNAC Json yielded by DNAC service
        '''
        if isinstance(area, list):
            return [Site(cb['id'], cb['name'], cb['groupNameHierarchy'], cb['systemGroup'],
                         cb['parentId'] if 'parentId' in cb.keys() else ' ') for cb in area]

        if isinstance(area, dict):
            if 'response' in area.keys():
                payload = area['response']
                area = payload[0] if isinstance(payload, list) else payload

        return Site(area['id'], area['name'], area['groupNameHierarchy'], area['systemGroup'] if 'systemGroup' in area.keys() else False,
                    area['parentId'] if 'parentId' in area.keys() else ' ') if area else None


    @staticmethod
    def makeBuilding(building):
        '''
            Factory (static) method to create a building from the DNAC Json yielded by DNAC service
        '''
        if isinstance(building, list):
            return [Building(bldg['id'], bldg['name'], bldg['groupNameHierarchy'], ' ',
                             bldg['parentId'] if 'parentId' in bldg.keys() else ' ') for bldg in building]

        if isinstance(building, dict):
            if 'response' in building.keys():
                building = building['response'][0] if len(building['response']) else None

        return Building(building['id'], building['name'], building['groupNameHierarchy'], ' ',
                        building['parentId'] if 'parentId' in building.keys() else ' ') if building else None


    @staticmethod
    def makeFloor(floor):
        '''
            Factory (static) method to create a floor area from the DNAC Json yielded by DNAC service
        '''
        return Floor.parseJson(floor)
