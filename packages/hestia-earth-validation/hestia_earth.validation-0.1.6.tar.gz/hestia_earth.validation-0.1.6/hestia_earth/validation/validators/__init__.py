from functools import reduce
from hestia_earth.schema import NodeType

from .cycle import validate_cycle
from .impact_assessment import validate_impact_assessment
from .organisation import validate_organisation
from .site import validate_site


VALIDATE_NODE_TYPE = {
    NodeType.CYCLE.value: lambda v: validate_cycle(v),
    NodeType.IMPACTASSESSMENT.value: lambda v: validate_impact_assessment(v),
    NodeType.ORGANISATION.value: lambda v: validate_organisation(v),
    NodeType.SITE.value: lambda v: validate_site(v)
}


def flatten(values: list):
    return list(reduce(lambda x, y: x + (y if isinstance(y, list) else [y]), values, []))


def update_error(error: dict, key: str, index=None):
    path = f".{key}[{index}]{error.get('dataPath')}" if index is not None else f".{key}{error.get('dataPath')}"
    return {**error, **{'dataPath': path}}


def validate_node_children(node: dict):
    validations = []
    for key, value in node.items():
        if isinstance(value, list):
            validations.extend([validate_node_child(key, value, index) for index, value in enumerate(value)])
        if isinstance(value, dict):
            validations.append(validate_node_child(key, value))
    return flatten(validations)


def validate_node_child(key: str, value: dict, index=None):
    values = validate_node(value)
    return list(map(lambda error: update_error(error, key, index) if isinstance(error, dict) else error, values))


def validate_node(node: dict):
    ntype = node.get('type', node.get('@type')) if isinstance(node, dict) else None
    if ntype is None:
        return []
    validations = flatten(
        (VALIDATE_NODE_TYPE[ntype](node) if ntype in VALIDATE_NODE_TYPE else []) +
        validate_node_children(node)
    )
    return list(filter(lambda v: v is not True, validations))
