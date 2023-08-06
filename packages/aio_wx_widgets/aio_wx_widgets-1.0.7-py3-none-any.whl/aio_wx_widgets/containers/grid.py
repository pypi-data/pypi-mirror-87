"""Grid layout item."""

# pylint: disable=duplicate-code


import logging

import wx

from aio_wx_widgets.core.base_widget import CallableItem
from aio_wx_widgets.core.sizers import SizerMixin

_LOGGER = logging.getLogger(__name__)

__all__ = ["Grid", "VERTICAL", "HORIZONTAL"]

VERTICAL = wx.VERTICAL
HORIZONTAL = wx.HORIZONTAL


class Grid(SizerMixin, CallableItem):
    """A grid component.

    Basically a boxsizer with some defaults.
    """

    default_sizer_margin = 0

    HOR = HORIZONTAL
    VER = VERTICAL

    def __init__(self, orientation=HORIZONTAL):
        """Init."""
        super().__init__()
        self._ui_item = self._sizer_ = wx.BoxSizer(orient=orientation)
        self._parent = None

    @property
    def ui_item(self):
        """Return UI item."""
        return self._ui_item

    @property
    def _sizer(self):
        return self._sizer_

    def __call__(self, parent) -> SizerMixin:
        # setting a specific parent.
        self._parent = parent
        return self

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
