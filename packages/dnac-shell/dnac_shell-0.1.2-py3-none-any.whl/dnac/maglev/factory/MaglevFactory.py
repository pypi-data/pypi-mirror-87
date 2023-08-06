from collections import namedtuple
from typing import NamedTuple
from dnac.maglev.security.SecurityManager import SecurityManager
from dnac.maglev.security.role.RoleManager import RoleManager
from dnac.maglev.security.user.UserManager import UserManager
from dnac.maglev.task.TaskManager import TaskManager
from dnac.maglev.kernel.MaglevKernel import MaglevKernel as Kernel


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class MaglevFactory:
    '''
    	Factory to instantiate the singleton Maglev instance for DnacCluster
	'''

    @staticmethod
    def makeMaglevInstance(dnac_ip, admin_credentials):
        '''
		Instantiate a maglev entity with framework services
		'''

        # 'Maglev' named tuple denotes the Maglev kernel instance in
        # the DNAC cluster
        #
        Maglev = namedtuple('Maglev', 'ip kernel securityManager roleManager userManager taskManager')

        Maglev.ip = dnac_ip
        Maglev.kernel = Kernel(Maglev)
        Maglev.security_manager = SecurityManager(Maglev, admin_credentials)
        Maglev.role_manager = RoleManager(Maglev)
        Maglev.user_manager = UserManager(Maglev)
        Maglev.task_manager = TaskManager(Maglev)

        return Maglev
