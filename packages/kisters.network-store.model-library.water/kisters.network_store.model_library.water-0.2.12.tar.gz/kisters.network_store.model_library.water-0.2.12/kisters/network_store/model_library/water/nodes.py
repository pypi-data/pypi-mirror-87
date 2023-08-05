from typing import List, Any, Optional

from pydantic import Field, validator

from kisters.network_store.model_library.base import BaseNode as _BaseNode
from kisters.network_store.model_library.base import Model as _Model


class _Node(_BaseNode):
    domain: str = Field("water", const=True)


class Junction(_Node):
    element_class: str = Field("Junction", const=True)
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )


class LevelBoundary(_Node):
    element_class: str = Field("LevelBoundary", const=True)
    initial_flow: Optional[float] = Field(
        None, description="Initial volumetric flow rate for simulation in m^3/s"
    )


class FlowBoundary(_Node):
    element_class: str = Field("FlowBoundary", const=True)
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )


class _StorageLevelVolume(_Model):
    level: float
    volume: float = Field(..., ge=0.0)


class Storage(_Node):
    element_class: str = Field("Storage", const=True)
    level_volume: List[_StorageLevelVolume] = Field(..., min_items=2)
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )

    @validator("level_volume")
    def check_monotonic(cls, v: Any) -> Any:
        volumes = [d.volume for d in v]
        if not all(a < b for a, b in zip(volumes, volumes[1:])):
            raise ValueError("Volume must be specified in strictly increasing order")
        return v
