from dnac.maglev.task.Task import Task


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class DnacException(Exception):
    """Base class for other DNAC exceptions"""
    pass


if __name__ == "__main__":
    m = DnacException('Hello')
    print('Exception ->')
    print(m)
