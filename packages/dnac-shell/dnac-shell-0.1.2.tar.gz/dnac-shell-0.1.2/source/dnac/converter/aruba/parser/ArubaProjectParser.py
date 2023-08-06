# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

from __future__ import annotations
from typing_extensions import Protocol
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional, Tuple
import os
import xml.etree.ElementTree as ET
from typing import List, Dict
import random

from dnac.exception.BadProjectFileException import InvalidProjectFileException
from dnac.exception.DuplicateFloorException import DuplicateFloorException
from dnac.model.network.AccessPoint import AccessPoint
from dnac.utils.os.FileSystem import FileSystem
from dnac.service.site.Site import Site
from dnac.service.site.Building import Building
from dnac.model.network.PAP import PAP
from dnac.service.maps.Floor import Floor


class ArubaProjectParser:
    def __init__(self):
        pass

    #
    # Validate basic elements of the AirWave project
    #
    @staticmethod
    def is_valid(project_root: str) -> bool:
        if not os.path.exists(project_root):
            return False

        if not os.path.isdir(project_root):
            return False

        campuses = 'campus_building_list.xml'
        if not FileSystem.is_valid_file(project_root, campuses):
            return False

        location = 'location_store.xml'
        if not FileSystem.is_valid_file(project_root, location):
            return False

        version = 'version.xml'
        if not FileSystem.is_valid_file(project_root, version):
            return False

        os.chdir(project_root)
        campus_tree = ET.parse(campuses)
        root = campus_tree.getroot()
        campus_list = [root.tag for elem in root.iter() if elem.tag == 'campus']
        return len(campus_list) > 0

    @staticmethod
    def parse(project_root: str) -> Dict[str, Site]:
        if not ArubaProjectParser.is_valid(project_root):
            raise InvalidProjectFileException

        os.chdir(project_root)
        campus_file = 'campus_building_list.xml'
        campus_tree = ET.parse(campus_file)
        root = campus_tree.getroot()
        campuses = dict()
        for campus in campus_tree.iter('campus'):
            next_campus = ArubaProjectParser.process_campus(campus)
            if next_campus:
                campuses[next_campus.id] = next_campus
            else:
                print('Campus <<', next_campus.tag, ">> not processed - incomplete")

        # Parse all floors from top level and insert them into
        # respective buildings
        #
        floor_count = ArubaProjectParser.process_floors(campuses, root)
        return campuses

    #
    # Parse  "campus" XMLElement in AirWave project and  yield
    # equivalent the DNAC "Site". If the XML entity is illegally formed, then yield
    # None as Site (hence, Optional[Site]).
    #
    @staticmethod
    def process_campus(campus_element) -> Optional[Site]:
        site = ArubaProjectParser.parse_campus_attributes(campus_element)
        if not site:
            return None
        for building_element in campus_element.iter('building'):
            building_entity = ArubaProjectParser.process_building(site, building_element)
            if building_entity:
                site.add_building(building_entity)
            else:
                print('Building <<', building_element, ">> not processed - incomplete")
        return site

    @staticmethod
    def parse_campus_attributes(campus_element) -> Optional[Site]:
        idx_namex = ArubaProjectParser.get_entity_id_name(campus_element)
        if not idx_namex:
            return None

        idx, namex = idx_namex
        if not idx:
            return None

        site = Site(idx, namex, 'Global/' + namex.strip())
        campus_attributes = campus_element.attrib
        geocoord = campus_attributes['latitude'] if 'latitude' in campus_attributes.keys() else None, campus_attributes[
            'longitude'] if 'longitude' in campus_attributes.keys() else None
        site.geocoordinates = geocoord
        return site

    @staticmethod
    def process_building(site, building_element) -> Optional[Building]:
        building = ArubaProjectParser.process_building_attributes(site, building_element)
        # if not building:
        # return None
        ####
        # for floor_element in building_element.iter('floor'):
        # floor_entity = ArubaProjectParser.process_building(site, building_element)
        # if floor_entity:
        # building.add_floor(floor_entity)
        # else:
        # print('Floor <<', floor_element, ">> not processed - incomplete")
        ####

        return building

    @staticmethod
    def process_building_attributes(site, building_element) -> Optional[Building]:
        idx_namex = ArubaProjectParser.get_entity_id_name(building_element)
        if not idx_namex:
            return None

        idx, namex = idx_namex
        if not idx:
            return None

        bldg_attributes = building_element.attrib
        geocoord = bldg_attributes['latitude'] if 'latitude' in bldg_attributes.keys() else None, bldg_attributes[
            'longitude'] if 'longitude' in bldg_attributes.keys() else None
        return Building.with_geocoords(idx, namex, site,
                                       geocoord if geocoord[0] and geocoord[1] else site.geocoordinates)

    @staticmethod
    def process_floors(sites, root_element) -> int:
        floor_count = 0
        for folder in os.listdir('.'):
            if folder == 'network':
                continue
            if os.path.isdir(folder):
                os.chdir(folder)
                floor_tree = ET.parse('site.xml') if os.path.isfile('site.xml') else None
                if not floor_tree:
                    continue
                for floor_element in floor_tree.iter('site'):
                    try:
                        next_floor = ArubaProjectParser.process_floor(sites, floor_element) if floor_element else None
                        if next_floor:
                            floor_count += 1
                        else:
                            print('Floor <<', folder, ">> not processed - incomplete")
                    except DuplicateFloorException as exc:
                        print('%% Duplicate listing of floor ', exc.floor, " under building ", exc.building,
                              " : ignored")
                        continue
                    finally:
                        os.chdir('..')
                        continue

        return floor_count

    #
    # Parse an  AirWave "floor" into a DNAC Floor.
    #
    @staticmethod
    def process_floor(sites: Dict[str, Site], floor_element) -> Optional[Floor]:
        idx_namex = ArubaProjectParser.get_entity_id_name(floor_element)
        if not idx_namex:
            return None
        idx, namex = idx_namex
        if not idx:
            return None

        floor_attribute = floor_element.attrib
        campus_id = floor_attribute['campus_id'] if 'campus_id' in floor_attribute.keys() else None
        building_id = floor_attribute['building_id'] if 'building_id' in floor_attribute.keys() else None
        height = floor_attribute['floor_height_ft'] if 'floor_height_ft' in floor_attribute.keys() else 10
        width = floor_attribute['width'] if 'width' in floor_attribute.keys() else None
        length = floor_attribute['height'] if 'height' in floor_attribute.keys() else None
        backdrop = os.path.abspath('background.jpg') if FileSystem.is_valid_file('.', 'background.jpg') else None
        dimension = (width, length, height) if width and length else None

        above = floor_attribute['above_id'] if 'above_id' in floor_attribute.keys() else None
        below = floor_attribute['below_id'] if 'below_id' in floor_attribute.keys() else None
        if campus_id and building_id:
            campus = sites[campus_id]
            building = campus.get_building(building_id)
            if not building:
                print('Building id ', building_id, ' not found in campus id ', campus_id)

            if building.floor_with_name_exists(namex):
                raise DuplicateFloorException(building.name, namex)

            # namex = ArubaProjectParser.generate_unique_name(namex, building) if building.floor_with_name_exists(
            # namex) else namex
            floor = Floor.with_dimensions(idx, namex, building, dimension, above, below)
            #
            # Process APs on this floor...
            floor = ArubaProjectParser.process_floor_aps(floor, floor_element)
            floor.image = backdrop
            # print('Total of ', floor.pap_count, " Access Points process on floor ", floor.name)
            return floor
        else:
            print('Floor <<', floor_element.tag, ">> not processed - has no parent references")
        return None

    @staticmethod
    def generate_unique_name(original_name: str, building: Building) -> str:
        for i in range(1, 100):
            random_int: int = random.randint(1, 100)
            derived_name = original_name + "-" + str(random_int)
            if not building.floor_with_name_exists(derived_name):
                return derived_name

        return None

    #
    # Parse the AirWave floor, convert all accesspoint definitoons intpo
    # DNAC Planned APs ("PAP").
    #
    @staticmethod
    def process_floor_aps(floor: Floor, floor_element) -> Floor:
        for ap_element in floor_element.iter('ap'):
            next_pap = ArubaProjectParser.process_ap(floor, ap_element)
            if next_pap:
                floor.add_pap(next_pap)
            else:
                print('Floor <<', ap_element.tag, ">> not processed - incomplete")
        return floor

    #
    # Parse a single AirWave AP definitopon: assume that thisis always
    # an internal Axel (C9130-I) Access Point.
    #
    @staticmethod
    def process_ap(floor: Floor, ap_element) -> Optional[PAP]:
        ap_attrib = ap_element.attrib
        idx = ap_attrib['id']
        apname = ap_attrib['name']
        aruba_model = ap_attrib['model']
        x = ap_attrib['x']
        y = ap_attrib['y']
        z = floor.geometry.height
        model = '9130I'
        new_ap = PAP(apname, model, floor)
        new_ap.position = (x, y, z)
        return new_ap

    @staticmethod
    def get_entity_id_name(entity_element) -> Tuple[str, str]:
        entity_attribute = entity_element.attrib
        idx = entity_attribute['id'] if 'id' in entity_attribute.keys() else None
        namex = entity_attribute['name'] if 'name' in entity_attribute.keys() else None
        return idx, namex if idx and namex else None
