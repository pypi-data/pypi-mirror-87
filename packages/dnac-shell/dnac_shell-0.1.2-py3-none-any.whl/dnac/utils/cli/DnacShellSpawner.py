import sys
import argparse
from dnac.utils.cli.CliSession import CliSession
from dnac.utils.os.FileSystem import FileSystem


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks


class DnacShellSpawner:
    def __init__(self):
        pass

    @staticmethod
    def parse_args():
        # Create the parser
        cmd_parser = argparse.ArgumentParser(description='DNAC Shell command line options parser ')
        cmd_parser.add_argument('--command-file',
                                type=str,
                                action="store",
                                required=False,
                                default=None,
                                help='The path of the file containing DNAC shell commands')

        # Execute the parse_args() method
        args = cmd_parser.parse_args()
        return args

    @staticmethod
    def spawn():
        clis = CliSession()
        arguments = DnacShellSpawner.parse_args()
        if arguments.command_file:
            if not FileSystem.is_file_readable(arguments.command_file):
                print('??? Command file <<' + arguments.command + '>> does not exist or is not readable')
                sys.exit(1)
            else:
                clis.batch(arguments.command_file)
                sys.exit(0)
        else:
            clis.start()


if __name__ == "__main__":
    DnacShellSpawner.spawn()
