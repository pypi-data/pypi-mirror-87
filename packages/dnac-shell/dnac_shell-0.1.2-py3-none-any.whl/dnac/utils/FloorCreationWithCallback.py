#
# This entity denotes a floor creation request that has an associated
# task cokmpletion callback. The entity is submitted (POSTed) to
# DNAC Platform (a a prt of DnacCluster), which then invokes
# the associated callback to signal success or failure.
#
# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com
#
import os
import threading
import requests
import json
from jinja2 import Template
from RESTServer import RESTServer

#from dnac.exception importx DnacException
#from dnac.exception importx InvalidCriterionException
#from dnac.service.site.Site importx Site
from dnac.service.maps.Floor import Floor
from dnac.service.maps.FloorGeometry import FloorGeometry
#from dnac.service.site.Building importx Building
#from dnac.service.site.Building importx Building
#from dnac.service.MapService importx MapService
#from dnac.maglev.security.Session importx Session


class FloorCreationWithCallback:
	def __init__(self,given_floor, service_address, service_port = 8080):
		self._callback_handler_ = RESTServer( service_address, service_port )
		self._floor_ = given_floor

	@property
	def floor(self):
		return self._floor_
		
	@property
	def callback_handler(self):
		return self._callback_handler_ 

	@property
	def callback_data(self):
		return self.callback_handler.data

	@property
	def jsonTemplate(self):
		return '''{ "floor": {{ tvFLOOR }}, 
			    "callback" : {{ tvCALLBACK }}
	 	        }'''

	# Generate Json version of this object
	@property
	def dnacJson(self):
		return Template(self.jsonTemplate).render( 
				tvFLOOR = self.floor.dnacJson, 
				tvCALLBACK = self.callback_handler.dnacJson)

	@property
	def rest_task(self):
		return self._rest_task_

	@rest_task.setter
	def rest_task(self, this_task):
		self._rest_task_ = this_task


	# Activate the callback handler
	def activate(self):
		self.rest_task = threading.Thread(name = 'Floor Callback REST Server', target = self.spawn_rest_server)
		self.rest_task.start()


	# Terminate the callback handler
	def terminate(self):
		pass

	# Spawn REST Server
	def spawn_rest_server(self):
		self.callback_handler.activate()

#
#
if __name__ == "__main__":
	geom =  FloorGeometry(  110.0, 110.0, 9.0)
	floor = Floor( '0', 'F1', 'd5079be3-c8cf-4c03-85f9-6033678ca11b', geom,  'rks@cisco.com', '')

	server = FloorCreationWithCallback(floor, 'localhost')
	print(server.dnacJson)

	#print(server.callback_data)
