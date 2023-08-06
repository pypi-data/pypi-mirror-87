from .. import backend
from collections import namedtuple
from collections.abc import Iterator


class _HandleWrapper:
    """A handle wrapper. Keeps a handle to a backend object and cleans up
       on deletion.
    """

    def __init__(self, handle, **kwargs):
        self._handle = handle
        super().__init__()

    @property
    def handle(self):
        return self._handle

    def __del__(self):
        if backend.jheaps_is_initialized():
            backend.jheaps_handles_destroy(self._handle)

    def __repr__(self):
        return "_HandleWrapper(%r)" % self._handle

