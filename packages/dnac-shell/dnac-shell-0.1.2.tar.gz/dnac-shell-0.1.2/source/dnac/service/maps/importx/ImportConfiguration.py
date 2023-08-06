
# copyright (c) 2020 cisco Systems Inc.
# @author rks@cisco.com

from dataclasses import dataclass
from dnac.service.maps.MapArchiveFormat import MapArchiveFormat
from dnac.service.maps.ImportOperation import ImportOperation


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class ImportConfiguration:
    operation: ImportOperation
    format: MapArchiveFormat
    file: str
    relocator: str
