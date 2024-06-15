"""Schedule class represents the scheduling object."""

from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin

from gilda_opts.system import System


@dataclass
class Schedule(DataClassJsonMixin):
    """
    Schedule class.

    Attributes:
    -----------
    system: system definition.
    """

    system: System = None
