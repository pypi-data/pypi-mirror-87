from cachetools import LRUCache
from collections.abc import Mapping
import uproot4
import numpy
from coffea.nanoevents import transforms
from coffea.nanoevents.util import key_to_tuple, tuple_to_key


class TrivialOpener:
    def __init__(self, uuid_pfnmap, uproot_options={}):
        self._uuid_pfnmap = uuid_pfnmap
        self._uproot_options = uproot_options

    def open_uuid(self, uuid):
        pfn = self._uuid_pfnmap[uuid]
        rootdir = uproot4.open(pfn, **self._uproot_options)
        if str(rootdir.file.uuid) != uuid:
            raise RuntimeError(
                f"UUID of file {pfn} does not match expected value ({uuid})"
            )
        return rootdir


class UprootSourceMapping(Mapping):
    _debug = False

    def __init__(self, fileopener, cache=None, access_log=None):
        self._fileopener = fileopener
        self._cache = cache
        self._access_log = access_log
        self.setup()

    def setup(self):
        if self._cache is None:
            self._cache = LRUCache(1)

    def __getstate__(self):
        return {
            "fileopener": self._fileopener,
        }

    def __setstate__(self, state):
        self._fileopener = state["fileopener"]
        self._cache = None
        self.setup()

    def _tree(self, uuid, treepath):
        key = "UprootSourceMapping:" + tuple_to_key((uuid, treepath))
        try:
            return self._cache[key]
        except KeyError:
            pass
        tree = self._fileopener.open_uuid(uuid)[treepath]
        self._cache[key] = tree
        return tree

    def preload_tree(self, uuid, treepath, tree):
        """To save a double-open when using NanoEventsFactory.from_file"""
        key = "UprootSourceMapping:" + tuple_to_key((uuid, treepath))
        self._cache[key] = tree

    @classmethod
    def interpret_key(cls, key):
        uuid, treepath, entryrange, form_key, *layoutattr = key_to_tuple(key)
        start, stop = (int(x) for x in entryrange.split("-"))
        nodes = form_key.split(",")
        if len(layoutattr) == 1:
            nodes.append("!" + layoutattr[0])
        elif len(layoutattr) > 1:
            raise RuntimeError(f"Malformed key: {key}")
        return uuid, treepath, start, stop, nodes

    def __getitem__(self, key):
        uuid, treepath, start, stop, nodes = UprootSourceMapping.interpret_key(key)
        if UprootSourceMapping._debug:
            print("Gettting:", uuid, treepath, start, stop, nodes)
        stack = []
        skip = False
        for node in nodes:
            if skip:
                skip = False
                continue
            elif node == "!skip":
                skip = True
                continue
            elif node == "!load":
                branch = stack.pop()
                if self._access_log is not None:
                    self._access_log.append(branch)
                branch = self._tree(uuid, treepath)[branch]
                # make sure uproot is single-core since our calling context might not be
                stack.append(
                    branch.array(
                        entry_start=start,
                        entry_stop=stop,
                        decompression_executor=uproot4.source.futures.TrivialExecutor(),
                        interpretation_executor=uproot4.source.futures.TrivialExecutor(),
                    )
                )
            elif node.startswith("!"):
                tname = node[1:]
                if not hasattr(transforms, tname):
                    raise RuntimeError(
                        f"Syntax error in form_key: no transform named {tname}"
                    )
                getattr(transforms, tname)(stack)
            else:
                stack.append(node)
        if len(stack) != 1:
            raise RuntimeError(f"Syntax error in form key {nodes}")
        out = stack.pop()
        try:
            out = numpy.array(out)
        except ValueError:
            if UprootSourceMapping._debug:
                print(out)
            raise RuntimeError(
                f"Left with non-bare array after evaluating form key {nodes}"
            )
        return out

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError


class CachedMapping(Mapping):
    """A cache-wrapped mapping

    Reads will call into ``cache`` first, and if no key exists,
    the read will fall back to ``base``, saving the reult into ``cache``.
    """

    def __init__(self, cache, base):
        self.cache = cache
        self.base = base
        self.stats = {"hit": 0, "miss": 0}

    def __getitem__(self, key):
        try:
            value = self.cache[key]
            self.stats["hit"] += 1
            return value
        except KeyError:
            value = self.base[key]
            self.cache[key] = value
            self.stats["miss"] += 1
            return value

    def __iter__(self):
        return iter(self.base)

    def __len__(self):
        return len(self.base)
