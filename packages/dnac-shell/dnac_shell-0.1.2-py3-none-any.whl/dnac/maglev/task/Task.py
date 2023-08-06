
import requests 
import json

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class Task:
	"""
	Task entity represents the DNAC async task containing the task ID and its URL.
	"""

	def __init__(self, task_id):
		self._id_ = task_id.strip() if task_id else None
		self.startTime = 0
		self.endTime = 0
		self.isError = False

	@property
	def id(self):
		return self._id_
	
	@staticmethod
	def baseUrl():
		return '/api/v1/task' 

	@property
	def url(self):
		return Task.baseUrl() + '/' + self.id.strip()

	@property
	def isError(self):
		return self._error_ 

	@isError.setter
	def isError(self, status):
		self._error_ = status

	@property
	def startTime(self):
		return self._st_

	@startTime.setter
	def startTime(self, x):
		self._st_ = x

	@property
	def endTime(self):
		return self._et_

	@endTime.setter
	def endTime(self, x):
		self._et_ = x

	@property
	def data(self):
		return self._data_

	@property
	def isComplete(self):
		return True if self.startTime and self.endTime else False

	@data.setter
	def data(self, x):
		self._data_  = x

	@classmethod
	def parseJson(cls, jsonstr):
		if jsonstr:
			taskattr = json.loads(jsonstr)
			if isinstance(taskattr, dict):
				#
				# Cull out all attributes oif task - either from task Json or
				# task response json
				#

				taskattr = taskattr['response'] if 'response' in taskattr.keys() else taskattr
				if 'taskId' in taskattr.keys():
					task = cls(taskattr['taskId'])
				elif 'id' in taskattr.keys():
					task = cls(taskattr['id'])
				else:
					raise ValueError('Task id not found in task json - invalid task json')

				task.isError = taskattr['isError'] if 'isError' in taskattr.keys() else None
				task.startTime = taskattr['startTime'] if 'startTime' in taskattr.keys() else None
				task.endTime = taskattr['endTime'] if 'endTime' in taskattr.keys() else None
				task.data = taskattr['data'] if 'data' in taskattr.keys() else None
				return task


		raise ValueError('Invalid task json')
	
#
	def __str__(self):
		return '<id = ' + str(self.id) + ', Url = ' + self.url + ', isError = ' + str(self.isError) + ', data = ' + str(self.data) + ', isComplete = ' + str(self.isComplete) + '>'
