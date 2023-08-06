from collections import namedtuple
from dnac.service.GroupingService import GroupingService
from dnac.service.FileService import FileService
from dnac.service.MapService import MapService

class ServicesFactory:
	'''
    	Factory to instantiate the singleton Application Services collection
	'''

	@staticmethod
	def makeServicesInstance(maglev):
		'''
		Instantiate a application services collection 
		'''

		# 'Services' named tuple denotes the Services kernel instance in
		# the DNAC cluster
		#
		Services = namedtuple('Services' , 'maglev groupingService mapService fileService')

		Services.maglev = maglev
		Services.groupingService = GroupingService(maglev)
		Services.mapService = MapService(Services)
		Services.fileService = FileService(Services)

		return Services

