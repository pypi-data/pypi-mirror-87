# copyright (c) 2019-20 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

import requests
import json
from dnac.exception import DnacException
from dnac.exception import InvalidCriterionException
from dnac.maglev.security import SecurityManager
from dnac.service.site.Site import Site
from dnac.service.site.Building import Building
from dnac.service.site.util.SiteParser import SiteParser
from dnac.service.site.factory.SiteFactory import SiteFactory
from dnac.maglev.task.TaskManager import TaskManager
from dnac.maglev.task.Task import Task


class GroupingService:
    def __init__(self, maglev):
        self._maglev_ = maglev

    #
    @property
    def dnacSecurityManager(self):
        return self._maglev_.security_manager

    #
    @property
    def dnacTaskManager(self):
        return self._maglev_.task_manager

    #
    @property
    def urlListGlobalSite(self):
        return '/api/v1/group?groupName=Global'

    @property
    def urlCreateSite(self):
        return '/api/v1/group'

    @staticmethod
    def urlGetSiteHierarchyUrl(site_hier_name):
        return '/api/v1/group?groupNameHierarchy=' + site_hier_name.strip() if site_hier_name and site_hier_name.strip() else None


    @staticmethod
    def urlGetSiteUrl(site_id):
        return '/api/v1/group/' + site_id.strip() if site_id and site_id.strip() else None

    @staticmethod
    def urlGetSiteChildrenUrl(site_id):
        return GroupingService.urlGetSiteUrl(site_id) + '/child'

    #
    # Get the specified Site
    #
    def discover_site(self, site_id):
        siteresp = self.dnacSecurityManager.call_dnac(GroupingService.urlGetSiteUrl(site_id))
        return SiteFactory.makeSite(siteresp.text) if siteresp.status_code == 200 else None

    #
    # Get the children of the specified Site
    #
    def discover_site_children(self, site_id):
        siteresp = self.dnacSecurityManager.call_dnac(GroupingService.urlGetSiteChildrenUrl(site_id))
        if siteresp.status_code != 200:
            return None
        cbs = json.loads(siteresp.text)
        return [ SiteFactory.makeSite(json.dumps(nextchildjson)) for nextchildjson in cbs['response']]

    #
    # Get the specified Site
    #
    def discover_site_hierarchy(self, site_hierarchy):
        if not site_hierarchy:
            return None
        siteresp = self.dnacSecurityManager.call_dnac(GroupingService.urlGetSiteHierarchyUrl(site_hierarchy.strip()))
        return SiteFactory.makeSite(siteresp.text) if siteresp.status_code == 200 else None

    #
    # Discover the Global site
    #
    def discover_global(self):
        return self.discover_site_hierarchy('Global')

    #
    # Create a site with the given parameters
    #
    def create_site(self, site):
        if site:
            # Create the async task...
            resp = self.dnacSecurityManager.post_to_dnac(self.urlCreateSite, site.dnacJson)
            if resp.status_code < 200 or resp.status_code > 202:
                return None

            task = Task.parseJson(resp.text)

            # Follow the async task to completion
            site.id = self.dnacTaskManager.follow_task(task)
            return site

        raise ValueError('Request to create Invalid site - ignored')

    #
    # Delete a site the given site
    #
    def delete_site(self, site):
        if site and site.url:
            resp = self.dnacSecurityManager.post_to_dnac(url=site.url, json_payload='', operation='delete')
            if resp.status_code < 200 or resp.status_code > 202:
                return None

            self.dnacTaskManager.follow_task(Task(resp.text))
            return True

        raise ValueError('Request to delete Invalid or non-existent site hierarchy ')

    #
    # Delete the specified site hierarchy
    #
    def delete_site_hierarchy(self, hierarchy):
        return self.delete_site(self.discover_site_hierarchy(hierarchy))


if __name__ == "__main__":
    m = SecurityManager.SecurityManager('192.168.117.50')
    m.adminCredentials = ('admin', 'Maglev123')
    ms = GroupingService(m)
    globalx = ms.discover_global()
    print('Global site ->')
    globalx.print()



    st = Site(0, 'AmalaPaul', ' ', False, globalx.id)

    idx = ms.create_site(st)
    st.print()

    hier = 'Global/AmalaPaul'
    nsite = ms.discover_site_hierarchy(hier)
    if nsite:
        nsite.print()
    else:
        print('no such hierarchy - ' + hier)

    hier = 'Global/AmalaPaul/B'
    nsite = ms.discover_site_hierarchy(hier)
    if nsite:
        nsite.print()
    else:
        print('no such hierarchy - ' + hier)

# try:
# if ms.delete_site(nsite):
# print(' SIte deleted: ' + nsite.name)
# else:
# print(' Failed to delete SIte : ' + nsite.name)
# except:
# print(' Exception - Failed to delete SIte : ' + nsite.name)
