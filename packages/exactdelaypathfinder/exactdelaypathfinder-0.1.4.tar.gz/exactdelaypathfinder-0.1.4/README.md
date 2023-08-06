This library was created by Florida International University's AMLight Team. For commercial and personal use.

This pathfinding tool uses [*NetworkX*](https://networkx.org/) graphs to find a list of paths with a total delay close to the user requirements - the first path in the list is the best match. 

## How to Install

Create and activate a virtual environment. It is safe to create the virtual environment folder at the root directory of this project.

With the virtual environment active, run the following commands:
> `pip3 install wheel`

> `pip3 install setuptools`

> `pip3 install twine`

While in the root directory of this project, build the library:
> `python3 setup.py sdist bdist_wheel`

Then install the built library with
> `pip3 install path/to/BuildDistributionFile.whl`

By default, the build distribution file is located within `dist/`.

## How to Import and Use ExactDelayPathfinder

```python
from exactdelaypathfinder.core import ExactDelayPathfinder

....

EDPF = ExactDelayPathfinder()
result = EDPF.search(G, 10, 'a', 'c')
```

## How to Uninstall

While in the virtual environment, enter
> `pip3 uninstall path/to/BuildDistributionFile.whl`

By default, the build distribution file is located within `dist/`.
