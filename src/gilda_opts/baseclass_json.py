"""Base class for json dataclasses."""

from dataclasses_json import DataClassJsonMixin, Undefined, config


class BaseClassJson(DataClassJsonMixin):
    """Base Json Mixin."""

    dataclass_json_config = config(undefined=Undefined.RAISE)["dataclasses_json"]
