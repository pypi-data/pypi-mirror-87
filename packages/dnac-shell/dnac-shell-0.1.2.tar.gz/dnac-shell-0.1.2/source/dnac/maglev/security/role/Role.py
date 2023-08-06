import json
from jinja2 import Template
from dnac.maglev.security.role.ResourceType import ResourceType 

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class Role:
	def __init__(self, role, description, roleid, role_type = 'CUSTOM', resource_types = None):
		self._role_ = role
		self._description_ = description
		self._roleid_ = roleid
		self._role_type_ = role_type
		if not isinstance(resource_types, list):
			raise ValueError('Resource Types must be a list' )

		self._resource_types_ = resource_types

	@classmethod
	def parseJson(cls, jsonx):
		resource_type_list = []
		if jsonx:
			if isinstance(jsonx, str):
				jsonx = json.loads(jsonx)
			elif not isinstance(jsonx, dict):
				raise ValueError('Role Json is invalid: should be a non-null dict')

			if jsonx['resourceTypes']:
				for resource_type in jsonx['resourceTypes']:
					resource_type_list.append(ResourceType.parseJson(resource_type))
			
			roleid = jsonx['roleId'] if 'roleId' in jsonx.keys() else None
			role = jsonx['role']
			descr = jsonx['description']
			role_type = jsonx['type'] if 'type' in jsonx.keys() else 'CUSTOM'
			return cls(role, descr, roleid, role_type, resource_type_list)
		else:
			return None

	@property
	def role(self):
		return self._role_
	
	@role.setter
	def role(self, newname):
		self._role_ = newname
	
	@property
	def description(self):
		return self._description_
	
	@description.setter
	def description(self, des):
		self._description_ = des

	@property
	def roleId(self):
		return self._roleid_ 
	
	@property
	def type(self):
		return self._role_type_ 
	
	@type.setter
	def type(self, newtype):
		self._role_type_  = newtype
	
	@property
	def resourceTypes(self):
		return self._resource_types_ 
	
	@resourceTypes.setter
	def resourceTypes(self, desc):
		self._description_ = desc

	@property
	def jsonTemplate(self):
		return '''{ "role": "{{ tvROLE }}",
			    "description" : "{{ tvDESCRIPTION }}",
			     "resourceTypes": [ 
				{{
				    tvRESOURCE_TYPES
				}}
	 	        ] }'''

	# Generate Json version of this object
	@property
	def dnacJson(self):

		# Generate stringified operations list...
		res_type_str = ''
		for next_rt  in self.resourceTypes:
			res_type_str +=  next_rt.dnacJson +  ','

		# Clip the trailing comma
		res_type_str = res_type_str[:-1]
		return Template(self.jsonTemplate).render(tvROLE = self.role,  tvDESCRIPTION = self.description, tvRESOURCE_TYPES = res_type_str)

	# Print out the object
	def __str__(self):
		return ('<Role: Name = ' + self.name + ', Id = ' + self.roleId if self.roleId else '<None>' + ', Descr = ' + self.description + '>')
		#print('Res Type = ' + self.resourceType)

#
if __name__ == "__main__":
	jsonx = '''
{"role":"bajjiRole","description":"Bajji","resourceTypes":[{"type":"Assurance","operations":["gRead"]},{"type":"Assurance.Monitoring and Troubleshooting","operations":["gRead"]},{"type":"Assurance.Monitoring Settings","operations":["gRead"]},{"type":"Assurance.Troubleshooting Tools","operations":["gRead"]},{"type":"Network Design.Advanced Network Settings","operations":["gRead"]},{"type":"Network Design.Image Repository","operations":["gRead"]},{"type":"Network Design.Network Hierarchy","operations":["gRead","gCreate","gUpdate","gRemove"]},{"type":"Network Design.Network Profiles","operations":["gRead"]},{"type":"Network Design.Network Settings","operations":["gRead"]},{"type":"Network Design.Network Telemetry","operations":["gRead"]},{"type":"Network Design.Virtual Network","operations":["gRead"]},{"type":"Network Provision","operations":["gRead"]},{"type":"Network Provision.Image Update","operations":["gRead"]},{"type":"Network Provision.Inventory Management","operations":["gRead"]},{"type":"Network Provision.License","operations":["gRead"]},{"type":"Network Provision.PnP","operations":["gRead"]},{"type":"Network Provision.Provision","operations":["gRead"]},{"type":"Utilities.Scheduler","operations":["gRead"]},{"type":"Network Services","operations":["gRead"]},{"type":"Network Services.App Hosting","operations":["gRead"]},{"type":"Network Services.Bonjour","operations":["gRead"]},{"type":"Network Services.Cloud Connect","operations":["gRead"]},{"type":"Network Services.Stealthwatch","operations":["gRead"]},{"type":"Network Services.Umbrella","operations":["gRead"]},{"type":"Security","operations":["gRead"]},{"type":"Security.Group-Based Policy","operations":["gRead"]},{"type":"Security.IP Based Access Control","operations":["gRead"]},{"type":"Security.Security Advisories","operations":["gRead"]},{"type":"System.Basic","operations":["gRead","gCreate","gUpdate","gRemove"]},{"type":"System.Machine Reasoning","operations":["gRead"]},{"type":"System.System Management","operations":["gRead"]},{"type":"Utilities","operations":["gRead"]},{"type":"Utilities.Audit Log","operations":["gRead"]},{"type":"Utilities.Network Reasoner","operations":["gRead"]},{"type":"Utilities.Report","operations":["gRead"]},{"type":"Utilities.Search","operations":["gRead"]}]}
		'''
	
	myrole = Role.parseJson(jsonx)
	print(myrole)
	print(str(myrole))

	# Regenerate Json
	xx = myrole.dnacJson
	print('generated Json')
	print(xx)
