import json
from jinja2 import Template
from dnac.maglev.security.role.Role import Role
from dnac.maglev.security.role.ResourceType  import ResourceType
from dnac.maglev.security.role.RoleManager import RoleManager
from dnac.maglev.security.SecurityManager import SecurityManager

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class User:
	def __init__(self, name, password, role, first_name, last_name):
		self._name_ = name
		self._password_ = password
		self._fn_ = first_name
		self._ln_ = last_name
		if role and not isinstance(role, Role):
			raise ValueError('Role must be of type "Role"')

		self._role_  = role

	@property
	def name(self):
		return self._name_
	
	@property
	def password(self):
		return self._password_

	@property
	def firstName(self):
		return self._fn_
	
	@property
	def lastName(self):
		return self._ln_
	
	@property
	def role(self):
		return self._role_
	
	@role.setter 
	def role(self, the_role):
		if not isinstance(the_role, Role):
			raise ValueError('Role must be of type "Role"')
		
		self._role_ = the_role
	
	@property
	def jsonTemplate(self):
		return '''{ "username": "{{ tvUSERNAME }}",
			    "passphrase" : "{{ tvPASSWORD }}",
			    "firstName" : "{{ tvFIRST_NAME }}",
			    "lastName" : "{{ tvLAST_NAME }}",
			     "roleList": [ 
				"{{
				    tvROLE_LIST
				}}"
	 	        ] }'''

	# Generate Json version of this object
	@property
	def dnacJson(self):
		return Template(self.jsonTemplate).render(
						tvUSERNAME = self.name,  
						tvPASSWORD = self.password, 
						tvROLE_LIST = self.role.roleId,
						tvFIRST_NAME = self.firstName,
						tvLAST_NAME = self.lastName)

	# Parse the entity Json returned by DNAC and recreate the object
	#
	@classmethod
	def parseJson(cls, userjson):
		if userjson:
			if not userjson or not isinstance(userjson, dict):
				raise ValueError('User Json is invalid: should be a non-null dict of attibute/value pairs: ' + str(userjson))
			elif not 'username' in userjson or not 'roleList' in userjson or not 'firstName' in userjson or not 'lastName' in userjson:
				raise ValueError('Invalid user Json received - user attributes missing: ' + jsonx)

			rolelist = userjson['roleList']
			username = userjson['username']
			user_id = userjson['userId']
			first_name = userjson['firstName']
			last_name = userjson['lastName']
			return cls(username, None, None, first_name, last_name)
		else:
			return None


	# Print out the object
	def print(self):
		print('==== Role ===')
		print('Name = ' + self.name)
		print('Role name = ' + self.role.name)
		print('Role id = ' + self.role.roleId)
		print('First Name id = ' + self.firstName)
		print('Last Name id = ' + self.lastName)
		print('=============')

#
if __name__ == "__main__":
	m = SecurityManager('192.168.117.50')
	m.adminCredentials = ('admin', 'Maglev123')

	rm = RoleManager(m)
	myrole = rm.find_role_by_name('RohanRole')
	if myrole:
		print("Deleting : " + myrole.roleId + ", " + myrole.name )
		resp = rm.delete_role(myrole.roleId)
		err_key ='error' 
		if err_key in resp.keys(): 
			print('Delete of role ' + myrole.roleId + ' failed')
		else:	
			print('Role ' + myrole.name + ' deleted!')
		
	print ('After attempted delete of role Roles === '  )
	roles =  rm.discover_roles()
	for key, obj in roles.items():
		obj.print()

	myrole = Role('RohanRole', 'Rohans ROle in GaTTech', ' ', 'CUSTOM', 
			[ ResourceType('Network Design.Network Hierarchy', ['gCreate', 'gRead']) ]
		)

	resp = rm.create_role(myrole)
	print(resp)

	print ('After adding new role Roles === '  )
	roles =  rm.discover_roles()

	for key, obj in roles.items():
		obj.print()

	rohan = User('RohanRk', 'StrongK!d123', myrole, 'AmalaPaul', 'Veriyan')
	jsonx = rohan.dnacJson
	
	
