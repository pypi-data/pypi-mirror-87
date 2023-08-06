# setup.py - unnecessary if not redistributing the code, see below
from setuptools import setup, find_packages

ldict = locals()
ldict['NAME'] = 'dnac-shell'
ldict['VERSION'] = '0.1.2'
ldict['DESCRIPTION'] = 'DNAC Command Line Shell that can be used to perform salient operations on DNAC'
ldict['AUTHOR'] = 'Rk Somasundaram'
ldict['LICENSE']='cisco Systems Inc.'
ldict['DOWNLOAD_URL']='http://www.cisco.com'
ldict['INSTALL_REQUIRES']=[
          'PyYAML',
          'requests']
ldict['AUTHOR_EMAIL']='rks@cisco.com'

setup(
      name=ldict['NAME'],
      author=ldict['AUTHOR'],
      author_email=ldict['AUTHOR_EMAIL'],
      maintainer=ldict['AUTHOR'],
      version=ldict['VERSION'],
      download_url=ldict['DOWNLOAD_URL'],
      description=ldict['DESCRIPTION'],
      # py_modules=['dnac'],
      package_dir={'': 'source'}, 
      #entry_points={
              #'console_scripts': [
                  #'DnacShell = dnac.utils.cli.DnacShell:main',
              #],
      #},
      install_requires=ldict['INSTALL_REQUIRES'],
      packages=find_packages(where='source'),
      license=ldict['LICENSE'])
