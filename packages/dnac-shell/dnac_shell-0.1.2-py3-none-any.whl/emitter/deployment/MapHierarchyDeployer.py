from dnac.DnacCluster import DnacCluster
from dnac.maglev.security.SecurityManager import SecurityManager
from dnac.service.GroupingService import GroupingService
from dnac.service.site.Site import Site
from dnac.service.maps.Floor import Floor
from dnac.service.maps.FloorGeometry import FloorGeometry
from dnac.service.site.Building import Building
from dnac.service.MapService import MapService
from dnac.exception import *
from dnac.model.network.PAP import PAP


# copyright (c) 2020 cisco Systems Inc., All righhts reseerved
# @author rks@cisco.com


class MapHierarchyDeployer:

    def __init__(self):
        pass

    @staticmethod
    def deploy_paps(floor, dnac_cluster):
        if floor and floor.pap_count > 0:
            print('Deploying %d PAPs on %s', floor.pap_count, floor.name)
            paps = floor.get_all_paps()
            for next_pap in paps:
                x = next_pap.position[0]
                y = next_pap.position[1]
                z = next_pap.position[2]
                dnac_cluster.mapService.assign_paps(floor, next_pap)
            return floor.pap_count
        return 0

    @staticmethod
    def deploy_floor_image(floor, dnac_cluster):
        if floor:
            if not dnac_cluster.mapService.update_floor_backdrop(floor, floor.image):
                print('?Failed to update floor image of %s ', floor.name)

    @staticmethod
    def deploy_floor(floor, dnac_cluster):
        if not floor:
            return 0, 0
        if dnac_cluster.mapService.create_floor(floor):
            MapHierarchyDeployer.deploy_floor_image(floor, dnac_cluster)
            pap_count = MapHierarchyDeployer.deploy_paps(floor, dnac_cluster)
            return 1, pap_count
        print('Failed to create floor ->', floor.name)
        return 0, 0

    @staticmethod
    def deploy_building(building, dnac_cluster):
        bidx = dnac_cluster.groupingService.create_site(building)
        floor_count = 0
        if bidx:
            building.id = bidx.id
            if building.floor_count > 0:
                for next_floor in building.get_all_floors():
                    next_floor.parentId = building.id
                    fc, papc = MapHierarchyDeployer.deploy_floor(next_floor, dnac_cluster)
                    floor_count += fc

            return 1, floor_count

        print('Failed to create bldg ->', building.name, building.hierarchy)
        return 0, 0

    @staticmethod
    def deploy(sites, dnac_cluster):
        deployed_sites = deployed_buildings = deployed_floors = 0
        if not sites or len(sites) == 0:
            return deployed_sites, deployed_buildings, deployed_floors

        global_site = dnac_cluster.groupingService.discover_global()
        for next_site in sites:
            if next_site:
                idx = dnac_cluster.groupingService.create_site(next_site)
                if idx:
                    deployed_sites += 1
                    next_site.id = idx.id
                    if next_site.building_count > 0:
                        buildings = next_site.get_all_buildings()
                        for next_bldg in buildings:
                            bcx, fcx = MapHierarchyDeployer.deploy_building(next_bldg, dnac_cluster)
                            if bcx:
                                deployed_buildings += bcx
                                deployed_floors += fcx

        print('[Finished deployment: ', deployed_sites, ' campuses ', deployed_buildings, ' buildings, and ',
              deployed_floors, ' floor areas]')
        return deployed_sites, deployed_buildings, deployed_floors
