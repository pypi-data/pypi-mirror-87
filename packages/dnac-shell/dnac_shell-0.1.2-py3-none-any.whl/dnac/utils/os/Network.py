# re module provides support 
# for regular expressions 
import re
import socket
import subprocess as sp

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class Network:
    def __init__(self):
        pass

    @staticmethod
    def is_valid_fqdn(fqdn):
        if not fqdn or not fqdn.strip():
            return False
        try:
            if socket.gethostbyname(fqdn) == fqdn:
                return True
            elif socket.gethostbyname(fqdn) != fqdn:
                return True
        except socket.gaierror:
            return False

    @staticmethod
    def is_dotted_ip(strx):
        if not strx:
            return False
        l = strx.strip().split('.')
        for octet in l:
            if not octet.strip().isnumeric():
                return False
        return True


    # Define a function for 
    # validate an IP addess 
    @staticmethod
    def is_valid_ip(ip):
        # Make a regular expression
        # for validating an Ip-address 
        regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
			        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
			        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
			        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''

        # pass the regular expression
        # and the string in search() method
        return True if ip and re.search(regex, ip) else False

    @staticmethod
    def is_ip_alive(ip):
        status, result = sp.getstatusoutput("ping -c1  " + str(ip))
        return status == 0
