# copyright (c) 2020 cisco Systems Inc., All righhts reseerved
# @author rks@cisco.com

from dataclasses import dataclass
from typing import Dict, Tuple
from dnac.DnacCluster import DnacCluster
from dnac.service.site.Site import Site

@dataclass
class RelocatedSite:
    """Class for denoting the mapping of a source site to a target site"""
    source_site: Site
    target_hierarchy: str
    target_site: Site

class MapHierarchyDeployer:
    """Class that implements the provisioning of a DNAC Map archive onto the specified DNAC CLuster"""
    def __init__(self):
        pass

    @staticmethod
    def deploy_paps(floor, dnac_cluster):
        if floor and floor.pap_count > 0:
            # print('Deploying %d PAPs on %s', floor.pap_count, floor.name)
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
                print('??Failed to update floor image of %s ', floor.name)

    @staticmethod
    def deploy_floor(floor, dnac_cluster):
        if not floor:
            return 0, 0
        if dnac_cluster.mapService.create_floor(floor):
            MapHierarchyDeployer.deploy_floor_image(floor, dnac_cluster)
            pap_count = MapHierarchyDeployer.deploy_paps(floor, dnac_cluster)
            return 1, pap_count
        print('??Failed to create floor ->', floor.name)
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
    def relocate_site(dnac_cluster: DnacCluster, given_site: Site, relocator: Dict[str, str] = None) -> RelocatedSite:
        if not given_site or not given_site.name or len(given_site.name.strip()) == 0 or not relocator or len(
                relocator) == 0:
            return RelocatedSite(given_site, None, None)

        mapped_name = relocator[given_site.name] if given_site.name in relocator.keys() else None
        if not mapped_name:
            return RelocatedSite(given_site, None, None)

        mapped_name = mapped_name.strip()
        mapped_site = dnac_cluster.groupingService.discover_site_hierarchy(mapped_name if mapped_name.startswith("Global") else "Global/" + mapped_name)
        return RelocatedSite(given_site, mapped_name, mapped_site)

    @staticmethod
    def deploy(sites: Dict[str, Site], relocator: Dict[str, str], dnac_cluster: DnacCluster) -> Tuple[
        int, int, int]:

        deployed_sites = deployed_buildings = deployed_floors = 0
        if not sites or len(sites) == 0:
            return deployed_sites, deployed_buildings, deployed_floors

        for the_next_site in sites.values():
            retargeted_site = MapHierarchyDeployer.relocate_site(dnac_cluster, the_next_site, relocator)
            if retargeted_site.target_site:
                target_site = retargeted_site.target_site
            elif retargeted_site.target_hierarchy:
                # Create target hierarchy
                name_components = retargeted_site.target_hierarchy.split('/')
                name = name_components[-1] if name_components else None
                if not name:
                    # Failed to parse the specified target hierarchy -  skip this site
                    print('%% Failed to parse mapped hierarchy <' + retargeted_site.target_hierarchy + '>: Skipping this site')
                    continue

                target_site = Site('', name, retargeted_site.target_hierarchy)
                target_site = dnac_cluster.groupingService.create_site(target_site)
                if not target_site:
                    print('%% Failed to create retargeted site hierarchy <' + retargeted_site.target_hierarchy + '>: Skipping this site')
                    continue
            else:
                # Failed to map  - skip this site with a warning
                print('%% Failed to map site <' + retargeted_site.source_site.name + '>: Skipping this site')
                continue

            deployed_sites += 1
            if the_next_site.building_count > 0:
                buildings = the_next_site.get_all_buildings()
                for next_bldg in buildings:
                    next_bldg.parentSite = target_site
                    bcx, fcx = MapHierarchyDeployer.deploy_building(next_bldg, dnac_cluster)
                    if bcx:
                        deployed_buildings += bcx
                        deployed_floors += fcx

        print('[Finished deployment: ', deployed_sites, ' campuses ', deployed_buildings, ' buildings, and ',
              deployed_floors, ' floor areas]')
        return deployed_sites, deployed_buildings, deployed_floors
