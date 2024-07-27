"""bus module contains the electric bus where the electric elements are connected."""

from dataclasses import dataclass

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class Bus(BaseClassJson):
    """Bus represent the electric bus where the electric elements are connected."""

    #: Bus unique id
    uid: int = -1

    #: Bus name
    name: str = ""
