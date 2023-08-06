"""Text widgets."""

import logging
from typing import Optional, Union

import wx

from aio_wx_widgets.colors import GREEN
from aio_wx_widgets.const import is_debugging
from aio_wx_widgets.core.base_widget import BaseWidget
from aio_wx_widgets.core.binding import Binding, OneWayBindable

_LOGGER = logging.getLogger(__name__)

__all__ = ["Text"]


def _get_font_info(current_font: wx.Font, font_size: float = 1, bold=False) -> wx.Font:
    font = wx.Font()

    if font_size != 1:
        current_font_size = current_font.GetPointSize()
        new_font_size = int(font_size * current_font_size)
        font.SetPointSize(new_font_size)

    if bold:
        font.MakeBold()

    return font


class Text(BaseWidget):
    """Static text."""

    def __init__(
        self,
        text="",
        font_size: float = 1,
        color: Optional[int] = None,
        enabled: Union[bool, Binding] = True,
        binding: Optional[Binding] = None,
        bold=False,
        wrap=False,
        min_width=-1,
    ):
        """Init.

        Args:
            text:
            font_size:
        """
        value_binding = (
            OneWayBindable(binding, self._set_ui_value) if binding is not None else None
        )

        super().__init__(
            wx.StaticText(),
            min_width=min_width,
            value_binding=value_binding,
            enabled=enabled,
        )
        self._parent = None
        self._color = color
        self._text = text
        self._wrap = wrap

        self._font = _get_font_info(self.ui_item.GetFont(), font_size, bold=bold)

        self._previous_size = None

    def _set_ui_value(self, value):
        self.set_text(value)

    def __call__(self, parent):
        self._parent = parent
        self.ui_item.Create(parent)

        if self._font:
            self.ui_item.SetFont(self._font)

        if self._text:
            self.set_text(self._text, self._color)
        if self._value_binding:
            self.set_text(self._value_binding.get_property_value(), self._color)
        if is_debugging():
            self.ui_item.SetBackgroundColour(GREEN)
        self._init()
        self.ui_item.Bind(wx.EVT_SIZE, self._on_size)

        return self

    def _set_text(self, color=None, client_size=None):
        # _LOGGER.debug("Setting text to: %s", self._text)
        self.ui_item.Unbind(wx.EVT_SIZE)

        self.ui_item.SetLabel(str(self._text))

        if self._wrap:
            if client_size:
                self.ui_item.Wrap(client_size[0])

        if color:
            self.ui_item.SetForegroundColour(color)

        self.ui_item.Bind(wx.EVT_SIZE, self._on_size)

    def _on_size(self, evt):
        size = evt.Size
        if self._previous_size is not None and self._previous_size[0] == size[0]:
            return

        self._previous_size = size
        self._set_text(client_size=size)

        # evt.Skip()

    def set_text(self, text, color=None):
        """Set or change the text."""
        self._text = str(text)
        self._set_text(color)
