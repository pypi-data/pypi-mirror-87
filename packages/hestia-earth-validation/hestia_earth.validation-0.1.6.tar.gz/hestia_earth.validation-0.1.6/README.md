# Hestia Data Validation

## Install

```bash
pip install hestia_earth.validation
```

### Usage

```python
from hestia_earth.validation import validate

# for each node, this will return a list containing all the errors/warnings (empty list if no errors/warnings)
errors = validate(nodes)
```
