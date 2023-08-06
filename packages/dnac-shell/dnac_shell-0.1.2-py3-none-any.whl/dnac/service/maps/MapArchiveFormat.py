from enum import Enum
import argparse


# copyright (c) 2020 cisco Systems Inc.
# @author rks@ciscocom

#
# Allows us to user enum type in CLI args
#
class ArgTypeMixin(Enum):

    @classmethod
    def argtype(cls, s: str) -> Enum:
        try:
            return cls[s]
        except KeyError:
            raise argparse.ArgumentTypeError(
                f"{s!r} is not a valid {cls.__name__}")

    def __str__(self):
        return self.name


class MapArchiveFormat(Enum):
    UNKNOWN = 0
    PRIME_ARCHIVE = 1
    EKAHAU = 2
    ARUBA = 3
