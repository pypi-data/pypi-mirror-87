from enum import Enum

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class SessionState(Enum):
    UNKNOWN = 0
    UNINITIALIZED = 1
    RUNNING = 2
    STOPPED = 3
