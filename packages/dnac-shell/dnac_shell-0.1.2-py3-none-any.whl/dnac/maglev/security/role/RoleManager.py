import requests 
import json
from dnac.exception import DnacException
from dnac.exception import InvalidCriterionException
from dnac.maglev.security.role.ResourceType import ResourceType 
from dnac.maglev.security.role.Role import Role 
from dnac.maglev.security import SecurityManager

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class RoleManager:
	def __init__(self,maglev):
		self._maglev_ = maglev

#
	@property
	def dnacSecurityManager(self):
		return self._maglev_.security_manager 
#
	@property
	def urlListRoles(self):
		return  '/api/system/v1/identitymgmt/roles'
#
	@property
	def urlCreateRoles(self):
		return  '/api/system/v1/identitymgmt/role/resource-types'
#
	def urlDeleteRole(self, role_id):
		return  '/api/system/v1/identitymgmt/role/' + role_id.strip() if role_id and role_id.strip() else None
#
	def discover_roles(self, order_by = 'id'):
		roleresp = self.dnacSecurityManager.call_dnac( self.urlListRoles)
		if roleresp.status_code != 200:
			return None
		rolesres = json.loads(roleresp.text)
		rolesjson = rolesres['response']['roles']
		roleslist = [ Role.parseJson(role_json) for role_json in rolesjson ]
		if order_by == 'id':
			kvpair = [ (role.roleId, role) for role in roleslist ]
		elif order_by == 'name':
			kvpair = [ (role.name, role) for role in roleslist ]
		else:
			raise InvalidCriterionException('Request to find role with invalid name')
			
		return dict(kvpair)

	#
	# Find with the given name
	#
	def find_role_by_name(self, given_role_name):
		if not given_role_name or not given_role_name.strip():
			raise InvalidCriterionException('Request to find role with invalid name')

		roles = self.discover_roles(order_by = 'name')
		return roles[given_role_name] if roles and len(roles) > 0 and given_role_name in roles.keys() else None

	#
	# Find with the role id
	#
	def find_role_by_id(self, given_role_id):
		if not given_role_id or not given_role_id.strip():
			raise InvalidCriterionException('Request to find role with invalid id')

		roles = self.discover_roles(order_by = 'id')
		return roles[given_role_id] if roles and len(roles) > 0 and given_role_id in roles.keys() else None

	#
	# Create a custom role with the given parameters
	#
	def create_role(self, thisRole):
		if thisRole:
			resp = self.dnacSecurityManager.post_to_dnac(self.urlCreateRoles, thisRole.dnacJson, operation = 'put')
			print('creat role')
			print(resp.status_code)
			print(resp.text)
			print(resp.headers)
			print('----')
			if resp.status_code == 200:
				respjson = json.loads(resp.text)
				if not 'response' in respjson:
					return {'error' : 'POST response invalid: ' + str(respjson) }
				if not 'roleId' in respjson['response']:
					return {'error' : 'POST response invalid: ' + str(respjson) }

				return { 'roleId': respjson['response']['roleId'] }
			else:	
				return {'error' : 'POST failed with http/' + str(resp.status_code), 'roleId': 0 }
			
		raise ValueError('Request to create Invalid or None role - ignored')
	
	#
	# Delete the specified custom role 
	#
	def delete_role(self, role_id):
		'''
		Delete the specified custom role 
		'''
		if role_id and role_id.strip():
			the_dnac_url = self.urlDeleteRole(role_id=role_id)
			resp = self.dnacSecurityManager.post_to_dnac(url=the_dnac_url, json_payload = '', operation = 'delete')
			if resp.status_code == 200:
				respjson = json.loads(resp.text)
				if not 'response' in respjson:
					return {'error' : 'DELETE response invalid: ' + str(respjson) }
				if not 'roleId' in respjson['response']:
					return {'error' : 'DELETE response invalid: ' + str(respjson) }

				return { 'roleId': respjson['response']['roleId'] }
			else:	
				return {'error' : 'DELETE failed with http/' + str(resp.status_code), 'roleId': 0 }
			
		raise ValueError('Request to delete Invalid or None role - ignored ' )
	
#
if __name__ == "__main__":
	m = SecurityManager.SecurityManager('192.168.117.50')
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
