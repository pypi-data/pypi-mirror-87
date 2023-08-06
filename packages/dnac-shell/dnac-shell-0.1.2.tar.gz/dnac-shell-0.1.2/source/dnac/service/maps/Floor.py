import json
from typing import List

from jinja2 import Template
from dnac.maglev.security.SecurityManager import SecurityManager
from dnac.service.site.util.SiteParser import SiteParser
from dnac.service.site.Building import Building
from dnac.service.maps.FloorGeometry import FloorGeometry


# copyright (c) 2019-20 cisco Systems Inc., ALl righhts reseerved

# @auto_attr_check
class Floor:
    '''
		This entity represents the floormap element the smallest granularity of
		sites managed by wireless maps.
	'''

    def __init__(self, id, name, parent, geometry, contact='', rfmodel='', above_floor=None, below_floor=None):
        if not isinstance(id, str):
            raise ValueError('Floor id must be a string')
        self._id_ = id
        self._name_ = name
        self._hierarchy_ = (parent.hierarchy if isinstance(parent, Building) else '') + '/' + self.name.strip()
        self._parent_id_ = parent
        self._parent_ = parent if isinstance(parent, Building) else Building(parent, ' ', ' ')
        self._geometry_ = geometry
        self._contact_ = contact
        self._rfmodel_ = rfmodel
        self._above_ = above_floor
        self._floor_index_ = 1
        self._below_ = below_floor
        self._image_ = None
        self._paps_ = dict()
        self._index_ = 1

    @classmethod
    def with_dimensions(cls, idx, namex, building, dimension, above, below):
        geometry = FloorGeometry.from_tuple(dimension)
        contactx = None
        rfmodelx = None
        floor = cls(idx, namex, building, geometry, contactx, rfmodelx, above, below)
        floor.parent = building
        return floor

    @property
    def name(self):
        return self._name_

    @name.setter
    def name(self, name):
        self._name_ = name

    @property
    def index(self):
        return self._index_

    @index.setter
    def index(self, idx):
        self._index_ = idx

    @property
    def floor_index(self):
        return self._floor_index_

    @floor_index.setter
    def floor_index(self, idx):
        self._floor_index_ = idx

    @property
    def geometry(self):
        return self._geometry_

    @property
    def hierarchy(self):
        return self._hierarchy_

    @hierarchy.setter
    def hierarchy(self, thehier):
        self._hierarchy_ = thehier

    @property
    def id(self):
        return self._id_

    @id.setter
    def id(self, id):
        self._id_ = id

    @property
    def rfmodel(self):
        return self._rfmodel_

    @rfmodel.setter
    def rfmodel(self, rfmodel):
        self._rfmodel_ = rfmodel

    @property
    def contact(self):
        return self._contact_

    @contact.setter
    def contact(self, contact):
        self._contact_ = contact

    @property
    def parentId(self):
        return self._parent_id_

    @parentId.setter
    def parentId(self, parent):
        self._parent_id_ = parent

    @property
    def parent(self):
        return self._parent_

    @parent.setter
    def parent(self, parent):
        self._parent_ = parent
        self._parent_.add_floor(self)
        self.parentId = parent.id if parent else None

    @property
    def image(self):
        return self._image_

    @image.setter
    def image(self, image):
        self._image_ = image

    @property
    def pap_count(self):
        return len(self._paps_) if self._paps_ else 0

    def get_all_paps(self):
        return [self._paps_[idx] for idx in self._paps_]

    def add_pap(self, pap):
        self._paps_[pap.name] = pap
        pap.parent = self

    def remove_ap(self):
        del self._paps_[ap.name]

    @property
    def url(self):
        return '/api/v1/dna-maps-service/domains/' + self.id if self.id else None

    @property
    def groupUrl(self):
        return '/api/v1/group/' + self.id if self.id else None

    @property
    def backdropImageUrl(self):
        return self.url + '/image' if self.url else None

    @property
    def jsonTemplate(self):
        return '''
{"type":4,"floorIndex":"{{tvFLOOR_INDEX}}","contact":"{{tvCONTACT}}","maintainAspectRatio":false,"geometry":{{ tvGEOMETRY }},"parentGroupUuid":"{{tvPARENT_ID}}","incomplete":false,"name":"{{tvSITE_NAME}}"}
	 	       '''

    # Generate Json version of this object
    @property
    def dnacJson(self):
        geometryjson = self.geometry.dnacJson
        # Generate stringified operations list...
        return Template(self.jsonTemplate).render(tvSITE_NAME=self.name, tvPARENT_ID=self.parentId,
                                                  tvCONTACT=self.contact, tvRFMODEL=self.rfmodel,
                                                  tvFLOOR_INDEX=self.index,
                                                  tvGEOMETRY=geometryjson.strip())

    # Parse the floor attributes to get floor entity
    #
    @staticmethod
    def find_hierarchy(grphier, namehier):
        grpid_list = grphier.split('/')
        name_list = namehier.split('/')
        if len(grpid_list) != len(name_list):
            return None
        lst = []
        for i in range(len(grpid_list)):
            lst.append((grpid_list[i], name_list[i]))

        return lst

    # Find additional Info fields
    #
    @staticmethod
    def find_additional_info(floor_addl_attributes: List) -> dict:
        additional_info = dict()
        for info in floor_addl_attributes:
            if isinstance(info, dict) and 'nameSpace' in info.keys() and 'attributes' in info.keys():
                key = info['nameSpace']
                attrs = info['attributes']
                additional_info[key] = attrs

        return additional_info

    # Parse the floor attributes to get floor entity
    #
    @staticmethod
    def parseJson(cbjsonstr):
        cbs = json.loads(cbjsonstr) if isinstance(cbjsonstr, str) else cbjsonstr
        cbs = cbs['response'] if isinstance(cbs, dict) and 'response' in cbs.keys() else cbs

        if cbs:
            if (isinstance(cbs, list)):
                return [Floor.parseJson(next_floor) for next_floor in cbs]
            elif (isinstance(cbs, dict)):
                if 'name' in cbs.keys() and 'groupHierarchy' in cbs.keys() and 'groupNameHierarchy' in cbs.keys():
                    geometry = FloorGeometry(100, 100, 10, 0.0, 0.0)
                    grphier = cbs['groupHierarchy']
                    namehier = cbs['groupNameHierarchy']
                    hier_pair_list = Floor.find_hierarchy(grphier, namehier)

                    floorid, floorname = hier_pair_list.pop() if hier_pair_list and len(hier_pair_list) else None
                    bldgid, bldgname = hier_pair_list.pop() if hier_pair_list and len(hier_pair_list) else None
                    parsed_floor = Floor(floorid, cbs['name'], bldgid, geometry, '', '')
                    parsed_floor.additional_info = Floor.find_additional_info(cbs['additionalInfo'])
                    if parsed_floor.additional_info and 'mapsSummary' in parsed_floor.additional_info.keys():
                        map_summary = parsed_floor.additional_info['mapsSummary']
                        parsed_floor.floor_index = map_summary['floorIndex'] if map_summary and 'floorIndex' in map_summary.keys() else 1
                return parsed_floor

        return None

    # Print out the object
    def __str__(self):
        return ('<Name = ' + self.name + ', Id = ' + str(self.id) + ', parentId = ' + str(
            self.parentId) + ', Contact = ' + self.contact + ', Rfmodel = ' + self.rfmodel if self.rfmodel else '<Default RF Model>' + '>')

#
