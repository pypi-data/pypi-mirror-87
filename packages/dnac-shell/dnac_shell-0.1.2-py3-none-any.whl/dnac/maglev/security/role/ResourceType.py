import json
from jinja2 import Template

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class ResourceType:
	def __init__(self,type, operations = list()):
		self._type_ = type
		self._operations_ = operations

	@property
	def Type(self):
		return self._type_
	
	@property
	def Operations(self):
		return self._operations_

	@Operations.setter
	def operations(self, given_operations):
		self._operations_ = given_operations

	@classmethod
	def parseJson(cls, jsonx):
		ops_list = []
		if jsonx:
			if isinstance(jsonx, str):
				jsonx = json.loads(jsonx)
			elif isinstance(jsonx, dict):
				if jsonx['operations']:
					for opx in jsonx['operations']:
						ops_list.append(opx)
			
				typex = jsonx['type']
				return cls(typex, ops_list)
			#
			else:
				raise ValueError('ResourceType Json is invalid: should be a non-null dict')

		else:
			return None

	@property
	def jsonTemplate(self):
		return '''{ "type" : "{{ tvRESOURCE_TYPE }}", "operations": [ {{ tvOPERATIONS }} ] }'''
	
	@property
	def dnacJson(self):

		# Generate stringified operations list...
		op_str = ''
		for next_op in self.Operations:
        		op_str += '"' + next_op + '"' + ','

		# Clip the trailing comma
		op_str = op_str[:-1]

		return Template(self.jsonTemplate).render(tvRESOURCE_TYPE = self.Type,  tvOPERATIONS = op_str )

#
if __name__ == "__main__":
	print ('Parsed res type === '  )
	js =  '''{  
                  "operations":[
                     "gRead",
                     "gCreate"
                  ],
                  "type":"Network Design.Network Hierarchy"
               }'''
	rst = ResourceType.parseJson(js)
	print ('class Type === '  )
	print(type(rst))
	print ('Type === '  )
	print(rst.Type)
	print ('Ops === '  )
	print(rst.Operations)

	print('json temp')
	print(rst.dnacJson)
