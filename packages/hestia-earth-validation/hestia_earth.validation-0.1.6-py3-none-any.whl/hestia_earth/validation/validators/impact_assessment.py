from .shared import validate_list_duplicates, validate_list_min_max, validate_region, validate_country


def validate_impact_assessment(impact_assessment: dict):
    return [
        validate_country(impact_assessment) if 'country' in impact_assessment else True,
        validate_region(impact_assessment) if 'region' in impact_assessment else True
    ] + ([
        validate_list_min_max(impact_assessment, 'impacts'),
        validate_list_duplicates(impact_assessment, 'impacts', [
            'term.@id'
        ])
    ] if 'impacts' in impact_assessment else []) + ([
        validate_list_min_max(impact_assessment, 'emissionsResourceUse'),
        validate_list_duplicates(impact_assessment, 'emissionsResourceUse', [
            'term.@id'
        ])
    ] if 'emissionsResourceUse' in impact_assessment else [])
