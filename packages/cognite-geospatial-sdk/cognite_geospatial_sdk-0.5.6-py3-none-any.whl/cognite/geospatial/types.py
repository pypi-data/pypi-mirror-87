# Copyright 2020 Cognite AS
import pprint
from enum import Enum
from typing import Dict, List, NamedTuple

from cognite.geospatial._client import SpatialRelationshipNameDTO


class SpatialRelationship(Enum):
    within = SpatialRelationshipNameDTO.WITHIN
    within_distance = SpatialRelationshipNameDTO.WITHINDISTANCE
    within_completely = SpatialRelationshipNameDTO.WITHINCOMPLETELY
    intersect = SpatialRelationshipNameDTO.INTERSECT
    within_3d = SpatialRelationshipNameDTO.WITHIN3D
    within_distance_3d = SpatialRelationshipNameDTO.WITHINDISTANCE3D
    within_completely_3d = SpatialRelationshipNameDTO.WITHINCOMPLETELY3D
    intersect_3d = SpatialRelationshipNameDTO.INTERSECT3D


class Geometry:
    def __init__(
        self, id: int = None, external_id: str = None, wkt: str = None, crs: str = None, geojson: object = None
    ):
        self.id = id
        self.external_id = external_id
        self.wkt = wkt
        self.crs = crs
        self.geojson = geojson


class TextBasedGeometry:
    def __init__(self, geojson=None, crs: str = None, wkt: str = None):
        self.geojson = geojson
        self.crs = crs
        self.wkt = wkt

    def __repr__(self):
        return pprint.pformat(vars(self))


class DataExtractor(NamedTuple):
    attribute: str
    min_val: str
    max_val: str


class GridCoverage:
    """Map from a line to list of cross points
    """

    def __init__(self, cross_points_map: Dict[int, List[int]]):
        self.cross_points_map = cross_points_map

    def get_cross_points(self, line: int):
        """

        Args:
            line (int): the line number

        Returns:
            List[int]: a list of cross points on this line
        """
        return self.cross_points_map.get(line, [])

    def __str__(self):
        return "\n".join(["line {} -> {}".format(key, value) for key, value in self.cross_points_map.items()])
