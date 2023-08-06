#
# This entity denotes the DNAC Platform object, which is a part  of DNAC cluster
# 
# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com
#
from dnac.maglev.factory.MaglevFactory import MaglevFactory 
from dnac.service.factory.ServicesFactory import ServicesFactory 
from dnac.maglev.security.SecurityManager import SecurityManager 
from dnac.service.GroupingService import GroupingService 
from dnac.service.site.Site import Site
from dnac.service.maps.Floor import Floor
from dnac.service.maps.FloorGeometry import FloorGeometry
from dnac.service.site.Building import Building
from dnac.service.site.Building import Building
from dnac.service.MapService import MapService 
from dnac.maglev.security.role.factory.RoleFactory import RoleFactory
from dnac.maglev.security.role.RoleManager import RoleManager
from dnac.maglev.security.role.Role import Role
from dnac.maglev.security.Session import Session

class DnacPlatform:
	def __init__(self,maglev):
		self._maglev_ = maglev
#
	@property
	def dnacSecurityManager(self):
		return self._maglev_.security_manager

	@staticmethod
	def urlOfFloorId(self, floorid):
		return '/dna/intent/api/v1/wireless/floormap/' + str(floorid).strip() if floorid  else None
#
	@staticmethod
	def urlOfFloor(floor):
		return urlOfFloorId(str(floor.id).strip()) if floor and floor.id  else None

	@property
	def urlListFloors(self):
		return  '/dna/intent/api/v1/wireless/floormap/all'

	@staticmethod
	def urlCreateFloor(self, buildingid):
		return  '/dna/intent/api/v1/wireless/floormap' + buildingid


	#
	# Get the specified floor
	#
	def get_floor(self, floorid):
		pass

	#
	# Create a floor with the given parameters
	#
	def create_floor(self, floor):
		if site:
			# Create the async task...
			pass
			
		raise ValueError('Request to create Invalid site - ignored')
	

	#
	# Delete specified floor
	#
	def delete_floor(self, floor):
		if floor and site.url:
			pass

		raise ValueError('Request to delete Invalid or non-existant floor ')
