import json
from collections import namedtuple

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class MaglevKernel:
    def __init__(self,maglev):
        self._maglev_ = maglev

    @property
    def maglev(self):
        return self._maglev_

    @property
    def versionUrl(self):
        return  '/api/system/v1/maglev/packages'

    #
    # Parse the JSon of a particular maglev package
    #
    @staticmethod
    def parsePackageJson(jsonx):
        maglevPackage = namedtuple('MaglevPackage', 'name version status')
        maglevPackage.name = jsonx['name']
        maglevPackage.version = jsonx['version']
        maglevPackage.status = jsonx['status']
        return maglevPackage

    # 
    # Discover all maglev packages off this DNAC Cluster
    # (MaglevPackage is a tuple (name, version string and status)
    # 
    def discover_packages(self):
        pkgs_resp = self.maglev.security_manager.call_dnac(self.versionUrl)
        if pkgs_resp.status_code != 200:
           return None
        pkgs_resp_json = json.loads(pkgs_resp.text)
        pkgsarray = pkgs_resp_json['response']
        pkgslist = [ MaglevKernel.parsePackageJson(pkg_json) for pkg_json in pkgsarray ]
        kvpair = [ (nextpkg.name, nextpkg) for nextpkg in pkgslist ]
        return dict(kvpair) # Yield mappings of maglev package name -> maglev package

    # 
    # Discover the version of the specified Maglev Package 
    # 
    def get_package_version(self, package_name):
        given_package = package_name.strip() if package_name else None
        if not given_package:
           return None
        packages = self.discover_packages()
        the_package = packages[given_package] if packages and given_package else None
        # 
        # If the package is present but is not deployed, treat it as non-existent
        return the_package.version if the_package and the_package.status and the_package.status.upper() == 'DEPLOYED' else None
