import os
import xml.etree.ElementTree as ET

from dnac.exception.BadProjectFileException import InvalidProjectFileException
from dnac.model.network.AccessPoint import AccessPoint
# from dnac.model.site.Building import Building
# from dnac.model.site.Floor import Floor
# from dnac.model.site.Site import Site
from dnac.utils.os.FileSystem import FileSystem
from dnac.service.site.Site import Site
from dnac.service.site.Building import Building
from dnac.model.network.PAP import PAP
from dnac.service.maps.Floor import Floor
from dnac.service.maps.FloorGeometry import FloorGeometry


class ArubaProjectParser:
    def __init__(self):
        pass

    @staticmethod
    def is_valid(project_root):
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
        if len(campus_list) == 0:
            return False

        return True

    @staticmethod
    def parse(project_root):
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
        print("Aruba Parser: ", floor_count, " floors processed")
        return campuses

    @staticmethod
    def process_campus(campus_element):
        site = ArubaProjectParser.parse_campus_attributes(campus_element)
        if not site:
            return
        for building_element in campus_element.iter('building'):
            building_entity = ArubaProjectParser.process_building(site, building_element)
            if building_entity:
                site.add_building(building_entity)
            else:
                print('Building <<', building_element, ">> not processed - incomplete")
        return site

    @staticmethod
    def parse_campus_attributes(campus_element):
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
    def process_building(site, building_element):
        building = ArubaProjectParser.process_building_attributes(site, building_element)
        if not building:
            return None
        for floor_element in building_element.iter('floor'):
            floor_entity = ArubaProjectParser.process_building(site, building_element)
            if floor_entity:
                building.add_floor(floor_entity)
            else:
                print('Floor <<', floor_element, ">> not processed - incomplete")

        return building

    @staticmethod
    def process_building_attributes(site, building_element):
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
        # return Building(idx, namex, site, geocoord if geocoord[0] and geocoord[1] else site.geocoordinates)

    @staticmethod
    def process_floors(sites, root_element):
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
                    next_floor = ArubaProjectParser.process_floor(sites, floor_element) if floor_element else None
                    os.chdir('..')
                    if next_floor:
                        floor_count += 1
                    else:
                        print('Floor <<', folder, ">> not processed - incomplete")
        return floor_count

    @staticmethod
    def process_floor(sites, floor_element):
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
            floor = Floor.with_dimensions(idx, namex, building, dimension, above, below)
            floor.image = backdrop
            #
            # Process APs on this floor...
            floor = ArubaProjectParser.process_floor_aps(floor, floor_element)
            floor.image = backdrop
            print('Total of ', floor.pap_count, " Access Points process on floor ", floor.name)
            return floor
        else:
            print('Floor <<', floor_element.tag, ">> not processed - has no parent references")
        return None

    @staticmethod
    def process_floor_aps(floor, floor_element):
        for ap_element in floor_element.iter('ap'):
            next_pap = ArubaProjectParser.process_ap(floor, ap_element)
            if next_pap:
                floor.add_pap(next_pap)
            else:
                print('Floor <<', ap_element.tag, ">> not processed - incomplete")
        return floor

    @staticmethod
    def process_ap(floor, ap_element):
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
    def get_entity_id_name(entity_element):
        entity_attribute = entity_element.attrib
        idx = entity_attribute['id'] if 'id' in entity_attribute.keys() else None
        namex = entity_attribute['name'] if 'name' in entity_attribute.keys() else None
        return idx, namex if idx and namex else None
