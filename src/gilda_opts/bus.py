"""bus module contains the electric bus where the electric elements are connected."""

from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Bus(DataClassJsonMixin):
    """Bus class."""

    uid: int = -1
    name: str = ''
