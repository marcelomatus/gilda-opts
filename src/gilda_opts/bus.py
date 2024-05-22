"""Bus class to represent where electric elements are connected."""

from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Bus(DataClassJsonMixin):
    """Bus class."""

    uid: int = -1
    name: str = ''
