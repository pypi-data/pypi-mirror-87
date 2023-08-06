import json
from jinja2 import Template
from dnac.service.site.util.SiteParser import SiteParser

# copyright (c) 2019 cisco Systems Inc., ALl righhts reseerved

class FloorGeometry:
	'''
		This entity denoytes the floor geometry
	'''
	def __init__(self, length, width, height, x = 0.0, y = 0.0):
		self._l_ = length
		self._w_ = width
		self._h_ = height
		self._x_ = x
		self._y_ = y

	@classmethod
	def from_tuple(cls, dimension):
		return cls(dimension[1], dimension[0], dimension[2]) # length, width, height

	@property
	def x(self):
		return self._x_ 

	@x.setter
	def id(self, x):
		self._x_ = x

	@property
	def y(self):
		return self._y_ 

	@y.setter
	def id(self, y):
		self._y_ = y

	@property
	def length(self):
		return self._l_ 

	@length.setter
	def id(self, length):
		self._l_ = length

	@property
	def width(self):
		return self._w_ 

	@width.setter
	def id(self, width):
		self._w_ = width

	@property
	def height(self):
		return self._h_ 

	@height.setter
	def id(self, height):
		self._h_ = height

	@property
	def jsonTemplate(self):
		return '''
	{ "type": "DUMMY", "length":"{{ tvLENGTH }}", "width":"{{ tvWIDTH }}", "height":"{{ tvHEIGHT }}", "offsetX":"{{ tvX }}", "offsetY":"{{ tvY }}" }
	 	       '''

	# Generate Json version of this object
	@property
	def dnacJson(self):
		# Generate stringified operations list...
		return Template(self.jsonTemplate).render( tvLENGTH = self.length,  tvWIDTH = self.width,  tvHEIGHT = self.height,  tvX = self.x  , tvY = self.y  ).strip()


	# Parse the floor geometry attributes to get dimensions
	#
	@staticmethod
	def parseJson(cbjsonstr):
		cbs = json.loads(cbjsonstr) if isinstance(cbjsonstr, str) else cbjsonstr
		cbs = cbs['response'] if isinstance(cbs, dict) and 'response' in cbs.keys() else cbs
		if cbs:
			print(cbs)
			if 'length' in cbs.keys() and 'width' in cbs.keys() and 'height' in cbs.keys() and 'offsetX' in cbs.keys() and 'offsetY' in cbs.keys():
				return FloorGeometry( cbs['length'], cbs['width'], cbs['height'], cbs['offsetX'], cbs['offsetY'])

		return None

