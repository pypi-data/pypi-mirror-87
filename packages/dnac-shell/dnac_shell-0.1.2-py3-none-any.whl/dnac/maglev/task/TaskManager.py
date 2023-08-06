import requests
import json
from dnac.maglev.security import SecurityManager
from dnac.maglev.task.Task import Task

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class TaskManager:
    '''
		TaskManager denotes the task service entity of Maglev. 
		:param arg: The arg is used for ...
		:type arg: str
		:param `*args`: The variable arguments are used for ...
		:param `**kwargs`: The keyword arguments are used for ...
		:ivar arg: This is where we store arg
		:vartype arg: str
	'''

    def __init__(self, maglev):
        self._maglev_ = maglev

    @property
    def dnacSecurityManager(self):
        return self._maglev_.security_manager

    #
    #
    @staticmethod
    def parse_async_response(taskjson):
        '''
		This static method parses the task json retirned by a DNAC service and follows the task to conclusion

		:param taskjson: The Json string that denotes the task
		:type : str
		:raises: :class:`ValueError`: Invalida result
		:returns: Task entity
		:rtype: Task

		'''
        task_dict = json.loads(taskjson)
        if not 'response' in task_dict.keys():
            raise ValueError('Invalid async response: expected task response - got: ' + taskjson)

        task_details = task_dict['response']
        if 'data' in task_details.keys():
            return {'data': task_details['data'], 'completed': True}
        elif 'taskId' in task_details.keys() and 'url' in task_details.keys():
            return {'url': task_details['url'], 'completed': None}

        raise ValueError('Invalid async response: expected task id in response - got: ' + taskjson)

    def follow_task(self, task):
        '''
			This method tracks a task to conlcusion of the task (either success or failure) and returns
			the computed data from the data field of the task.

			:param task: Either task object or the Json string that denotes the task
			:type : Task or str
			:raises: :class:`ValueError`: Invalid task
			:returns: String data compirising the resylt of the task
			:rtype: str
		'''

        if not isinstance(task, Task):
            raise ValueError('Invalid task response: expected task object in response - got: ' + task)

        for i in range(500):
            if task and task.isComplete is True:
                return task.data
            response = self.dnacSecurityManager.call_dnac(task.url)
            if response.status_code != 200:
                print('follow task ', response.status_code, response.text)
                return None

            # Expect a task response - follow the taskid to completion
            #
            task = Task.parseJson(response.text)

        print('Abnormal exit: out of follow task ', task.url, task.isComplete, task.isError, task.data)
        raise ValueError('Async task failed to complete - could not create site')

#
