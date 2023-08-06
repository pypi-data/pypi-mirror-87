from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional
from typing_extensions import Protocol
from signal import signal, SIGINT
import re
import shlex
import argparse
import time
import requests
import socket
import sys
import datetime
from collections import deque
from datetime import datetime

from dnac.converter.Converter import Converter
from dnac.emitter.deployment.MapHierarchyDeployer import MapHierarchyDeployer
from dnac.exception.BadProjectFileException import InvalidProjectFileException
from dnac.service.maps.ImportOperation import ImportOperation
from dnac.service.maps.MapArchiveFormat import MapArchiveFormat
from dnac.utils.StackUtils import StackUtils
from dnac.utils.cli.SessionState import SessionState
from dnac.service.site.SiteType import SiteType
from dnac.DnacCluster import DnacCluster
from dnac.service.maps.Floor import Floor
from dnac.service.site.Building import Building
from dnac.service.maps.export.DnacMapExporter import DnacMapExporter
from dnac.utils.csv.MapsCsv import MapsCsv
from dnac.utils.os.FileSystem import FileSystem
from dnac.utils.os.Network import Network
from dnac.service.maps.importx.ImportConfiguration import ImportConfiguration


# copyright (c) 2020 cisco Systems Inc., All rights reserved
# @author rks@cisco.com

class CliSession:
    def __init__(self, dnac_cluster=None):
        self.__cwd__ = None, None
        self.__state__ = SessionState.UNINITIALIZED
        self.__num_children_sites__ = 0
        self.__versionx__ = '<Unknown>'
        self.__prompt__ = 'DNAC Maps> '
        self.__dnac_cluster__ = dnac_cluster
        self.__batch_file__ = None
        self.__build__ = '0.0.60'
        signal(SIGINT, CliSession.handler)

    @property
    def build(self):
        return self.__build__

    @property
    def dnac_cluster(self):
        return self.__dnac_cluster__

    @dnac_cluster.setter
    def dnac_cluster(self, given_cluster):
        self.__dnac_cluster__ = given_cluster

    @property
    def prompt(self):
        return self.__prompt__

    @property
    def state(self):
        return self.__state__

    @state.setter
    def state(self, new_state):
        self.__state__ = new_state

    @property
    def cwd(self):
        return self.__cwd__

    @cwd.setter
    def cwd(self, newcwd):
        self.__cwd__ = newcwd

    @property
    def num_children_sites(self):
        return self.__num_children_sites__

    @property
    def version(self):
        return self.__versionx__

    @property
    def batch_file(self):
        return self.__batch_file__

    @batch_file.setter
    def batch_file(self, command_file):
        self.__batch_file__ = command_file

    def batch(self, command_file):
        self.batch_file = open(command_file, 'r') if FileSystem.is_file_readable(command_file) else None
        self.start()

    def start(self):
        if self.dnac_cluster:
            self.cwd = 'Global', self.dnac_cluster.global_site.id, SiteType.SITE
            self.state = SessionState.RUNNING
        else:
            self.state = SessionState.UNINITIALIZED
        self.shell()
        self.cwd = 'Global', self.dnac_cluster.global_site, SiteType.SITE
        self.state = SessionState.STOPPED

    @staticmethod
    def site_type(typeenum):
        if typeenum == SiteType.FLOOR:
            return 'Floor'
        if typeenum == SiteType.BUILDING:
            return 'Building'
        return 'Site'

    def preamble(self):
        requests.packages.urllib3.disable_warnings()
        print(' ')
        print('*** DNAC Map Shell, (c) 2020 cisco Systems Inc.  ***')
        print('             ver. 2.2' + ' (' + self.build + '), Sep 2020')
        print(' ')

    def cd(self, site=None):
        sitex = self.dnac_cluster.groupingService.discover_site_hierarchy(site)
        if isinstance(sitex, list):
            sitex = sitex[0] if len(sitex) > 0 else None
        if not sitex:
            print('??? Unrecognized site: "', site, '"')
        else:
            typex = SiteType.UNKNOWN
            if isinstance(sitex, Floor):
                typex = SiteType.FLOOR
            elif isinstance(sitex, Building):
                typex = SiteType.BUILDING
            else:
                typex = SiteType.SITE

            self.cwd = site, sitex.id, typex

        self.do_prompt()

    @staticmethod
    #
    # Normalize a possibly a path comprising . and ..
    #
    def normalize_path(given_path: str) -> str:
        normal_path = None
        if not given_path:
            return normal_path
        path_components = given_path.strip().split('/')
        stack = deque()
        for next_comp in path_components:
            if next_comp == '..':
                if not StackUtils.isempty(stack):
                    stack.pop()
                else:
                    return None
            elif next_comp == '.':
                continue
            else:
                stack.append(next_comp)

        if not StackUtils.isempty(stack):
            normal_path = "/".join(stack)
            normal_path = normal_path[1:] if normal_path.startswith('/') else normal_path

        return normal_path

    #
    # Evaluate the specified path that may contain
    # metacharacters into a normalized path
    #
    def get_full_path(self, rel_path):
        rel_path = rel_path.strip() if rel_path else None
        if not rel_path:
            rel_path = '~'
        if rel_path == '.':
            return self.cwd[0]
        # rel_path = os.path.normpath(rel_path)
        if rel_path == '..':
            brk = self.cwd[0].split('/')
            if brk and len(brk) > 0:
                brk.pop()
                rel_path = '/'.join(brk)
        elif rel_path.startswith('/'):
            if rel_path == '/Global':
                rel_path = 'Global'
            elif rel_path.startswith('/Global/'):
                rel_path = rel_path[1:]
            elif not rel_path.startswith('Global/'):
                rel_path = 'Global' + rel_path
        elif rel_path == '~':
            rel_path = 'Global'
        else:
            # rel_path = os.path.join(self.cwd[0], rel_path)
            rel_path = '/'.join([self.cwd[0], rel_path])
            # rel_path = os.path.normpath(rel_path)

        normalized_path = rel_path = CliSession.normalize_path(rel_path)
        rel_path = normalized_path if normalized_path else rel_path
        return rel_path.strip() if rel_path and rel_path.startswith('Global') else None

    #
    # Print usage help information fopr the specified command
    #
    def usage(self, command, *args):
        if command:
            if command == 'login':
                print('Usage: ', 'login [to <dnac-ip> [as <dnac-admin-user> [using password <dnac-admin-password>]]]')
                return

            if command == 'cd':
                print(args[0])
                print('Usage: ', 'cd [<site hierarchy>]')
                return

            if command == 'delete':
                print(args[0])
                print('Usage: ', 'delete [<site hierarchy>]')
                return

            if command == 'export':
                print('Usage: ', 'export [--map-archive|--bulk-apa] --file <file>]')
                return

            if command == 'import':
                print('Usage: ', 'import [--map [--format prime|aruba|ekahau  --relocate <mapper> ] |--bulk-apa] '
                                 '--file <file>]')
                return

            if command == 'update':
                print('Usage: ', 'update sites --csvfile <file>]')
                return

            if command == 'pwd' or command == 'info' or command == 'date':
                print('Usage: ', command)
                return
        print('??' + command + '??')
        return

    def execute_server(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        versx = str(self.dnac_cluster.version) if self.dnac_cluster.version else '<Unknown>'
        print('[DNAC Server: ' + self.dnac_cluster.address + ', vers. ' + versx + ']')

    def execute_update_floors(self, csvfile):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        updated = self.dnac_cluster.mapService.update_floor_indices(csvfile)
        if updated == -1:
            # Malformed CSV
            print('?? Malformed CSV file - typo in column headers?')
        elif updated < -1:
            print('?? Malformed CSV file - is "' + csvfile + '" a CSV file at all?')
        else:
            print('[' + (str(updated) if updated > 0 else 'No') + ' floors updated]')

    def execute_info(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        self.execute_server()
        self.execute_pwd()
        print('Number of children sites: ', self.num_children_sites)

    def execute_pwd(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return

        if self.cwd[2] == SiteType.FLOOR:
            floor = self.dnac_cluster.mapService.discover_floor(self.cwd[0])
            floor = floor[0] if isinstance(floor, list) else floor
            print(CliSession.site_type(self.cwd[2]))
            print('\tHierarchy:\t\t' + self.cwd[0])
            print('\tIndex:\t\t\t' + floor.floor_index)
            print('\tGroup Id:\t\t' + self.cwd[1])
        else:
            print(CliSession.site_type(self.cwd[2]) + ': ' + self.cwd[0] + '\t, Id: ' + self.cwd[1])

    def execute_version(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        print('DNAC Version: ', self.dnac_cluster.version)

    def execute_date(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%b %d %Y, %H:%M:%S")
        print(dt_string, time.localtime().tm_zone)

    def execute_time(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        print(datetime.now().strftime("%H:%M:%S"))

    def execute_export_map(self, root, file) -> None:
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        saved_file = DnacMapExporter.do_export(self.dnac_cluster, root, file)
        print(' ')
        if saved_file:
            print('*** Export completed: archive file: ', saved_file)
        return

    def execute_import_map(self, root, config: ImportConfiguration) -> None:
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return

        # We support only Aruba import as of now
        if config.format != MapArchiveFormat.ARUBA:
            return

        # Step 1: Parse Aruba project...
        #
        aruba_project_converter = Converter()
        try:
            sites = aruba_project_converter.process_aruba_project(config.file)
        except InvalidProjectFileException as e:
            return

        # Step 2: Deploy parsed project onto DNAC
        #
        try:
            deployer = MapHierarchyDeployer()
            invalid_mapper, error_code, mapper = False, 0, dict()
            if config.relocator:
                mapper_result = MapsCsv(config.relocator).load_site_mapper()
                invalid_mapper, error_code, mapper = mapper_result
                if invalid_mapper:
                    print("?? Import Failed: Invalid relocation mapper")
                    return

            deployer.deploy(sites, mapper, self.dnac_cluster)
        except Exception as e:
            import traceback
            print("?? Deploy failed...", e)
            traceback.print_exc()
            return

        print('*** Import completed: archive file: ', config.file)
        return

    def list_floor_aps(self):
        elements = self.dnac_cluster.mapService.discover_floor_aps(self.cwd[1])
        element_count = len(elements) if elements else 0
        print('=> ' + str(element_count) + ' Access Points ')

    def list_floor_paps(self):
        elements = self.dnac_cluster.mapService.discover_floor_paps(self.cwd[1])
        element_count = len(elements) if elements else 0
        print('=> ' + str(element_count) + ' Planned Access Points ')

    def execute_ls(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        print(' ')
        print('[' + CliSession.site_type(self.cwd[2]) + ': ' + self.cwd[0] + ']')
        if self.cwd[2] == SiteType.FLOOR:
            print('*** Items on the floor area: ')
            self.list_floor_aps()
            self.list_floor_paps()
            print(' ')
        else:
            children = self.dnac_cluster.groupingService.discover_site_children(self.cwd[1])
            for child in children:
                print(child.name, "\t", child.id)
        self.do_prompt()

    @staticmethod
    def extract_login_parameters(given_parms):
        pattern1 = re.compile('to\s+([a-zA-Z0-9_.\-]+)\Z')
        pattern1 = re.compile('to\s+([a-zA-Z0-9_.\-]+)\Z')
        pattern2 = re.compile('to\s+([a-zA-Z0-9_.\-]+)\s+as\s+(\w+)\Z')
        pattern3 = re.compile('to\s+([a-zA-Z0-9_.\-]+)\s+as\s+(\w+)\s+using\s+password\s+(\S+)\Z')
        # pattern1 = re.compile('to\s+(\w+)\Z')
        # pattern1 = re.compile('to\s+(\w+)\Z')
        # pattern2 = re.compile('to\s+(\w+)\s+as\s+(\w+)\Z')
        # pattern3 = re.compile('to\s+(\w+)\s+as\s+(\w+)\s+using\s+password\s+(\S+)\Z')
        ipx = adminx = pwdx = None
        parms = given_parms.strip() if given_parms else None
        if parms:
            match = re.search(pattern3, parms)
            if match:
                ipx = match.group(1)
                adminx = match.group(2)
                pwdx = match.group(3)
            else:
                match = re.search(pattern2, parms)
                if match:
                    ipx = match.group(1)
                    adminx = match.group(2)
                else:
                    match = re.search(pattern1, parms)
                    if match:
                        ipx = match.group(1)
                    else:
                        return None
        return ipx, adminx, pwdx

    def execute_login(self, args):
        parameters = CliSession.extract_login_parameters(' '.join(args))
        dnac_ip = None
        if parameters:
            (dnac_ip, dnac_admin, dnac_password) = parameters
        else:
            self.usage('login')
            return

        dnac_ip = dnac_ip if dnac_ip else input('DNAC Address: ')
        if re.search('[a-zA-Z]', dnac_ip):
            if not Network.is_valid_fqdn(dnac_ip):
                print('?? Invalid FQDN "' + dnac_ip + '": did you mistype the DNAC FQDN?')
                self.usage('login')
                return
        elif not Network.is_valid_ip(dnac_ip):
            print('?? Invalid IP "' + dnac_ip + '": did you mistype the DNAC IP?')
            self.usage('login')
            return

        #
        # if not Network.is_ip_alive(dnac_ip):
        # print('?? DNAC "' + dnac_ip + '" unreachable: did you mistype the IP?')
        # self.usage('login')
        # return

        if dnac_admin:
            dnac_password = dnac_password if dnac_password else DnacCluster.get_password()
            dnac_credentials = (dnac_admin, dnac_password)
        else:
            dnac_credentials = DnacCluster.get_credentials()
        self.dnac_cluster = DnacCluster(socket.getfqdn(dnac_ip), dnac_credentials)
        try:
            self.dnac_cluster.login_as(dnac_credentials)
        except requests.exceptions.ConnectionError:
            print('??? Unable to reach ' + dnac_ip + ' - did you mistype IP/FQDN?')
            self.usage('login')
            self.dnac_cluster = None
            return
        if not self.dnac_cluster.global_site:
            print('??? Unable to connect to ' + dnac_ip + ' - did you mistype IP/FQDN?')
            return

        if self.dnac_cluster.valid_session():
            print('[Connected: ', self.dnac_cluster.address + ']')
            self.start()
        else:
            print('??? Invalid credentials - retry')

    def execute_cd(self, args):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        if not args:
            self.cd()
            return
        site = self.get_full_path(args)
        if not site:
            self.usage('cd', 'Invalid Path: "' + args + '"')
            return
        self.cd(site)
        return

    def execute_delete(self, args):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        if not args:
            self.usage('delete', 'Invalid Path: "' + args + '"')
            return
        site = self.dnac_cluster.groupingService.discover_site_hierarchy(args)
        print('disc site = ', site )
        if not site:
            self.usage('delete', 'Invalid Path: "' + args + '"')
            return
        try:
            if not self.dnac_cluster.groupingService.delete_site(site[0]):
                print('? Failed to delete - some other error')
        except ValueError as exc:
            print('?? Failed to delete - an internal error has occurred ')

        return

    def do_prompt(self):
        print(self.prompt)

    #
    # Obtain the next command either rom batch file (if in batch mode)
    # or interactively from user
    #
    def get_next_command(self):
        if self.batch_file:
            next_command = self.batch_file.readline()
            if next_command == '':
                next_command = 'exit'
            temp_copy_of_command = next_command.split()
            if 'login' in next_command and 'using' in next_command and 'password' in next_command:
                temp_copy_of_command = temp_copy_of_command[:7] if len(
                    temp_copy_of_command) > 7 else temp_copy_of_command
                temp_copy_of_command.append('<masked>')
            print(self.prompt + ' '.join(temp_copy_of_command))
        else:
            next_command = input(self.prompt)
        return next_command

    def shell(self):
        self.preamble()
        while self.state != SessionState.STOPPED:
            self.execute(self.get_next_command())

    #
    # Retrieve from the list of tuple (opts),
    # the opt value that matchjes the given opt.
    #
    @staticmethod
    def retrieve_opt(optlist, given_opt):
        if optlist and given_opt:
            for i in optlist:
                if type(i) is tuple:
                    if i[0] == given_opt:
                        return given_opt, i[1]
        return None

    def execute(self, command):
        op_and_args = command.strip() if command else None
        if not op_and_args or op_and_args.startswith('#'):
            #
            # Comments are NOOP
            return
        op_and_args = op_and_args.split() if op_and_args else None
        if not op_and_args:
            return
        op, *args = op_and_args
        sargs = ' '.join(args) if args else None

        if op == 'login':
            self.execute_login(args)
            return
        if self.state == SessionState.STOPPED:
            return
        if op == 'dnac':
            self.execute_server()
            return
        if op == 'cd':
            self.execute_cd(sargs)
            return
        if op == 'delete':
            self.execute_delete(sargs)
            return
        if op == 'info':
            self.execute_info()
            return
        if op_and_args[0] == 'pwd':
            self.execute_pwd()
            return
        if op_and_args[0] == 'date':
            self.execute_date()
            return
        if op_and_args[0] == 'update':
            update_config = self.parse_csv_update_opts(sargs)
            mode, csvfile = update_config if update_config else (None, None)
            if not mode or not csvfile:
                self.usage('update')
                return
            if mode == 'aps':
                print("?? '--aps' not yet implemented")
                return
            if not FileSystem.is_file_readable(csvfile):
                print('?? CSV File <' + csvfile + '> not found')
                self.usage('update')
                return

            self.execute_update_floors(csvfile)
            return
        if op_and_args[0] == 'import':
            import_config = self.parse_import_opts(sargs)
            if not import_config:
                self.usage('import')
                return
            if import_config.operation != ImportOperation.IMPORT_MAPS:
                print(import_config.operation)
                print('import: <bulk-ap> is not yet implemented')
                self.usage('import')
                return

            if import_config.format == MapArchiveFormat.UNKNOWN:
                print(import_config.format)
                print('import: Map archive format must be specified>')
                self.usage('import')
                return

            if not import_config.file:
                print('?? Must specify import file')
                self.usage('import')
                return

            self.execute_import_map(self.cwd[1], import_config)
            return
        if op_and_args[0] == 'export':
            export_config = self.parse_export_opts(sargs)
            if not export_config:
                self.usage('export')
                return
            mode, file = export_config
            if mode != 'map-archive':
                print('export: <bulk-ap> is not yet implemented')
                self.usage('export')
                return

            if not file:
                print('?? Must specify export file')
                self.usage('export')
                return

            self.execute_export_map(self.cwd[1], file)
            return
        if op_and_args[0] == 'ls':
            self.execute_ls()
            return
        if op_and_args[0] == 'exit' or op_and_args[0] == 'quit':
            sys.exit(0)
        self.usage(op)

    @staticmethod
    def handler(signal_received, frame):
        # User typed CTRL/C - clean up and quit gracefully
        print('  ')
        print('[^C detected: type "exit"/"quit" to exit]')
        return

    def export_usage(self):
        self.usage('export')

    def import_usage(self):
        self.usage('importx')

    def update_usage(self):
        self.usage('update')

    def parse_csv_update_opts(self, args):
        parser = argparse.ArgumentParser(usage=self.update_usage)
        type_group = parser.add_mutually_exclusive_group(required=True)
        type_group.add_argument('--floors',
                                default=False,
                                required=False,
                                dest='floors', action='store_true',
                                help='Update floors ')

        type_group.add_argument('--aps',
                                default=False,
                                required=False,
                                dest='aps', action='store_true',
                                help='Update Access Points/Sensors ')

        parser.add_argument('-csv', '--csvfile',
                            default=False,
                            type=str,
                            required=False,
                            dest='csvfile', action='store',
                            help='CSV File with floor attributes')
        try:
            pargs = parser.parse_args(shlex.split(args))
            return ('floors', pargs.csvfile) if pargs.floors else ('aps', pargs.csvfile)
        except:
            pass
        return None

    def parse_export_opts(self, args):
        parser = argparse.ArgumentParser(usage=self.export_usage)
        mode_group = parser.add_mutually_exclusive_group(required=False)
        mode_group.add_argument('--map-archive',
                                default=False,
                                required=False,
                                dest='map_archive', action='store_true',
                                help='Export map archive')

        mode_group.add_argument('--bulk-ap',
                                default=False,
                                required=False,
                                dest='bulk_ap', action='store_true',
                                help='Export Access Points in bulk')

        parser.add_argument('--file',
                            type=str,
                            action="store",
                            required=False,
                            help='Target file to use for export')

        try:
            pargs = parser.parse_args(shlex.split(args))
            if pargs.map_archive:
                return 'map-archive', pargs.file
            if pargs.bulk_ap:
                return 'bulk-ap', pargs.file
        except:
            pass
        return None

    #
    # Parse importx command and return Import configuration
    #
    def parse_import_opts(self, args) -> ImportConfiguration:
        # importConfig = ImportConfiguration('John Doe', 34)('John Doe', 34)
        parser = argparse.ArgumentParser(usage=self.import_usage)
        # mode_group = parser.add_mutually_exclusive_group(required=False)
        parser.add_argument('--map',
                            default=False,
                            required=False,
                            dest='map_archive', action='store_true',
                            help='Import map archive')

        #
        # Format of the archive to be imported: Prime (default), Ekahau, or Aruba
        #
        parser.add_argument('--format',
                            type=str,
                            default="prime",
                            required=False,
                            dest='import_format', action='store',
                            help='Import map archive format')

        # mode_group.add_argument('--format',
        #                         type=MapArchiveFormat.argtype,
        #                         choices=MapArchiveFormat,
        #                         default=MapArchiveFormat.PRIME_ARCHIVE,
        #                         required=False,
        #                         dest='import_format', action='store',
        #                         help='Import map archive format')

        # mode_group.add_argument('--parent-site',
        #                        type=str,
        #                        action="store",
        #                        default='',
        #                        help='The name of the site under which to plant the buildings')

        # mode_group.add_argument('--bulk-ap',
        #                         default=False,
        #                         required=False,
        #                         dest='bulk_ap', action='store_true',
        #                         help='Import Access Points in bulk')

        parser.add_argument('--file',
                            type=str,
                            action="store",
                            required=False,
                            help='Target file to use for import')

        parser.add_argument('--relocate',
                            type=str,
                            action="store",
                            required=False,
                            help='Relocation mapper file ')

        # Initialize the import configuration attributes
        #
        try:
            pargs = parser.parse_args(shlex.split(args))
            if pargs.map_archive:
                if pargs.import_format == "prime":
                    pargs.import_format = MapArchiveFormat.PRIME_ARCHIVE
                elif pargs.import_format == "aruba":
                    pargs.import_format = MapArchiveFormat.ARUBA
                elif pargs.import_format == "ekahau":
                    pargs.import_format = MapArchiveFormat.EKAHAU
                else:
                    pargs.import_format == MapArchiveFormat.UNKNOWN

                return ImportConfiguration(ImportOperation.IMPORT_MAPS, pargs.import_format, pargs.file,
                                           pargs.relocate)
            if pargs.bulk_ap:
                return ImportConfiguration(ImportOperation.IMPORT_APS, MapArchiveFormat.UNKNOWN, pargs.file)
        except SystemExit as e:
            print('except in parse opts import', e)
        return None
