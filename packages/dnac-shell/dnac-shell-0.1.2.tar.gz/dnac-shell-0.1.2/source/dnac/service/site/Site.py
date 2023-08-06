import json
from jinja2 import Template
from dnac.maglev.security.SecurityManager import SecurityManager
from dnac.service.site.util.SiteParser import SiteParser


# copyright (c) 2019 cisco Systems Inc., ALl righhts reseerved

class Site:
    def __init__(self, id, name, hierarchy=None, is_system_grp=False, parent=''):
        self._id_ = id
        self._name_ = name
        self._hierarchy_ = hierarchy if hierarchy else 'Global/' + name.strip()
        self._is_system_grp_ = is_system_grp
        self._parent_id_ = parent
        self._buildings_ = dict()
        self._coordinates_ = ()

    @property
    def name(self):
        return self._name_

    @name.setter
    def name(self, given_name):
        self._name_ = given_name

    @property
    def id(self):
        return self._id_

    @id.setter
    def id(self, id):
        self._id_ = id

    @property
    def parentId(self):
        return self._parent_id_

    @parentId.setter
    def parentId(self, parent):
        self._parent_id_ = parent

    @property
    def hierarchy(self):
        return self._hierarchy_

    @property
    def isSystemGroup(self):
        return self._is_system_grp_

    @property
    def building_count(self):
        return len(self._buildings_)

    @property
    def geocoordinates(self):
        return self._coordinates_

    @geocoordinates.setter
    def geocoordinates(self, coords):
        self._coordinates_ = coords

    @property
    def url(self):
        return '/api/v1/group/' + self.id if self.id else None

    @property
    def jsonTemplate(self):
        return '''
	{
   		"groupTypeList":[
      		"SITE"
   		],
   		"parentId":"{{ tvPARENT_SITE_ID }}",
   		"name":"{{ tvSITE_NAME }}",
   		"additionalInfo":[
      			{
         			"nameSpace":"Location",
         			"attributes":{
            			"type":"area"
         			}
      			}
   		]
	}
	 	       '''

    # Generate Json version of this object
    @property
    def dnacJson(self):
        x = Template(self.jsonTemplate)

        # Generate stringified operations list...
        return x.render(tvSITE_NAME=self.name, tvPARENT_SITE_ID=self.parentId)

    def get_building(self, id):
        return self._buildings_[id] if id and id in self._buildings_.keys() else None

    def get_all_buildings(self):
        return [self._buildings_[idx] for idx in self._buildings_]

    def add_building(self, building):
        if not building or not building.id:
            raise InvalidAttributeException(building)
        self._buildings_[building.id] = building

    def remove_building(self, building):
        if not building or not building.id:
            raise InvalidAttributeException(building)
        del self._buildings_[building.id]

    # Print out the object
    def print(self):
        print('==== Site ===')
        print('Name = ' + self.name)
        print('Id = ' + str(self.id))
        print('parentId = ' + str(self.parentId))
        print('Hierarchy = ' + str(self.hierarchy))
        print('is system grp = ' + str(self.isSystemGroup))
        print('=============')


#
if __name__ == "__main__":
    cbjson = '''
		[{"systemGroup":true,"groupHierarchy":"69444522-a32c-4e59-90fa-bad096537201","groupNameHierarchy":"Global","additionalInfo":[{"nameSpace":"System Settings","attributes":{"group.count.total":"2","hasChild":"TRUE","group.count.direct":"1","group.hierarchy.groupType":"SITE","member.count.total":"0","member.count.direct":"0"}}],"name":"Global","instanceTenantId":"SYS0","id":"69444522-a32c-4e59-90fa-bad096537201"}]
		'''

    model2 = Site.parseJson(cbjson)
    print('Model 2')
    print(type(model2))
    for i in model2:
        i.print()

    cbjson = '''
	{"response":[{"parentId":"69444522-a32c-4e59-90fa-bad096537201","systemGroup":false,"groupTypeList":["SITE"],"groupHierarchy":"69444522-a32c-4e59-90fa-bad096537201/ea91df3c-2b39-418c-89cf-a4ffdad133d4","groupNameHierarchy":"Global/AmalaPaul","additionalInfo":[{"nameSpace":"Location","attributes":{"addressInheritedFrom":"ea91df3c-2b39-418c-89cf-a4ffdad133d4","type":"area"}},{"nameSpace":"com.wireless.managingwlc","attributes":{"secondaryWlcInheritedFrom":"ea91df3c-2b39-418c-89cf-a4ffdad133d4","anchorWlcInheritedFrom":"ea91df3c-2b39-418c-89cf-a4ffdad133d4","tertiaryWlcInheritedFrom":"ea91df3c-2b39-418c-89cf-a4ffdad133d4","primaryWlcInheritedFrom":"ea91df3c-2b39-418c-89cf-a4ffdad133d4"}},{"nameSpace":"System Settings","attributes":{"group.count.total":"1","hasChild":"TRUE","group.count.direct":"1","group.hierarchy.groupType":"SITE","member.count.total":"0","member.count.direct":"0"}}],"name":"AmalaPaul","instanceTenantId":"5db7884336388b00b79e9d1b","id":"ea91df3c-2b39-418c-89cf-a4ffdad133d4"}],"version":"1.0"}
		'''

    model3 = Site.parseJson(cbjson)
    print('Model 3')
    print(type(model3))
    model3.print()
