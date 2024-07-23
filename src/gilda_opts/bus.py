"""bus module contains the electric bus where the electric elements are connected."""

from dataclasses import dataclass

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class Bus(BaseClassJson):
    """Bus class.

    Attributes:
      uid:  Bus unique id
      name: Bus name
    """

    uid: int = -1
    name: str = ""
