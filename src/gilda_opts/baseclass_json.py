"""Base class for json dataclasses."""

from dataclasses_json import Undefined, dataclass_json
from dataclass_wizard import JSONWizard


@dataclass_json(undefined=Undefined.RAISE)
class BaseClassJson(JSONWizard):
    """Base Json Mixin.

    If a unknown key is found in JSON, an exception will RAISE.
    """
