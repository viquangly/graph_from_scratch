
from typing import Collection, Tuple, Hashable, Union

Numeric = Union[float, int]
NodeCollection = Collection[Hashable]
Edge = Union[Tuple[Hashable, Hashable], Tuple[Hashable, Hashable, Numeric]]
EdgeCollection = Collection[Edge]
