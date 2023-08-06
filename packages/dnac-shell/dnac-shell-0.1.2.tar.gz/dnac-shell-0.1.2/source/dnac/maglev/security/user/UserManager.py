import requests

import requests 
import json
from dnac.exception import DnacException
from dnac.exception import InvalidCriterionException
from dnac.exception import InvalidUserException
from dnac.maglev.security.role.ResourceType import ResourceType 
from dnac.maglev.security.role.Role import Role 
from dnac.maglev.security.role.RoleManager import RoleManager
from dnac.maglev.security import SecurityManager
from dnac.maglev.security.user.User import User
  
# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class UserManager:
	def __init__(self,maglev):
		self._maglev_ = maglev

	@property
	def dnacRoleManager(self):
		return self._maglev_.role_manager
#
	@property
	def dnacSecurityManager(self):
		return self._maglev_.security_manager
#
	@property
	def urlListUsers(self):
		return  '/api/system/v1/identitymgmt/users'
#
	@property
	def urlCreateUser(self):
		return  '/api/system/v1/identitymgmt/user'
#
	def urlDeleteUser(self, user_id):
		return '/api/system/v1/identitymgmt/user/' + user_id
#
	def discover_users(self, order_by = 'name'):
		useresp = self.dnacSecurityManager.call_dnac( self.urlListUsers)
		if useresp.status_code != 200:
			return None
		usersres = json.loads(useresp.text)
		usersjson = usersres['response']['users']
		userslist = [ User.parseJson(user_json) for user_json in usersjson ]
		if order_by == 'id':
			kvpair = [ (user.userId, user) for user in userslist ]
		elif order_by == 'name':
			kvpair = [ (user.name, user) for user in userslist ]
		else:
			raise InvalidCriterionException('Request to find user with invalid name')
			
		return dict(kvpair)

	#
	# Find with the given name
	#
	def find_user_by_name(self, given_user_name):
		if not given_user_name or not given_user_name.strip():
			raise InvalidCriterionException('Request to find user with invalid name')

		users = self.discover_users()
		return users[given_user_name] if users and len(users) > 0 and given_user_name in users.keys() else None

	#
	# Create the given  user 
	#
	def create_user(self, this_user):
		if this_user:
			resp = self.dnacSecurityManager.post_to_dnac(self.urlCreateUser, this_user.toDnacJson())
			if resp.status_code == 200:
				respjson = json.loads(resp.text)
				if not 'response' in respjson:
					return {'error' : 'POST response invalid: ' + str(respjson) }
				if not 'userId' in respjson['response']:
					return {'error' : 'POST response invalid: ' + str(respjson) }

				return { 'userId': respjson['response']['userId'] }
			return {'error' : 'POST failed with http/' + str(resp.status_code) }
			
		raise ValueError('Request to create Invalid or None user - ignored')
	
	#
	# Delete the specified user
	#
	def delete_user_using_id(self, user_id):
		if user_id and user_id.strip():
			the_dnac_url = self.urlDeleteUser(user_id=user_id)
			resp = self.dnacSecurityManager.post_to_dnac(url=the_dnac_url, json_payload = '', operation = 'delete')
			if resp.status_code == 200:
				respjson = json.loads(resp.text)
				if not 'response' in respjson:
					return {'error' : 'DELETE response invalid: ' + str(respjson) }

				return { 'message': respjson['response']['message'] }
			else:	
				return {'error' : 'DELETE failed with http/' + str(resp.status_code) }
			
		raise ValueError('Request to delete Invalid or None user - ignored ' )
	
	#
	# Delete the specified user using user's name
	#
	def delete_user_using_name(self, given_user_name):
		user_id = self.find_user_by_name( given_user_name)
		if user_id:
			return delete_user_using_id(user_id)

		raise InvalidUserException('Username "' + given_user_name + '" is invalid or non-existant')
#
if __name__ == "__main__":
	m = SecurityManager.SecurityManager('192.168.117.50')
	m.adminCredentials = ('admin', 'Maglev123')

	rm = RoleManager(m)
	myrole = Role('RohanRole', 'Rohans ROle in GaTTech', ' ', 'CUSTOM', 
			[ ResourceType('Network Design.Network Hierarchy', ['gCreate', 'gRead']) ]
		)

	resp = rm.create_role(myrole)
	print(resp)

	print ('After adding new role Roles === '  )
	roles =  rm.discover_roles()

	myrole = rm.find_role_by_name('RohanRole')

	myrole.print()
	um = UserManager(rm)
	rohan = User('RohanRk', 'StrongK!d123', myrole, 'AmalaPaul', 'Veriyan')
	jsonx = rohan.toDnacJson()
	print(jsonx)

	if um.find_user_by_name('RohanRk'):
		# Delete the user first, if he exists
		try:
			um.delete_user_using_name('RohanRk')
		except:	
			# User exists but cannot delete - dont try to create the user id
			print(' User exists but cannot delete - dont try to create the user id')
			quit()
		
	resp = um.create_user(rohan)
	print('Create respons efor user ' )
	print(resp)

	# Now login as Rohan
	rohan_token = m.getAuthTokenFor( (rohan.name, rohan.password) )
	print('Rohan xuath token = ' )
	print(rohan_token)

