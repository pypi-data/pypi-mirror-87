import enum
import math
from typing import Any, Dict, List, Optional, Union

from kisters.network_store.model_library.base import BaseLink as _BaseLink
from kisters.network_store.model_library.base import Model as _Model
from pydantic import Field, validator


class _Link(_BaseLink):
    domain: str = Field("water", const=True)


class Delay(_Link):
    element_class: str = Field("Delay", const=True)
    transit_time: float = Field(
        0.0, ge=0.0, description="Time delay in seconds between source and target nodes"
    )


class PipeFrictionModel(str, enum.Enum):
    DARCY_WEISBACH = "darcy-weisbach"
    HAZEN_WILLIAMS = "hazen-williams"


class Pipe(_Link):
    element_class: str = Field("Pipe", const=True)
    diameter: float = Field(..., gt=0.0, description="Measured internal diameter")
    length: float = Field(..., gt=0.0, description="Longitudinal length of the pipe")
    roughness: float = Field(..., gt=0.0, description="Friction coefficient")
    model: PipeFrictionModel = Field(
        ..., description="Friction loss approximation method"
    )
    check_valve: Optional[bool] = Field(False, description="Disallow reverse flow")


class ChannelRoughnessModel(str, enum.Enum):
    CHEZY = "chezy"
    MANNING = "manning"


class HydraulicRoutingModel(str, enum.Enum):
    SAINT_VENANT = "saint-venant"
    INERTIAL_WAVE = "inertial-wave"
    DIFFUSIVE_WAVE = "diffusive-wave"


class _HydraulicCrossSectionStation(_Model):
    lr: float = Field(
        ..., description="Station distance from left bank when looking downstream"
    )
    z: float = Field(..., description="Station elevation")
    roughness_correction: Optional[float] = Field(
        None,
        description="Local roughness correction (acts as multiplier on base roughness)",
    )


class _HydraulicLongitudinalStation(_Model):
    roughness: float = Field(..., gt=0.0, description="Friction coefficient")
    cross_section: List[_HydraulicCrossSectionStation] = Field(
        ..., min_items=3, description="List of points defining the channel bottom"
    )
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )

    @validator("cross_section")
    def check_cross_section_stations(cls, v: Any) -> Any:
        if sorted(v, key=lambda x: x.lr) != v:
            raise ValueError(
                "Cross Section Stations must be specified in increasing order"
            )
        return v

    @validator("cross_section")
    def check_non_empty(cls, v: Any) -> Any:
        z = [x.z for x in v]
        if min(z) >= max(z):
            raise ValueError("Empty cross section specified")
        return v


class _LongitudinalDelimitedStation(_Model):
    distance: float = Field(
        ..., ge=0.0, description="Distance along channel from source node"
    )


class _HydraulicLongitudinalDelimitedStation(
    _HydraulicLongitudinalStation, _LongitudinalDelimitedStation
):
    pass


class _HydraulicRouting(_Model):
    model: HydraulicRoutingModel = Field(
        ..., description="Hydraulics approximation equations"
    )
    stations: Union[
        _HydraulicLongitudinalStation, List[_HydraulicLongitudinalDelimitedStation]
    ] = Field(
        ..., min_items=1, description="Longitudinal stations defining channel geometry"
    )
    roughness_model: ChannelRoughnessModel = Field(
        ChannelRoughnessModel.CHEZY, description="Friction loss approximation method"
    )
    initial_flow: Optional[float] = Field(
        None, description="Initial volumetric flow rate for simulation in m3/s"
    )

    @validator("stations")
    def stations_sorted(cls, v: Any) -> Any:
        if isinstance(v, list):
            return sorted(v, key=lambda x: x.distance)
        return v

    @validator("stations")
    def stations_unique(cls, v: Any) -> Any:
        if isinstance(v, list):
            distances = [s.distance for s in v]
            unique_distances = sorted(set(distances))
            if distances != unique_distances:
                raise ValueError("Two stations may not be placed at the same distance")
        return v


class _MuskingumCungeLongitudinalStation(_Model):
    k: float = Field(..., description="Storage coefficient")
    x: float = Field(..., description="Weighting factor")


class _MuskingumCungeLongitudinalDelimitedStation(
    _MuskingumCungeLongitudinalStation, _LongitudinalDelimitedStation
):
    pass


class HydrologicRoutingModel(str, enum.Enum):
    MUSKINGUM_CUNGE = "muskingum-cunge"


class _HydrologicRouting(_Model):
    model: HydrologicRoutingModel = Field(
        ..., description="Hydrology flow routing scheme"
    )
    stations: Union[
        _MuskingumCungeLongitudinalStation,
        List[_MuskingumCungeLongitudinalDelimitedStation],
    ] = Field(
        ...,
        min_items=1,
        description="Longitudinal stations characterizing channel hydrology",
    )

    @validator("stations")
    def stations_sorted(cls, v: Any) -> Any:
        if isinstance(v, list):
            return sorted(v, key=lambda x: x.distance)
        return v

    @validator("stations")
    def stations_unique(cls, v: Any) -> Any:
        if isinstance(v, list):
            distances = [s.distance for s in v]
            unique_distances = sorted(set(distances))
            if distances != unique_distances:
                raise ValueError("Two stations may not be placed at the same distance")
        return v


class Channel(_Link):
    element_class: str = Field("Channel", const=True)
    length: float = Field(..., gt=0.0, description="Longitudinal length of the channel")
    hydraulic_routing: _HydraulicRouting = Field(
        None, description="Hydraulic routing model"
    )
    hydrologic_routing: _HydrologicRouting = Field(
        None, description="Hydrologic routing model"
    )

    @validator("hydraulic_routing", "hydrologic_routing")
    def check_distance_less_than_length(cls, v: Any, values: Dict[str, Any]) -> Any:
        if isinstance(v.stations, list):
            if v.stations[-1].distance > values["length"]:
                raise ValueError(
                    f"Station {v.stations[-1].distance} distance exceeds"
                    f" length {values['length']}"
                )
        return v


class FlowControlledStructure(_Link):
    element_class: str = Field("FlowControlledStructure", const=True)
    min_flow: float = Field(..., description="Minimum volumetric flow rate in m^3/s")
    max_flow: float = Field(..., description="Maximum volumetric flow rate in m^3/s")
    initial_flow: Optional[float] = Field(
        None, description="Initial volumetric flow rate for simulation in m^3/s"
    )

    @validator("max_flow")
    def min_flow_le_max_flow(cls, v: Any, values: Dict[str, Any]) -> Any:
        min_flow = values.get("min_flow")
        if min_flow is not None and v < min_flow:
            raise ValueError("max_flow must be greater than min_flow")
        return v

    @validator("min_flow", "max_flow")
    def bounds_are_real_valued(cls, v: Any) -> Any:
        if v is not None and not math.isfinite(v):
            raise ValueError("Only real-valued bounds are allowed")
        return v


class _PumpTurbineSpeedPoint(_Model):
    flow: float = Field(..., ge=0.0)
    head: float = Field(..., ge=0.0)
    speed: float = Field(1.0, ge=0.0)


class _PumpTurbineEfficiencyPoint(_Model):
    flow: float = Field(..., ge=0.0)
    head: float = Field(..., ge=0.0)
    efficiency: float = Field(..., gt=0.0, le=1.0)


class _PumpTurbineHeadTWCorrection(_Model):
    link_uid: str = Field(..., regex="^[a-zA-Z]\\w*$")
    power: int = Field(..., ge=0.0)
    value: float


class _PumpTurbineOtherConstraints(_Model):
    flow_power: int = Field(..., ge=0.0)
    head_power: int = Field(..., ge=0.0)
    value: float


class _PumpTurbine(_Link):
    speed: Optional[List[_PumpTurbineSpeedPoint]] = Field(
        None, min_items=1, description="Flow-head-speed curve of drive shaft"
    )
    efficiency: Optional[List[_PumpTurbineEfficiencyPoint]] = Field(
        None,
        min_items=1,
        description="Flow-head-efficiency energy conversion curve of assembly",
    )
    length: Optional[float] = Field(None, gt=0.0, description="Length of flow path")
    min_flow: float = Field(..., description="Minimum volumetric flow rate in m^3/s")
    max_flow: float = Field(..., description="Maximum volumetric flow rate in m^3/s")
    initial_flow: Optional[float] = Field(
        None, description="Initial volumetric flow rate for simulation in m^3/s"
    )
    min_head: Optional[float] = Field(None, ge=0.0, description="Minimum head in m")
    max_head: Optional[float] = Field(None, ge=0.0, description="Maximum head in m")
    min_power: float = Field(..., description="Minimum power in W")
    max_power: float = Field(..., description="Maximum power in W")
    min_speed: Optional[float] = Field(None, ge=0.0, description="Minimum speed")
    max_speed: Optional[float] = Field(None, ge=0.0, description="Maximum speed")
    head_tailwater_correction: Optional[List[_PumpTurbineHeadTWCorrection]] = Field(
        None,
        description="This polynomial is added to the difference between"
        " up- and downstream levels",
    )
    other_constraints: Optional[List[_PumpTurbineOtherConstraints]] = Field(
        None, description="Every polynomial will be added a constraint <= 0"
    )

    @validator(
        "min_flow",
        "max_flow",
        "min_head",
        "max_head",
        "min_power",
        "max_power",
        "min_speed",
        "max_speed",
    )
    def bounds_are_real_valued(cls, v: Any) -> Any:
        if v is not None and not math.isfinite(v):
            raise ValueError("Only real-valued bounds are allowed")
        return v

    @validator("max_flow")
    def min_flow_le_max_flow(cls, v: Any, values: Dict[str, Any]) -> Any:
        min_flow = values.get("min_flow")
        if min_flow is not None and v < min_flow:
            raise ValueError("max_flow must be greater than min_flow")
        return v

    @validator("max_head")
    def min_head_le_max_head(cls, v: Any, values: Dict[str, Any]) -> Any:
        min_head = values.get("min_head")
        if min_head is not None and v < min_head:
            raise ValueError("max_head must be greater than min_head")
        return v

    @validator("max_power")
    def min_power_le_max_power(cls, v: Any, values: Dict[str, Any]) -> Any:
        min_power = values.get("min_power")
        if min_power is not None and v < min_power:
            raise ValueError("max_power must be greater than min_power")
        return v

    @validator("max_speed")
    def min_speed_le_max_speed(cls, v: Any, values: Dict[str, Any]) -> Any:
        min_speed = values.get("min_speed")
        if min_speed is not None and v < min_speed:
            raise ValueError("max_speed must be greater than min_speed")
        return v


class Pump(_PumpTurbine):
    element_class: str = Field("Pump", const=True)


class Turbine(_PumpTurbine):
    element_class: str = Field("Turbine", const=True)


class ValveModel(str, enum.Enum):
    PRV = "prv"
    PSV = "psv"
    PBV = "pbv"
    FCV = "fcv"
    TCV = "tcv"
    GPV = "gpv"


class Valve(_Link):
    element_class: str = Field("Valve", const=True)
    model: ValveModel = Field(..., description="Specific type of valve")
    coefficient: float = Field(..., gt=0.0, description="Discharge coefficient")
    diameter: float = Field(
        ..., ge=0.0, description="Measured characteristic internal diameter"
    )
    setting: float = Field(
        ..., description="Valve setting, meaning varies with valve model"
    )


class FlowModel(str, enum.Enum):
    FREE = "free"
    SUBMERGED = "submerged"
    DYNAMIC = "dynamic"


class _FlowRelation(_Link):
    coefficient: float = Field(..., gt=0.0, description="Discharge coefficient")
    flow_model: FlowModel = Field(..., description="Flow model")


class Weir(_FlowRelation):
    element_class: str = Field("Weir", const=True)
    min_crest_level: float = Field(..., description="Minimum crest level")
    max_crest_level: float = Field(..., description="Maximum crest level")
    initial_crest_level: Optional[float] = Field(
        None, description="Initial crest level value for simulation"
    )
    crest_width: float = Field(..., gt=0.0)

    @validator("max_crest_level")
    def min_crest_level_le_max_crest_level(cls, v: Any, values: Dict[str, Any]) -> Any:
        min_crest_level = values.get("min_crest_level")
        if min_crest_level is not None and v < min_crest_level:
            raise ValueError("max_crest_level must be greater than min_crest_level")
        return v


class _TopDownOrifice(_FlowRelation):
    bottom_level: float = Field(..., description="Bottom level")
    min_top_level: float = Field(..., description="Minimum top level")
    max_top_level: float = Field(..., description="Maximum top level")
    reference_width: float = Field(..., gt=0.0)


class TopDownRectangularOrifice(_FlowRelation):
    element_class: str = Field("TopDownRectangularOrifice", const=True)


class TopDownSphericalOrifice(_FlowRelation):
    element_class: str = Field("TopDownSphericalOrifice", const=True)


class Drain(_FlowRelation):
    element_class: str = Field("Drain", const=True)
    level: float = Field(..., description="Level at which drain is installed")
    min_area: float = Field(..., ge=0.0, description="Minimum aperture area")
    max_area: float = Field(..., gt=0.0, description="Maximum aperture area")
    initial_area: Optional[float] = Field(
        None, description="Initial area value for simulation"
    )
