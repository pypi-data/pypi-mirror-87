from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional, Tuple
from typing_extensions import Protocol
import getpass
from dnac.maglev.factory.MaglevFactory import MaglevFactory
from dnac.service.FileService import FileService
from dnac.service.GroupingService import GroupingService
from dnac.service.MapService import MapService
from dnac.service.factory.ServicesFactory import ServicesFactory
from dnac.service.site.Site import Site
from dnac.maglev.security.Session import Session
from dnac.platform.DnacPlatform import DnacPlatform


# copyright (c) 2020 cisco Systems Inc., All rights reseerved
# @author rks@cisco.com

class DnacCluster:
    def __init__(self, cluster_address : str, admin_credentials : Tuple[str, str]) -> None:
        self._ip_ = cluster_address  # socket.gethostbyname(address)
        self._version_ = None
        self._maglev_ = MaglevFactory.makeMaglevInstance(cluster_address, admin_credentials)
        self._services_ = ServicesFactory.makeServicesInstance(self.maglev)
        self._dnac_platform_ = DnacPlatform(self.maglev)
        self.global_site = self.groupingService.discover_global()

    @property
    def maglev(self):
        return self._maglev_

    @property
    def version(self) -> str:
        return self._version_

    @version.setter
    def version(self, theversion):
        self._version_ = theversion

    #
    @property
    def dnacSecurityManager(self):
        return self.maglev.security_manager

    #
    @property
    def dnacRoleManager(self):
        return self.maglev.role_manager

    #
    @property
    def dnacPlatform(self):
        return self._dnac_platform_

    #
    @property
    def address(self) -> str:
        return self.maglev.ip

    @property
    def services(self):
        return self._services_

    def setAdminCredentials(self, ac):
        self.dnacSecurityManager.setAdminCredentials(ac)

    #
    @property
    def groupingService(self) -> GroupingService:
        return self._services_.groupingService

    #
    @property
    def mapService(self) -> MapService:
        return self._services_.mapService

    @property
    def fileService(self) -> FileService:
        return self.services.fileService

    @property
    def global_site(self):
        return self._global_

    @global_site.setter
    def global_site(self, thesite):
        self._global_ = thesite

    @staticmethod
    def get_credentials() -> Tuple[str, str]:
        username = input('Administrator: [admin] ') or 'admin'
        passwordx = DnacCluster.get_password()
        return username, passwordx

    @staticmethod
    def get_password() -> str:
        return getpass.getpass()

    # Login to DNAC as the specified user
    def login_as(self, credentials) -> None:
        self.global_site = None
        self.dnacSecurityManager.session = Session(credentials, None)
        self.global_site = self.groupingService.discover_global()

    # Is logged in
    def valid_session(self) -> bool:
        return not (self.global_site is None)


#
if __name__ == "__main__":
    dnac_cluster = DnacCluster('192.168.117.50', ('admin', 'Maglev123'))

    globalx = dnac_cluster.groupingService.discover_global()
    print('Global site ->')
    globalx.print()

    st = Site(0, 'AmalaPaul', ' ', False, globalx.id)

    idx = dnac_cluster.groupingService.create_site(st)
    st.print()

    hier = 'Global/AmalaPaul'
    nsite = dnac_cluster.groupingService.discover_site_hierarchy(hier)
    if nsite:
        nsite.print()
    else:
        print('no such hierarchy - ' + hier)

    hier = 'Global/AmalaPaul/B'
    nsite = dnac_cluster.groupingService.discover_site_hierarchy(hier)
    if nsite:
        nsite.print()
    else:
        print('no such hierarchy - ' + hier)

    print('============================ Find Floor F1 ======')

# hier = 'Global/AmalaPaul/B/F1'
# floor =dnac_cluster.mapService.discover_floor( hier)
# if isinstance(floor, list):
# if not len(floor):
# print('No such floor')
# raise SystemExit
# for i in floor:
# if i:
# print(str(i))
# res = dnac_cluster.mapService.delete_floor( i)
# print('delete result = ' + str(res))
# else:
# print('empty floor')
# elif isinstance(floor, Floor):
# print('floor is site')
# if floor:
# print(str(floor))
# else:
# print('empty floor')
# else:
# print('NOTHING')

# geom =  FloorGeometry(  110.0, 110.0, 9.0)
# floor = Floor( '0', 'F1', 'd5079be3-c8cf-4c03-85f9-6033678ca11b', geom,  'rks@cisco.com', '')

# floor =dnac_cluster.mapService.create_floor( floor)
# print(' created floor -> ')
# print(type(floor))
# print(str(floor))

# hier = 'Global/AmalaPaul/B/F1'
# floor = dnac_cluster.groupingService.discover_site_hierarchy(hier)

# if floor:
# f = floor[0]
# f.name =  'OmNamahSivayah'
# print('floor id = ' + str(f.id))
# floor =dnac_cluster.mapService.update_floor( f)
# print(' updated floor -> ')
# print(type(f))
# print(str(f))

# Role
# therole = RoleFactory.makeCustomRole( 'MyCoolRole', 'My Cool Role',  ( 'Network Design.Netwok Hierarchy', ['gRead', 'gDelete', 'gCreate', 'gUpdate'] ))
# print (therole.dnacJson)

# print ('creating role')
# therole = dnac_cluster.dnacRoleManager.create_role(therole)
# print (str(therole))
