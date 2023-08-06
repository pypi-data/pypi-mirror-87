"""All type annotations go here."""


from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

    import wx

    from aio_wx_widgets.controller import BaseController
    from aio_wx_widgets.core.base_widget import BaseWidget, CallableItem
    from aio_wx_widgets.core.binding import Binding

    try:
        import Protocol  # type: ignore
    except ImportError:
        from typing_extensions import Protocol

    assert BaseController
    assert AbstractEventLoop
    assert Binding
    assert wx
    assert BaseWidget

    class Choice(Protocol):
        """Typing protocol to be used for static type checking."""

        label: str
        value: Any

    Widget = Union[BaseWidget, wx.Window, wx.BoxSizer, CallableItem]
