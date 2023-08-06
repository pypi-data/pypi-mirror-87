import os
from typing import List, Mapping, Optional, Tuple, Union

from cognite.seismic._api.utility import MaybeString

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import (
        Geometry as GeometryProto,
        IngestionSource,
        CRS as CRSProto,
        GeoJson,
        Wkt,
    )
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import (
        TextHeader as TextHeaderProto,
        BinaryHeader as BinaryHeaderProto,
    )
else:
    from enum import Enum

    class IngestionSource(Enum):
        INVALID_SOURCE = 0
        FILE_SOURCE = 1
        TRACE_WRITER = 2


# Contains types returned by the SDK API.


class Coordinate:
    """Represents physical coordinates in a given CRS."""

    crs: str
    x: float
    y: float

    def __init__(self, crs, x, y):
        self.crs = crs
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coordinate<crs: {self.crs}, x: {self.x}, y: {self.y}>"

    @staticmethod
    def from_proto(proto) -> "Coordinate":
        return Coordinate(crs=proto.crs, x=proto.x, y=proto.y)


class Trace:
    """Represents a seismic trace with a single inline / crossline coordinate."""

    trace_header: bytes
    inline: int
    crossline: int
    trace: List[float]
    coordinate: Coordinate

    def __init__(self, trace_header, inline, crossline, trace, coordinate):
        self.trace_header = trace_header
        self.inline = inline
        self.crossline = crossline
        self.trace = trace
        self.coordinate = coordinate

    def __repr__(self):
        return f"Trace<inline: {self.inline}, crossline: {self.crossline}, coordinates: {str(self.coordinate)}, trace: {self.trace}>"

    @staticmethod
    def from_proto(proto) -> "Trace":
        return Trace(
            trace_header=proto.trace_header,
            inline=proto.iline.value,
            crossline=proto.xline.value,
            trace=proto.trace,
            coordinate=Coordinate.from_proto(proto.coordinate),
        )


class VolumeDef:
    """Represents a VolumeDef, a method to describe an inline/crossline grid. Refer to /volumedef.md for more information."""

    json: str

    def __init__(self, json):
        self.json = json

    def __repr__(self):
        return f"VolumeDef<{self.json}>"

    def from_proto(proto) -> "VolumeDef":
        return VolumeDef(json=proto.json)


class File:
    """Represents a raw SEGY file."""

    id: str
    name: str
    metadata: Mapping[str, str]
    is_temporary: bool

    def __init__(self, *, id, name, metadata, is_temporary):
        self.id = id
        self.name = name
        self.metadata = metadata
        self.is_temporary = is_temporary

    def __repr__(self):
        temporary = ", temporary" if self.is_temporary else ""
        return f"File<id: {self.id}, name: {self.name}{temporary}, metadata: {metadata}>"

    @staticmethod
    def from_proto(proto) -> "File":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]
        return File(id=proto.id, name=proto.name, metadata=metadata, is_temporary=proto.is_temporary)


class Geometry:
    """Represents a CRS + shape, in either a WKT format or a GeoJSON."""

    crs: str
    geojson: Optional[dict]
    wkt: Optional[str]

    def __init__(self, crs: str, *, geojson=None, wkt=None):
        if (geojson is None) and (wkt is None):
            raise ValueError("You must specify one of: geojson, wkt")
        if (geojson is not None) and (wkt is not None):
            raise ValueError("You must specify either of: geojson, wkt")
        self.crs = crs
        self.geojson = geojson
        self.wkt = wkt

    def __repr__(self):
        if geojson:
            return f"Geometry<crs: {self.crs}, geojson: {self.geojson}>"
        else:
            return f"Geometry<crs: {self.crs}, wkt: {self.wkt}>"

    @staticmethod
    def from_proto(proto) -> Union["Geometry", None]:
        """Convert a Geometry proto into a Geometry object.

        May return None if neither geojson nor wkt are specified.        
        """
        crs = proto.crs.crs
        # TODO: the json is a Struct, when it should probably be a python type.
        geojson = proto.geo.json or None
        wkt = proto.wkt.geometry or None
        if geojson is None and wkt is None:
            return None
        return Geometry(crs=crs, geojson=geojson, wkt=wkt)

    def to_proto(self):
        crs_proto = CRSProto(crs=self.crs)
        if self.geojson is not None:
            return GeometryProto(crs=crs_proto, geo=GeoJson(json=self.geojson))
        if self.wkt is not None:
            return GeometryProto(crs=crs_proto, wkt=Wkt(geometry=self.wkt))


class TextHeader:
    """A representation of text headers used to create or edit existing headers."""

    def __init__(self, *, header: MaybeString = None, raw_header: MaybeString = None):
        """Create a text header.

        Specify either header or raw_header.
        
        Args:
            header (String | None): The text content of a header
            raw_header (String | None): The raw bytes of a header
        """
        self.header = header
        self.raw_header = raw_header

    def __repr__(self):
        return f"TextHeader<{self.header}>"

    def from_proto(proto):
        return TextHeader(header=proto.header, raw_header=proto.raw_header)

    def into_proto(self):
        return TextHeaderProto(header=self.header, raw_header=self.raw_header)


class BinaryHeader:
    """A representation of binary headers used to create or edit existing headers.
    
    BinaryHeader.FIELDS contains the list of valid fields. to set after the object is constructed.
    """

    FIELDS = (
        "traces",
        "trace_data_type",
        "fixed_length_traces",
        "segy_revision",
        "auxtraces",
        "interval",
        "interval_original",
        "samples",
        "samples_original",
        "ensemble_fold",
        "vertical_sum",
        "trace_type_sorting_code",
        "sweep_type_code",
        "sweep_frequency_start",
        "sweep_frequency_end",
        "sweep_length",
        "sweep_channel",
        "sweep_taper_start",
        "sweep_taper_end",
        "sweep_taper_type",
        "correlated_traces",
        "amplitude_recovery",
        "original_measurement_system",
        "impulse_signal_polarity",
        "vibratory_polarity_code",
    )

    def __init__(self, *args, raw_header: Union[bytes, None] = None, **kwargs):
        """Initialize.
        
        Args:
            *args (int): An optional list of arguments. The fields are assigned to the binary_header fields in sequential order, and missing fields are assigned None.
            **kwargs (int): An optional key-value mapping of arguments, which overwrite any values from *args.
            raw_header (bytes | None): Optional raw header.            
        """
        for i, field in enumerate(BinaryHeader.FIELDS):
            val = args[i] if i < len(args) else None
            val = kwargs[field] if field in kwargs else val
            setattr(self, field, val)
        self.raw_header = raw_header

    def __repr__(self):
        fields = []
        for field in self.FIELDS:
            val = getattr(self, field)
            if val:
                field_strings.push(f"{field}: {val}")
        fields = fields.join(", ")
        return f"BinaryHeader<{fields}>"

    @staticmethod
    def from_proto(proto) -> "BinaryHeader":
        return BinaryHeader(
            traces=proto.traces,
            trace_data_type=proto.trace_data_type,
            fixed_length_traces=proto.fixed_length_traces,
            segy_revision=proto.segy_revision,
            auxtraces=proto.auxtraces,
            interval=proto.interval,
            interval_original=proto.interval_original,
            samples=proto.samples,
            samples_original=proto.samples_original,
            ensemble_fold=proto.ensemble_fold,
            vertical_sum=proto.vertical_sum,
            trace_type_sorting_code=proto.trace_type_sorting_code,
            sweep_type_code=proto.sweep_type_code,
            sweep_frequency_start=proto.sweep_frequency_start,
            sweep_frequency_end=proto.sweep_frequency_end,
            sweep_length=proto.sweep_length,
            sweep_channel=proto.sweep_channel,
            sweep_taper_start=proto.sweep_taper_start,
            sweep_taper_end=proto.sweep_taper_end,
            sweep_taper_type=proto.sweep_taper_type,
            correlated_traces=proto.correlated_traces,
            amplitude_recovery=proto.amplitude_recovery,
            original_measurement_system=proto.original_measurement_system,
            impulse_signal_polarity=proto.impulse_signal_polarity,
            vibratory_polarity_code=proto.vibratory_polarity_code,
            raw_header=proto.raw_header,
        )

    def into_proto(self):
        return BinaryHeaderProto(
            traces=self.traces,
            trace_data_type=self.trace_data_type,
            fixed_length_traces=self.fixed_length_traces,
            segy_revision=self.segy_revision,
            auxtraces=self.auxtraces,
            interval=self.interval,
            interval_original=self.interval_original,
            samples=self.samples,
            samples_original=self.samples_original,
            ensemble_fold=self.ensemble_fold,
            vertical_sum=self.vertical_sum,
            trace_type_sorting_code=self.trace_type_sorting_code,
            sweep_type_code=self.sweep_type_code,
            sweep_frequency_start=self.sweep_frequency_start,
            sweep_frequency_end=self.sweep_frequency_end,
            sweep_length=self.sweep_length,
            sweep_channel=self.sweep_channel,
            sweep_taper_start=self.sweep_taper_start,
            sweep_taper_end=self.sweep_taper_end,
            sweep_taper_type=self.sweep_taper_type,
            correlated_traces=self.correlated_traces,
            amplitude_recovery=self.amplitude_recovery,
            original_measurement_system=self.original_measurement_system,
            impulse_signal_polarity=self.impulse_signal_polarity,
            vibratory_polarity_code=self.vibratory_polarity_code,
            raw_header=self.raw_header,
        )


class SeismicStore:
    """Represents a seismic store."""

    id: int
    name: str
    survey_id: str
    ingestion_source: IngestionSource
    metadata: Mapping[str, str]
    ingested_file: Optional[File]
    inline_volume_def: Optional[VolumeDef]
    crossline_volume_def: Optional[VolumeDef]
    coverage: Geometry
    text_header: Optional[TextHeader]
    binary_header: Optional[BinaryHeader]
    storage_tier_name: List[str]

    def __init__(
        self,
        *,
        id,
        name,
        survey_id,
        ingestion_source,
        metadata,
        ingested_file,
        inline_volume_def,
        crossline_volume_def,
        coverage,
        text_header,
        binary_header,
        storage_tier_name,
    ):
        self.id = id
        self.name = name
        self.survey_id = survey_id
        self.ingestion_source = ingestion_source
        self.metadata = metadata
        self.ingested_file = ingested_file
        self.inline_volume_def = inline_volume_def
        self.crossline_volume_def = crossline_volume_def
        self.coverage = coverage
        self.text_header = text_header
        self.binary_header = binary_header
        self.storage_tier_name = storage_tier_name

    def __repr__(self):
        return f"SeismicStore<id: {self.id}, name: {self.name}, survey_id: {self.survey_id}, ingestion_source: {self.ingestion_source}, metadata: {self.metadata}, storage_tier: {self.storage_tier_name}>"

    @staticmethod
    def from_proto(proto) -> "SeismicStore":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]
        return SeismicStore(
            id=proto.id,
            name=proto.name,
            survey_id=proto.survey_id,
            ingestion_source=proto.ingestion_source,
            metadata=metadata,
            ingested_file=proto.ingested_file,
            inline_volume_def=VolumeDef.from_proto(proto.inline_volume_def),
            crossline_volume_def=VolumeDef.from_proto(proto.crossline_volume_def),
            coverage=proto.coverage,
            binary_header=BinaryHeader.from_proto(proto.binary_header),
            text_header=TextHeader.from_proto(proto.text_header),
            storage_tier_name=proto.storage_tier_name,
        )


class Seismic:
    """Represents a seismic, a subset of a seismic store."""

    id: int
    external_id: str
    name: str
    crs: str
    metadata: Mapping[str, str]
    text_header: Optional[TextHeader]
    binary_header: Optional[BinaryHeader]
    line_range: Optional[Tuple[int, int]]
    volume_def: Optional[VolumeDef]
    partition_id: int
    seismicstore_id: Optional[int]
    coverage: Optional[Geometry]

    def __init__(
        self,
        *,
        id,
        external_id,
        name,
        crs,
        metadata,
        text_header,
        binary_header,
        line_range,
        volume_def,
        partition_id,
        seismicstore_id,
        coverage,
    ):
        self.id = id
        self.external_id = external_id
        self.name = name
        self.crs = crs
        self.metadata = metadata
        self.text_header = text_header
        self.binary_header = binary_header
        self.line_range = line_range
        self.volume_def = volume_def
        self.partition_id = partition_id
        self.seismicstore_id = seismicstore_id
        self.coverage = coverage

    def __repr__(self):
        return f"Seismic<id: {self.id}, external_id: {self.external_id}, name: {self.name}, crs: {self.crs}, metadata: {self.metadata}>"

    @staticmethod
    def from_proto(proto) -> "Seismic":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]
        return Seismic(
            id=proto.id,
            external_id=proto.external_id,
            name=proto.name,
            crs=proto.crs,
            metadata=metadata,
            text_header=TextHeader.from_proto(proto.text_header),
            binary_header=BinaryHeader.from_proto(proto.binary_header),
            line_range=(proto.line_range.from_line, proto.line_range.to_line),
            volume_def=VolumeDef.from_proto(proto.volume_def),
            partition_id=proto.partition_id,
            seismicstore_id=proto.seismicstore_id,
            coverage=Geometry.from_proto(proto.coverage),
        )


class Partition:
    """Represents a partition and its included seismics"""

    id: int
    external_id: str
    name: str
    seismics: List[Seismic]

    def __init__(self, *, id, external_id, name, seismics):
        self.id = id
        self.external_id = external_id
        self.name = name
        self.seismics = seismics

    def __repr__(self):
        return f"Partition<id: {self.id}, external_id: {self.external_id}, name: {self.name}>"

    @staticmethod
    def from_proto(proto) -> "Partition":
        seismics = [Seismic.from_proto(s) for s in proto.seismics]
        return Partition(id=proto.id, external_id=proto.external_id, name=proto.name, seismics=seismics)
