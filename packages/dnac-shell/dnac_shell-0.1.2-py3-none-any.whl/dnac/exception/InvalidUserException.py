from dnac.exception.DnacException  import DnacException 

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class InvalidUserException(DnacException):
   """User specified user id is invalid """
   pass

if __name__ == "__main__":
	m = InvalidUserException("Invalid user 'rks' !!!")
	print( 'Exception ->')
	print( m)
