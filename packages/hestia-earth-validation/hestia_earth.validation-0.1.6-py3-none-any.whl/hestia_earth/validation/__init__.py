from pkgutil import extend_path
from typing import List
from concurrent.futures import ThreadPoolExecutor

from .validators import validate_node

__path__ = extend_path(__path__, __name__)


def validate(nodes: List[dict]):
    with ThreadPoolExecutor() as executor:
        return list(executor.map(validate_node, nodes))
