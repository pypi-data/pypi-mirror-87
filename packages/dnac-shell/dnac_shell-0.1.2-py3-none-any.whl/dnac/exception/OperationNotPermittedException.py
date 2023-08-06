from dnac.exception.DnacException  import DnacException

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class OperationNotPermittedException(DnacException):
   """Exception indicates that the requested/attempted operation was not permitted """
   pass

if __name__ == "__main__":
	m = DnacException('Hello')
	print( 'Exception ->')
	print( m)
