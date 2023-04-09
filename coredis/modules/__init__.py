from __future__ import annotations

from deprecated.sphinx import versionadded

from coredis.commands import CommandMixin
from coredis.typing import AnyStr

from .autocomplete import Autocomplete
from .filters import BloomFilter, CountMinSketch, CuckooFilter, TDigest, TopK
from .json import Json
from .search import Search
from .timeseries import TimeSeries


class ModuleMixin(CommandMixin[AnyStr]):
    @property
    @versionadded(version="4.12.0")
    def json(self) -> Json[AnyStr]:
        """
        Property to access :class:`~coredis.modules.json.Json` commands.
        """
        return Json(self)

    @property
    @versionadded(version="4.12.0")
    def bf(self) -> BloomFilter[AnyStr]:
        """
        Property to access :class:`~coredis.modules.filters.BloomFilter` commands.
        """
        return BloomFilter(self)

    @property
    @versionadded(version="4.12.0")
    def cf(self) -> CuckooFilter[AnyStr]:
        """
        Property to access :class:`~coredis.modules.filters.CuckooFilter` commands.
        """
        return CuckooFilter(self)

    @property
    @versionadded(version="4.12.0")
    def cms(self) -> CountMinSketch[AnyStr]:
        """
        Property to access :class:`~coredis.modules.filters.CountMinSketch` commands.
        """
        return CountMinSketch(self)

    @property
    @versionadded(version="4.12.0")
    def tdigest(self) -> TDigest[AnyStr]:
        """
        Property to access :class:`~coredis.modules.filters.TDigest` commands.
        """
        return TDigest(self)

    @property
    @versionadded(version="4.12.0")
    def topk(self) -> TopK[AnyStr]:
        """
        Property to access :class:`~coredis.modules.filters.TopK` commands.
        """
        return TopK(self)

    @property
    @versionadded(version="4.12.0")
    def timeseries(self) -> TimeSeries[AnyStr]:
        """
        Property to access :class:`~coredis.modules.timeseries.TimeSeries` commands.
        """
        return TimeSeries(self)

    @property
    @versionadded(version="4.12.0")
    def search(self) -> Search[AnyStr]:
        """
        Property to access :class:`~coredis.modules.search.Search` commands.
        """
        return Search(self)

    @property
    @versionadded(version="4.12.0")
    def autocomplete(self) -> Autocomplete[AnyStr]:
        """
        Property to access :class:`~coredis.modules.autocomplete.Autocomplete` commands.
        """
        return Autocomplete(self)
