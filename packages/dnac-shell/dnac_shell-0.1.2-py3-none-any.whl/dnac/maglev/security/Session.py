
# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class Session:
	'''
		Session entity encapsulates the current user credentials and the current session auth token
	'''
	def __init__(self, credentials, auth_token):
		self._credentials_ = credentials
		self._auth_token_ = auth_token

	@property
	def credentials(self):
		return self._credentials_ 
	
	@property
	def authToken(self):
		return self._auth_token_ 
	
	@authToken.setter
	def authToken(self, new_token):
		self._auth_token_  = new_token

