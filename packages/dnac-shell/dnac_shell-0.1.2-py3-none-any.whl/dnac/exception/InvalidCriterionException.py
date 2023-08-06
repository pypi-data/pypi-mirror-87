from dnac.exception.DnacException  import DnacException 

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class InvalidCriterionException(DnacException):
   """User specified data invalid filtering criterin """
   pass

if __name__ == "__main__":
	m = InvalidCriterionException("Invalid!!!")
	print( 'Exception ->')
	print( m)
