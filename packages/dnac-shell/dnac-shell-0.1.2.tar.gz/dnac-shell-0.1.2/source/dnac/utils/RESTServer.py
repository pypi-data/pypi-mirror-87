#
# This entity denotes a simple REST server that is used to implement 
# callbacks. THis forms the underpinning of the request with
# callbacks sent to DNAC Platform
#
# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com
#

import os
import bottle
from bottle import route, run, request

import requests
import json
from jinja2 import Template

#from dnac.exception importx DnacException
#from dnac.exception importx InvalidCriterionException
#from dnac.service.site.Site importx Site
#from dnac.service.maps.Floor importx Floor
#from dnac.service.maps.FloorGeometry importx FloorGeometry
#from dnac.service.site.Building importx Building
#from dnac.service.site.Building importx Building
#from dnac.service.MapService importx MapService
#from dnac.maglev.security.Session importx Session

# copyright (c) 2019 cisco Systems Inc., ALl righhts reseerved

class RESTServer:
	def __init__(self,service_address, service_port = 8080):
		self._ip_ = service_address
		self._port_ = 8080 if service_port <= 0 else service_port
		self._data_ = ''
		self._protocol_ = 'http'

	@property
	def protocol(self):
		return self._protocol_

		
	@property
	def ip(self):
		return self._ip_

	@property
	def port(self):
		return self._port_

	@property
	def handler_url(self):
		return '/floor/callback'

	@property
	def data(self):
		return self._data_

	@data.setter
	def data(self, x):
		self._data_ = x

	def floorcreate(self):
		for l in request.body:
        		print (l)

		self.data = request.body.readlines()
		print (self.data)

	@property
	def jsonTemplate(self):
		return '''{ "uri": "{{ tvPROTOCOL }}:{{ tvIP }}:{{ tvPORT }}/{{ tvHANDLER_URL }}",
			    "headers" : [
			    	{ "header" : "{{ tvHEADER_NAME1 }}", "value":"{{ tv_HEADER_VALUE1 }}" },
			    	{ "header" : "{{ tvHEADER_NAME2 }}", "value":"{{ tv_HEADER_VALUE2 }}" },
			    	{ "header" : "{{ tvHEADER_NAME3 }}", "value":"{{ tv_HEADER_VALUE3 }}" },
			    	{ "header" : "{{ tvHEADER_NAME4 }}", "value":"{{ tv_HEADER_VALUE4 }}" }
	 	        ] }'''

	# Generate Json version of this object
	@property
	def dnacJson(self):
		return Template(self.jsonTemplate).render(
						tvPROTOCOL = self.protocol,  
						tvIP = self.ip,  
						tvPORT = self.port,  
						tvHANDLER_URL = self.handler_url, 
						tvHEADER_NAME1 = 'X-header1',
						tvHEADER_NAME2 = 'X-my-header2',
						tvHEADER_NAME3 = 'X-my-header3',
						tvHEADER_NAME4 = 'X-my-header4',
						tvHEADER_VALUE1 = 'Om Namah Sivayah',
						tvHEADER_VALUE2 = 'Om Namah Sivayah',
						tvHEADER_VALUE3 = 'Om Namah Sivayah',
						tvHEADER_VALUE4 = 'Om Namah Sivayah')


	# Activate the REST server
	def activate(self):
		bottle.route(self.handler_url, method='POST', callback=self.floorcreate)
		bottle.run(host=self.ip, port = self.port, debug=True)


