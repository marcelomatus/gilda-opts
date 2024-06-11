"""Schedule class represents the scheduling object."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin

from gilda_opts.block import Block
from gilda_opts.system import System


@dataclass
class Schedule(DataClassJsonMixin):
    """
    Schedule class.

    Attributes:
    -----------
    blocks: List of blocks.
    system:
    """

    blocks: List[Block] = field(default_factory=list)
    system: System = None
