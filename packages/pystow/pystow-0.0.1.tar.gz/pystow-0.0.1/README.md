# PyStow

Easily pick a place to store data to go with your python package.

Install with: `pip install pystow`

Example usage:

```python
import pystow

# Get a directory (as a pathlib.Path)
pykeen_directory = pystow.get('pykeen')

# Get a subdirectory (as a pathlib.Path).
# You can specify as deep as you want.
pykeen_experiments_directory = pystow.get('pykeen', 'experiments')
```
