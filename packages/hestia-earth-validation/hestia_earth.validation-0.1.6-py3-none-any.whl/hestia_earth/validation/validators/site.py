from typing import List
from functools import reduce
from hestia_earth.schema import SiteSiteType

from hestia_earth.validation.geojson import get_geojson_area
from hestia_earth.validation.gadm import exec_request
from .shared import list_has_props, validate_dates, validate_list_dates, validate_list_duplicates, diff_in_years, \
    validate_list_min_max, validate_region, validate_country


SOIL_TEXTURE_IDS = ['sandContent', 'siltContent', 'clayContent']
INLAND_TYPES = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.PERMANENT_PASTURE.value,
    SiteSiteType.POND.value,
    SiteSiteType.BUILDING.value,
    SiteSiteType.FOREST.value,
    SiteSiteType.OTHER_NATURAL_VEGETATION.value
]


def group_measurements_depth(measurements: List[dict]):
    def group_by(group: dict, measurement: dict):
        key = measurement['depthUpper'] + measurement['depthLower'] \
            if 'depthUpper' in measurement and 'depthLower' in measurement else 'default'
        if key not in group:
            group[key] = []
        group[key].extend([measurement])
        return group

    return reduce(group_by, measurements, {})


def validate_soilTexture(measurements: List[dict]):
    def validate(values):
        values = list(filter(lambda v: v['term']['@id'] in SOIL_TEXTURE_IDS, values))
        terms = list(map(lambda v: v['term']['@id'], values))
        return len(set(terms)) != len(SOIL_TEXTURE_IDS) or 99.5 < sum(map(lambda v: v['value'], values)) < 100.5 or {
            'level': 'error',
            'dataPath': '.measurements',
            'message': 'The sum of Sand, Silt, and Clay content should equal 100% for each soil depth interval.'
        }

    results = list(map(validate, group_measurements_depth(measurements).values()))
    return next((x for x in results if x is not True), True)


def validate_depths(measurements: List[dict]):
    def validate(values):
        index = values[0]
        measurement = values[1]
        return measurement['depthUpper'] < measurement['depthLower'] or {
            'level': 'error',
            'dataPath': f".measurements[{index}].depthLower",
            'message': 'must be greater than depthUpper'
        }

    results = list(map(validate, enumerate(list_has_props(measurements, ['depthUpper', 'depthLower']))))
    return next((x for x in results if x is not True), True)


def value_range_error(value: int, minimum: int, maximum: int):
    return 'minimum' if minimum is not None and value < minimum else \
        'maximum' if maximum is not None and value > maximum else False


def validate_measurements_value(measurements: List[dict]):
    def validate(values):
        index = values[0]
        measurement = values[1]
        props = measurement.get('term', {}).get('defaultProperties', [])
        mininum = next((prop.get('value') for prop in props if prop.get('term', {}).get('@id') == 'minimum'), None)
        maximum = next((prop.get('value') for prop in props if prop.get('term', {}).get('@id') == 'maximum'), None)
        value = measurement.get('value')
        error = value_range_error(value, mininum, maximum) if value is not None else False
        return error is False or ({
            'level': 'error',
            'dataPath': f".measurements[{index}].value",
            'message': f"should be above {mininum}"
        } if error == 'minimum' else {
            'level': 'error',
            'dataPath': f".measurements[{index}].value",
            'message': f"should be below {maximum}"
        })

    results = list(map(validate, enumerate(measurements)))
    return next((x for x in results if x is not True), True)


def validate_lifespan(infrastructure: List[dict]):
    def validate(values):
        value = values[1]
        index = values[0]
        lifespan = diff_in_years(value.get('startDate'), value.get('endDate'))
        return lifespan == round(value.get('lifespan'), 1) or {
            'level': 'error',
            'dataPath': f".infrastructure[{index}].lifespan",
            'message': f"must equal to endDate - startDate in decimal years (~{lifespan})"
        }

    results = list(map(validate, enumerate(list_has_props(infrastructure, ['lifespan', 'startDate', 'endDate']))))
    return next((x for x in results if x is not True), True)


def validate_site_dates(site: dict):
    return validate_dates(site) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def validate_area(site: dict):
    try:
        area = get_geojson_area(site.get('boundary'))
        return area == round(site.get('area'), 1) or {
            'level': 'error',
            'dataPath': '.area',
            'message': f"must be equal to boundary (~{area})"
        }
    except KeyError:
        # if getting the geojson fails, the geojson format is invalid
        # and the schema validation step will detect it
        return True


def need_validate_coordinates(site: dict):
    return 'latitude' in site and 'longitude' in site and site.get('siteType') in INLAND_TYPES


def validate_coordinates(site: dict):
    latitude = site.get('latitude')
    longitude = site.get('longitude')
    country = site.get('country', {})
    region = site.get('region')
    gadm_id = region.get('@id') if region else country.get('@id')
    id = None if region else gadm_id  # pass in the id for a country for faster results
    res = exec_request(gadm_id, id=id, latitude=latitude, longitude=longitude)
    id = res.get('id')
    return (region and region.get('@id') == id) or (country.get('@id') == id) or {
        'level': 'error',
        'dataPath': '.region' if region else '.country',
        'message': 'does not contain latitude and longitude'
    }


def validate_site(site: dict):
    return [
        validate_site_dates(site),
        validate_country(site) if 'country' in site else True,
        validate_region(site) if 'region' in site else True,
        validate_coordinates(site) if need_validate_coordinates(site) else True,
        validate_area(site) if 'area' in site and 'boundary' in site else True
    ] + ([
        validate_list_dates(site, 'measurements'),
        validate_list_min_max(site, 'measurements'),
        validate_soilTexture(site.get('measurements')),
        validate_depths(site.get('measurements')),
        validate_measurements_value(site.get('measurements')),
        validate_list_duplicates(site, 'measurements', [
            'term.@id',
            'method.@id',
            'methodDescription',
            'startDate',
            'endDate',
            'depthUpper',
            'depthLower'
        ])
    ] if 'measurements' in site else []) + ([
        validate_list_dates(site, 'infrastructure'),
        validate_lifespan(site.get('infrastructure'))
    ] if 'infrastructure' in site else [])
