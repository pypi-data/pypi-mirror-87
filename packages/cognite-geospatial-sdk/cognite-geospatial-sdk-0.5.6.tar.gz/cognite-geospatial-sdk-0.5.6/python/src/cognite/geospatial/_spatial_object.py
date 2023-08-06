# Copyright 2020 Cognite AS
from functools import lru_cache

import numpy as np
from cognite.geospatial._client import FullSpatialItemDTO
from cognite.geospatial._util import plot_geometry, plot_grid_point
from cognite.geospatial.types import Geometry
from shapely import wkt
from shapely.geometry import LineString

try:
    from collections.abc import Mapping  # noqa
    from collections.abc import MutableMapping  # noqa
except ImportError:
    from collections import Mapping  # noqa
    from collections import MutableMapping  # noqa


def _attributes_map(layer):
    if layer is None or layer.attributes is None:
        return {}
    attribute_map = {}
    for attribute in layer.attributes:
        attribute_map[attribute.name] = attribute
    return attribute_map


GEOMETRY_TYPES = [
    "point",
    "line",
    "polygon",
    "multipoint",
    "multiline",
    "multipolygon",
    "pointz",
    "linez",
    "polygonz",
    "multipointz",
    "multilinez",
    "multipolygonz",
    "surface",
]


def _is_geometry(layer_attribute):
    return layer_attribute.type in GEOMETRY_TYPES


def _is_number(layer_attribute):
    return layer_attribute.type in ["int", "long", "float", "double"]


class SpatialObject(FullSpatialItemDTO, Geometry):
    def __init__(self, client=None, spatial_item: FullSpatialItemDTO = None):
        self.client = client
        self.__dict__.update(spatial_item.__dict__)

        self._layer_info = None

        self.double_vector = {}
        self.integer_vector = {}
        self.boolean_vector = {}
        self.text_vector = {}

    def _set_layer_info(self, layer):
        self._layer_info = layer

    def layer_info(self):
        """Get spatial item layer.
        """
        if self._layer_info is None:
            self._layer_info = self.client.get_layer(name=self.layer)
        return self._layer_info

    def _add_double(self, name: str, vector):
        self.double_vector[name] = np.array(vector, dtype=np.double)

    def _add_integer(self, name: str, vector):
        self.integer_vector[name] = np.array(vector, dtype=np.int32)

    def _add_boolean(self, name: str, vector):
        self.boolean_vector[name] = np.array(vector, dtype=np.bool)

    def _add_text(self, name: str, value):
        self.text_vector[name] = value

    def __getitem__(self, name: str):
        if name in self.attributes:
            return self.attributes[name]

        if name in self.double_vector:
            return self.double_vector[name]

        if name in self.integer_vector:
            return self.integer_vector[name]

        if name in self.boolean_vector:
            return self.boolean_vector[name]

        if name in self.text_vector:
            return self.text_vector[name]

        attributes = self.client.get_attributes(attributes=[name], id=self.id)
        if name in attributes:
            return attributes[name]

        return None

    @lru_cache(maxsize=32)
    def coverage(self, dimensional_space: str = "2d", output_crs: str = None, geometry_format: str = None):
        """Retrieve the coverage of the spatial object.
        Args:
            dimensional_space (str): The geometry projection of the coverage. Valid values are "2d" (default), "3d"
            output_crs (str): the crs of the coverage
            geometry_format (str): Geometry format wkt or geojson
        """
        if output_crs is None:
            output_crs = self.crs

        coverage = self.client.get_coverage(output_crs=output_crs, id=self.id, dimensional_space=dimensional_space)
        if geometry_format is None or geometry_format == "wkt":
            return wkt.loads(coverage.coverage)

        return {"geojson": coverage}

    def delete(self) -> bool:
        """Delete spatial item.
        """
        item = self.client.delete_spatial(id=self.id)
        return item is not None

    def get(self):
        """ Get numpy arrays of x,y,z if the layer is raster/seismic/horizon. Otherwise, get geometry in the form of wkt
        """
        x_name, y_name, z_name = self._xyz()
        if self.layer == "raster" or self.layer == "seismic" or self.layer == "horizon":
            x = self.__getitem__(x_name)
            y = self.__getitem__(y_name)

            if z_name is None:
                data = np.stack((x, y), axis=-1)
            else:
                z = self.__getitem__(z_name)
                data = np.stack((x, y, z), axis=-1)
            if self.layer == "horizon":
                return data
            active = self.__getitem__("active")
            if active is None:
                return data
            active = active[: len(data)]
            return data[active]
        else:
            return self.geometry.wkt

    def height(self):
        """ Get the difference between maximum and minimum inline
        """
        rows = self._row_min_max()
        return self._get_side_size(rows, self._height_name())

    def width(self):
        """ Get the difference between maximum and minimum xline
        """
        columns = self._column_min_max()
        return self._get_side_size(columns, self._width_name())

    def _get_side_size(self, min_max, size_name):
        if min_max is not None:
            min_ = self.__getitem__(min_max[0])
            max_ = self.__getitem__(min_max[1])
            if min_ is not None and max_ is not None:
                return int(max_) - int(min_) + 1
        elif size_name is not None:
            return self.__getitem__(size_name)
        return None

    def _row_min_max(self):
        if self.layer == "seismic":
            return ("inline_min", "inline_max")
        return None

    def _column_min_max(self):
        if self.layer == "seismic":
            return ("xline_min", "xline_max")
        return None

    def _xyz(self):
        if self.layer == "horizon":
            return ("x", "y", "z")
        return ("x", "y", None)

    def _row_column(self):
        if self.layer == "horizon":
            row_name = "row"
            column_name = "column"
        elif self.layer == "seismic":
            row_name = "xline"
            column_name = "inline"
        return (row_name, column_name)

    def _height_name(self):
        if self.layer == "horizon":
            return "height"
        return None

    def _width_name(self):
        if self.layer == "horizon":
            return "width"
        return None

    def grid(self):
        """ Get the discrete grid representation if the layer is raster/seismic/horizon
        Seismic: grid[xline][inline] zero based index (grid[ xline - seismic_geo[“xline_min”] ][ inline - seismic_geo[“inline_min”] ]).
        """
        row_name, column_name = self._row_column()
        x_name, y_name, z_name = self._xyz()

        if self.layer == "raster" or self.layer == "seismic" or self.layer == "horizon":
            x = self.__getitem__(x_name)
            y = self.__getitem__(y_name)

            if z_name is None:
                points = np.stack((x, y), axis=-1)
            else:
                z = self.__getitem__(z_name)
                points = np.stack((x, y, z), axis=-1)

            width = self.width()
            height = self.height()

            if self.layer == "horizon":
                rows = self.__getitem__(row_name)
                columns = self.__getitem__(column_name)
                if rows is None or columns is None:
                    return None
                data = np.ndarray(shape=(height, width, points.shape[1]), dtype=np.double)
                for i in range(len(points)):
                    r = rows[i] - rows.min()
                    c = columns[i] - columns.min()
                    data[r, c] = points[i]
            else:
                active = self.__getitem__("active")
                data = np.ndarray(shape=(width, height, points.shape[1]), dtype=np.double)
                size = len(active)
                active_indx = np.argwhere(active[:size] == True)  # noqa: E712
                for i in active_indx:
                    r = int(i % height)
                    c = int((i - r) / height)
                    data[c, r] = points[i]

            return data
        return None

    def __str__(self):
        return f"id: {self.id}\nexternal_id: {self.external_id}\nname: {self.id}\nlayer: {self.layer}\ncrs: {self.crs}"

    def __hash__(self):
        return self.id

    def plot(self, attributes=None, label=None, title=None, xlabel="x", ylabel="y", output_crs=None):
        """ Plot coverage using holoview.

        Note:
            holoview should be installed separately.

        Args:
            attributes (List[str]): geometry attributes to visualize (default coverage)
            label (str): label of the geometry
            title (str): title of the plot
            xlabel (str): x axis label (default: x)
            ylabel (str): y axis label (default: y)
            output_crs (str): CRS of geometry
        Returns:
            holoview plot
        """
        plot = None
        if attributes is None:
            geometry = self.coverage(dimensional_space="2d", geometry_format="wkt", output_crs=output_crs)
            plot = plot_geometry(
                geometry, label=label or "Coverage", title=title or "Coverage", xlabel=xlabel, ylabel=ylabel
            )
        else:
            layer = self.layer_info()
            attribute_map = _attributes_map(layer)
            points = []
            for name in attributes:
                layer_attribute = attribute_map[name]
                value = self.__getitem__(name)
                if _is_geometry(layer_attribute):
                    geometry = wkt.loads(value)
                    if plot is None:
                        plot = plot_geometry(
                            geometry, label=label or name, title=title or name, xlabel=xlabel, ylabel=ylabel
                        )
                    else:
                        plot = plot * plot_geometry(
                            geometry, label=label or name, title=title or name, xlabel=xlabel, ylabel=ylabel
                        )
                elif _is_number(layer_attribute):
                    points.append(value)

            if len(points) > 0 and len(points) % 2 == 0:
                line = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]
                line.append(line[0])
                geometry = LineString(line)
                if plot is None:
                    plot = plot_geometry(
                        geometry, label=label or "Attributes", title=title or "Attributes", xlabel=xlabel, ylabel=ylabel
                    )
                else:
                    plot = plot * plot_geometry(
                        geometry, label=label or "Attributes", title=title or "Attributes", xlabel=xlabel, ylabel=ylabel
                    )

        return plot

    def plot_compute_grid(self):
        """ Plot compute grid  using holoview. Supported only for seismic layer.

        Note:
            holoview should be installed separately.

        Returns:
            holoview plot
        """
        layer = self.layer_info()
        if layer.name == "seismic":
            return self.plot(
                attributes=[
                    "inline_min",
                    "xline_min",
                    "inline_max",
                    "xline_min",
                    "inline_max",
                    "xline_max",
                    "inline_min",
                    "xline_max",
                ],
                title="Grid in xline/inline",
                label="File",
                xlabel="inline",
                ylabel="xline",
            )
        return None

    def plot_bounding(self):
        """ Plot bounded box of spatial object

        Note:
            holoview should be installed separately.

        Returns:
            holoview plot
        """
        layer = self.layer_info()
        if layer.name == "seismic":
            return self.plot(
                attributes=[
                    "top_left_x",
                    "top_left_y",
                    "top_right_x",
                    "top_right_y",
                    "bottom_right_x",
                    "bottom_right_y",
                    "bottom_left_x",
                    "bottom_left_y",
                ],
                label="File",
                title="Grid in UTM-coordinates",
                xlabel="UTM-X",
                ylabel="UTM-Y",
            )

        geometry = self.coverage(dimensional_space="2d", geometry_format="wkt")
        if geometry is not None:
            (minx, miny, maxx, maxy) = geometry.bounds
            box_geometry = LineString([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)])
            return plot_geometry(box_geometry, title="Grid in UTM-coordinates")

        return None

    def plot_grid(self, label="Grid", title="Grid", xlabel="x", ylabel="y"):
        """ Plot raster grid using holoview.

        Note:
            holoview and datashader should be installed separately.

        Args:
            label (str): label of the geometry
            title (str): title of the plot
            xlabel (str): x axis label (default: x)
            ylabel (str): y axis label (default: y)
        Returns:
            holoview plot
        """
        points_array = self.get()
        return plot_grid_point(points_array, label, title, xlabel, ylabel)


class SpatialList(list):
    def __init__(self, client, layer_name):
        self.client = client
        self.layer_name = layer_name

    def plot(self, attributes=None, label=None, title=None, xlabel="x", ylabel="y", output_crs=None):
        """ Plot all geoemtries of the list using holoview.

        Note:
            holoview should be installed separately.

        Args:
            attributes (List[str]): geometry attributes to visualize (default coverage)
            label (str): label of the geometry
            title (str): title of the plot
            xlabel (str): x axis label (default: x)
            ylabel (str): y axis label (default: y)
            output_crs (str): CRS of geometry
        Returns:
            holoview plot
        """
        plot = None
        for item in self:
            if plot is None:
                plot = item.plot(
                    attributes=attributes, label=label, title=title, xlabel=xlabel, ylabel=ylabel, output_crs=output_crs
                )
            else:
                plot = plot * item.plot(
                    attributes=attributes, label=label, title=title, xlabel=xlabel, ylabel=ylabel, output_crs=output_crs
                )
        return plot
