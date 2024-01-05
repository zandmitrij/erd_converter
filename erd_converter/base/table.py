from __future__ import annotations

import dataclasses

from .field import Field


@dataclasses.dataclass
class Table:
    name: str
    fields: list[Field] = dataclasses.field(default_factory=lambda: [])
