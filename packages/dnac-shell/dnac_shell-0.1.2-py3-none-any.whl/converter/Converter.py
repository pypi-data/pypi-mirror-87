import argparse
import os
import sys
import getpass

from dnac.converter.aruba.parser.ArubaProjectParser import ArubaProjectParser
from dnac.exception.BadProjectFileException import InvalidProjectFileException
from dnac.utils.package.Packager import Packager


class Converter:

    def __init__(self):
        self.credentials = None
        self.parse_args()

    # initialize
    @staticmethod
    def parse_args():
        # Create the parser
        my_parser = argparse.ArgumentParser(description='Convert Aruba project to DNAC map archive')
        my_parser.add_argument('--project',
                               type=str,
                               action="store",
                               required=True,
                               help='The path of the Aruba project file to be converted')

        my_parser.add_argument('--deploy-on',
                               type=str,
                               action="store",
                               default='',
                               help='The IP/FQDN of DNAC on which this is to be deployed')

        # Execute the parse_args() method
        args = my_parser.parse_args()
        return args

    @staticmethod
    def process(args):
        projfile = args.project
        if not os.path.exists(projfile):
            print('The specified Aruba Project does not exist')
            sys.exit(1)

        if os.path.isdir(projfile):
            print('The specified path denotes a folder - cannot process')
            sys.exit(1)

        # self.credentials = Converter.get_credentials()

        try:
            project_root = Packager.unpack(projfile)
        except InvalidProjectFileException:
            print('The specified Aruba project file is invalid - aborting')
            sys.exit(1)

        if not ArubaProjectParser.is_valid(project_root):
            print('The specified Aruba project file has invalid format or is malformed')
            sys.exit(1)

        try:
            sites = ArubaProjectParser.parse(project_root)
        except InvalidProjectFileException:
            print('The specified Aruba project file is invalid - aborting')
            sys.exit(1)

        Converter.print_summary(sites)
        print('The specified Aruba project file was successfully parsed. Sites = ', sites)
        return sites

    @staticmethod
    def get_credentials():
        dnac_user = getpass.getuser()
        try:
            dnac_pw = getpass.getpass()
        except Exception as error:
            print('Failed to obtain password', error)
            raise
        else:
            print('Password entered:', dnac_pw)
        return dnac_user, dnac_pw

    @staticmethod
    def print_summary(sites):
        if not sites or len(sites) == 0:
            print('No campuses processed - empty project')
            return
        print(len(sites), ' Sites processed:')
        for next_site_id in sites:
            next_site = sites[next_site_id]
            print('Site id ', next_site_id, ', Site name = ', next_site.name)
            print('Buildings count = ', next_site.building_count)
            for building in next_site.get_all_buildings():
                Converter.print_building(building)
            print('=========')

    @staticmethod
    def print_building(building):
        print('Building ', building.name, ', floor count = ', building.floor_count)
        for floor in building.get_all_floors():
            Converter.print_floor(floor)

    @staticmethod
    def print_floor(floor):
        print('Floor ', floor.name, ', AP count = ', floor.pap_count)
        for ap in floor.get_all_paps():
            Converter.print_ap(ap)

    @staticmethod
    def print_ap(ap):
        print('AP ', ap.name, ', AP model = ', ap.model, ', Position = ', ap.position)

    @staticmethod
    def main():
        converter = Converter()
        args = Converter.parse_args()
        sites = converter.process(args)


if __name__ == "__main__":
    Converter.main()
