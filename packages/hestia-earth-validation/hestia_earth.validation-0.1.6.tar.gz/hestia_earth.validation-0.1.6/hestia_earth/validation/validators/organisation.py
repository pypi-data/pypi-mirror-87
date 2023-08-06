from .shared import validate_dates


def validate_organisation_dates(organisation: dict):
    return validate_dates(organisation) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def validate_organisation(organisation: dict):
    return [
        validate_organisation_dates(organisation)
    ]
