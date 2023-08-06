import getpass
import argparse
import os
import socket
import sys

import requests
from dnac.DnacCluster import DnacCluster
from dnac.utils.os.Network import Network
from dnac.utils.os.FileSystem import FileSystem
from dnac.service.maps.MapArchiveFormat import MapArchiveFormat


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class DnacMapExporter:
    def __init__(self):
        self._archive_format = MapArchiveFormat.PRIME_ARCHIVE
        self._archive_file_ = None
        self._dnac_cluster_ = None
        self._anchor_site_ = None

    @property
    def archive_format(self):
        return self._archive_format 

    @archive_format.setter
    def archive_format(self, thisformat):
        self._archive_format = thisformat

    @property
    def archive_file(self):
        return self._archive_file_

    @archive_file.setter
    def archive_file(self, thefile):
        self._archive_file_ = thefile

    @property
    def dnac_cluster(self):
        return self._dnac_cluster_

    @dnac_cluster.setter
    def dnac_cluster(self, thecluster):
        self._dnac_cluster_ = thecluster

    @property
    def anchor_site(self):
        return self._anchor_site_

    @anchor_site.setter
    def anchor_site(self, thesite):
        self._anchor_site_ = thesite

    @staticmethod
    def preamble():
        requests.packages.urllib3.disable_warnings()
        print(' ')
        print('*** DNAC Map Archive Exporter, (c) 2020 cisco Systems Inc. ***')
        print('***                  ver. 2.1, May 2020                    ***')
        print(' ')

    @staticmethod
    def get_credentials(args):
        username = args.dnac_admin if args.dnac_admin else input('DNAC Web Admin: ')
        passwordx = getpass.getpass()
        return username, passwordx

    @staticmethod
    def get_dnac(args):
        dnac = args.dnac_address if args.dnac_address else input('DNAC IP/FQDN: ')
        if Network.is_dotted_ip(dnac):
            if not Network.is_valid_ip(dnac):
                print('??? Bad IP or FQDN - aborted')
                sys.exit(1)

        dnac = socket.getfqdn(dnac)
        admin_credentials = DnacMapExporter.get_credentials(args)
        given_dnac_cluster = DnacCluster(dnac, admin_credentials)
        try:
            given_dnac_cluster.login_as(admin_credentials)
        except:
            print('??? Failed to access DNAC Cluster <', dnac, '>: Pl check if the server is reachable')
        given_dnac_cluster.version = given_dnac_cluster.mapService.discover_service_version()
        return given_dnac_cluster

    @staticmethod
    def get_site_hierarchy(args, the_dnac_cluster):
        site_hierarchy = None
        site_id = None
        while not site_hierarchy and not site_id:
            sh = args.site if args.site else input('Site Name to archive from: ')
            sh = sh.strip()
            if not sh.startswith('Global'):
                sh = 'Global' + sh if sh.startswith('/') else 'Global/' + sh
            site_hierarchy = the_dnac_cluster.groupingService.discover_site_hierarchy(sh)
            if not site_hierarchy:
                print('??? Unable to locate site <', sh, '> on DNAC ', the_dnac_cluster.address, ' : Please retry')

        return site_hierarchy

    @staticmethod
    def get_target_file():
        given_file = input('File to save the archive into: ')
        return given_file.strip()

    def print_export_summary(self):
        print(' ')
        print('*********************** Export Summary ***********************')
        print(' >DNAC Cluster: ', self.dnac_cluster.address, ', version: ', self.dnac_cluster.version)
        print(' >Site Hierarchy: ', self.anchor_site.hierarchy, ', Id = ', self.anchor_site.id)
        print(' >Target Archive File: ', self.archive_file)
        print(' >Archive Format: ', self.archive_format)
        print('**************************************************************')
        print(' ')
        print('Exporting... ')

    @staticmethod
    def parse_args():
        # Create the parser
        my_parser = argparse.ArgumentParser(description='DNAC Map Archive Exporter, (c) 2020, cisco Systems Inc ',
                                            epilog='Enjoy the tool! :)')

        my_parser.version = '2.1'
        site_arg_group = my_parser.add_mutually_exclusive_group(required=False)
        site_arg_group.add_argument('--site',
                               type=str,
                               action="store",
                               default='',
                               required=False,
                               help='The name of base of the site of the hierarchy to be exported ')

        site_arg_group.add_argument('--site-id',
                               type=str,
                               action="store",
                               default='',
                               required=False,
                               help='The ID of the base of the site of the hierarchy to be exported ')

        my_parser.add_argument('--dnac-address',
                               type=str,
                               action="store",
                               required=False,
                               help='The IP/FQDN of DNAC on which this is to be deployed')

        my_parser.add_argument('--dnac-admin',
                               type=str,
                               action="store",
                               default='',
                               required=False,
                               help='Username of the DNAC administrative user')

        my_parser.add_argument('--archive-file',
                               type=str,
                               action="store",
                               default='',
                               required=False,
                               help='Full path of the archive file into which the archive must be stored ')

        my_parser.add_argument('--format',
                               type=str,
                               action="store",
                               default='prime',
                               required=False,
                               help='Format of the exported archive: Prime Archive or Ekahau Pro project')

        # Execute the parse_args() method
        args = my_parser.parse_args()
        return args

    @staticmethod
    def do_export(dnac_cluster, anchor_site_id, archive_file, export_format=MapArchiveFormat.EKAHAU):
        if not FileSystem.is_file_writable(archive_file):
            print('???Export Aborted: Specified archive file is not writeable')
            return None

        temp_archive_file = os.path.basename(archive_file)
        FileSystem.force_delete_file(temp_archive_file)

        #self.print_export_summary()

        print('Exporting site <' + anchor_site_id + '> into ' + archive_file, end ='...', flush=True)
        result = dnac_cluster.mapService.export_site(anchor_site_id, temp_archive_file, export_format)
        if not result:
            print('...Failed')
            print('???Failed to export: Aborted')
            return None
        status, content_type, content = result
        if 'application/json' in content_type:  # DNAC 2.1.1.x style response
            file_url = content
            res_components = file_url.split('/') if file_url else None
            fileid = res_components[-1] if res_components else None
            if fileid:
                dnac_cluster.fileService.download_file(fileid, temp_archive_file)
            else:
                print('...Failed')
                print('???Failed to export: Aync task to export failed with error')
                return None
        elif 'application/octet-stream' in content_type:  # Pre DNAC 2.1.1.x style...
            f = open(temp_archive_file, 'w+b')
            f.write(content)
            f.close()
        else:
            print('...Failed')
            print('???Failed to export: Unrecognized response from DNAC Cluster: ', content_type)
            return None
        FileSystem.move(temp_archive_file, archive_file)
        print('...Done')
        return archive_file

    def start_export(self):
        args = DnacMapExporter.parse_args()
        #System.clear()
        DnacMapExporter.preamble()
        self.dnac_cluster = DnacMapExporter.get_dnac(args)
        self.anchor_site = DnacMapExporter.get_site_hierarchy(args, self.dnac_cluster)
        if not self.anchor_site:
            print('???Export Aborted: No such site or building or floor')
            sys.exit(1)

        self.archive_file = args.archive_file if args.archive_file else DnacMapExporter.get_target_file()
        if not FileSystem.is_file_writable(self.archive_file):
            print('???Export Aborted: Specified archive file is not writeable')
            sys.exit(1)

        temp_archive_file = os.path.basename(self.archive_file)
        FileSystem.force_delete_file(temp_archive_file)

        self.archive_format = MapArchiveFormat.EKAHAU if args.format and args.format == 'ekahau' else MapArchiveFormat.PRIME_ARCHIVE

        self.print_export_summary()

        globalx = self.dnac_cluster.groupingService.discover_global()
        result = self.dnac_cluster.mapService.export_site(self.anchor_site.id, temp_archive_file,  self.archive_format )
        if not result:
            print('???Failed to export: Aborted')
            sys.exit(1)
        status, content_type, content = result
        if 'application/json' in content_type:  # DNAC 2.1.1.x style response
            file_url = content
            res_components = file_url.split('/') if file_url else None
            fileid = res_components[-1] if res_components else None
            if fileid:
                self.dnac_cluster.fileService.download_file(fileid, temp_archive_file)
            else:
                print('???Failed to export: Aync task to export failed with error')
                sys.exit(1)
        elif 'application/octet-stream' in content_type:  # Pre DNAC 2.1.1.x style...
            f = open(temp_archive_file, 'w+b')
            f.write(content)
            f.close()
        else:
            print('???Failed to export: Unrecognized response from DNAC Cluster: ', content_type)
            sys.exit(1)
        print(' ')
        FileSystem.move(temp_archive_file, self.archive_file)
        print('*** Export completed: archive file: ', self.archive_file)
