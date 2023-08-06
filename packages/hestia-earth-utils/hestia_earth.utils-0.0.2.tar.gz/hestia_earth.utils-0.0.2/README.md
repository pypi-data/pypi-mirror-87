# Hestia Utils

## Install

1. Install the module:
```bash
pip install hestia_earth.utils
```

## Usage

1. To download a file from the Hestia API:
```python
from hestia_earth.schema import SchemaType
from hestia_earth.utils import download_hestia

cycle = download_hestia('cycleId', SchemaType.CYCLE)
sandContent = download_hestia('sandContent', SchemaType.TERM)
```

2. To search for a specific Node on Hestia:
```python
from hestia_earth.schema import SchemaType
from hestia_earth.utils import find_node_exact

source = find_node_exact(SchemaType.SOURCE, {'bibliography.title.keyword': 'My Bibliography'})
```
