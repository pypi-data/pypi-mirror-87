import json
from jinja2 import Template
from dnac.maglev.security.SecurityManager import SecurityManager

class CalibrationModel:
	def __init__(self, name, id = 0, status = 2 ):
		self._name_ = name
		self._id_ = id
		self._status_ = status

	@property
	def name(self):
		return self._name_
	
	@property
	def id(self):
		return self._id_

	@property
	def status(self):
		return self._status_
	
	# Parse the entity Json returned by DNAC and recreate the object
	#
	@classmethod
	def parseJson(cls, cbjsonstr):
		cbs = json.loads(cbjsonstr)
		if isinstance(cbs, list):
			return [ cls(cb['name'], cb['id'], cb['status']) for cb in cbs]

		return cls(cbs['name'], cbs['id'], cbs['status']) if isinstance(cbs, dict) else None

	def _eq_(self, other):
		return self.id == other.id

	# Print out the object
	def _str_(self):
		return '<Id = ' + str(self.id) + ' , Name = ' + self.name + '>'

#
