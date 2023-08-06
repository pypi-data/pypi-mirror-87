import json

# copyright (c) 2019 cisco Systems Inc., ALl righhts reseerved

class SiteParser:

	# Parse the site additional attributes tpo get site type
	#
	@staticmethod
	def parseSiteAttributes(cbjsonstr):
		cbs = json.loads(cbjsonstr) if isinstance(cbjsonstr, str) else cbjsonstr
		cbs = cbs['response'] if isinstance(cbs, dict) and 'response' in cbs.keys() else cbs
		if isinstance(cbs, list):
			cbs = cbs[0] if len(cbs) else None  # empty list

		if cbs:
			if cbs['groupNameHierarchy'] == 'Global':
				return 'area'
			
			if not 'additionalInfo' in cbs.keys():
				return 'area'

			ai = cbs['additionalInfo']
			for i in ai:
				attr = i['attributes']
				if i['nameSpace'] == 'Location':
					return attr['type']

		return None



#
if __name__ == "__main__":
	cbjson = '''
		[{"systemGroup":true,"groupHierarchy":"69444522-a32c-4e59-90fa-bad096537201","groupNameHierarchy":"Global","additionalInfo":[{"nameSpace":"System Settings","attributes":{"group.count.total":"2","hasChild":"TRUE","group.count.direct":"1","group.hierarchy.groupType":"SITE","member.count.total":"0","member.count.direct":"0"}}],"name":"Global","instanceTenantId":"SYS0","id":"69444522-a32c-4e59-90fa-bad096537201"}]
		'''

	model2 = Site.parseJson(cbjson)
	print('Model 2')
	print(type(model2))
	for i in model2:
		i.print()

	cbjson = '''
	{"response":[{"parentId":"69444522-a32c-4e59-90fa-bad096537201","systemGroup":false,"groupTypeList":["SITE"],"groupHierarchy":"69444522-a32c-4e59-90fa-bad096537201/ea91df3c-2b39-418c-89cf-a4ffdad133d4","groupNameHierarchy":"Global/AmalaPaul","additionalInfo":[{"nameSpace":"Location","attributes":{"addressInheritedFrom":"ea91df3c-2b39-418c-89cf-a4ffdad133d4","type":"area"}},{"nameSpace":"com.wireless.managingwlc","attributes":{"secondaryWlcInheritedFrom":"ea91df3c-2b39-418c-89cf-a4ffdad133d4","anchorWlcInheritedFrom":"ea91df3c-2b39-418c-89cf-a4ffdad133d4","tertiaryWlcInheritedFrom":"ea91df3c-2b39-418c-89cf-a4ffdad133d4","primaryWlcInheritedFrom":"ea91df3c-2b39-418c-89cf-a4ffdad133d4"}},{"nameSpace":"System Settings","attributes":{"group.count.total":"1","hasChild":"TRUE","group.count.direct":"1","group.hierarchy.groupType":"SITE","member.count.total":"0","member.count.direct":"0"}}],"name":"AmalaPaul","instanceTenantId":"5db7884336388b00b79e9d1b","id":"ea91df3c-2b39-418c-89cf-a4ffdad133d4"}],"version":"1.0"}
		'''

	model3 = Site.parseJson(cbjson)
	print('Model 3')
	print(type(model3))
	model3.print()
