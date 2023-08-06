from dnac.exception.DnacException  import DnacException

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class NoSessionException(DnacException):
	"""
		Exception indicates that there is no current login session using which to
		execute operations on DNAC cluster
	"""
	pass

if __name__ == "__main__":
	m = DnacException('Hello')
	print( 'Exception ->')
	print( m)
