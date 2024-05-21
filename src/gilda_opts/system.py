from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin

from typing import List

from gilda_opts.bus import Bus
from gilda_opts.demand import Demand


@dataclass
class SystemOptions():
    '''System options class'''
    cfail: float = 1000
    integer_mode: int = 0


@dataclass
class System(DataClassJsonMixin):
    '''System class'''
    name: str = ''
    uid: int = -1
    options: SystemOptions = field(default_factory=SystemOptions)
    buses: List[Bus] = field(default_factory=lambda: [])
    demands: List[Demand] = field(default_factory=lambda: [])
