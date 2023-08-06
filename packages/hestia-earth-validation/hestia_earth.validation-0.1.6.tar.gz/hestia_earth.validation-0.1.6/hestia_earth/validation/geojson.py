from area import area


GEOMETRY_BY_TYPE = {
    'FeatureCollection': lambda x: get_geometry_by_type(x.get('features')[0]),
    'GeometryCollection': lambda x: get_geometry_by_type(x.get('geometries')[0]),
    'Feature': lambda x: x.get('geometry'),
    'Polygon': lambda x: x,
    'MultiPolygon': lambda x: x
}


def get_geometry_by_type(geojson): return GEOMETRY_BY_TYPE[geojson.get('type')](geojson)


def get_geojson_area(geojson: dict): return round(area(get_geometry_by_type(geojson)) / 10000, 1)
