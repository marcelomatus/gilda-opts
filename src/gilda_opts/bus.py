from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class Bus(DataClassJsonMixin):
    uid: int = -1
    name: str = ''
