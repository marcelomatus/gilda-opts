from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class Demand(DataClassJsonMixin):
    uid: int = -1
    name: str = ''
    load: float = 0.0
