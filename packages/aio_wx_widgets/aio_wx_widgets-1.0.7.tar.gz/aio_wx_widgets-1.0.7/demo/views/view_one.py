from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aio_wx_widgets.containers.grid import VERTICAL, Grid
from aio_wx_widgets.containers.group import Group, Section
from aio_wx_widgets.core.binding import Binding
from aio_wx_widgets.core.data_types import HorAlign, VerAlign
from aio_wx_widgets.core.validators import float_validator, int_validator
from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets.button import AioButton
from aio_wx_widgets.widgets.checkbox import CheckBox
from aio_wx_widgets.widgets.labelled_item import LabelledItem
from aio_wx_widgets.widgets.text import Text
from aio_wx_widgets.widgets.text_entry import Entry

if TYPE_CHECKING:
    from demo.controller.controller_one import ControllerOne

_LOGGER = logging.getLogger(__name__)


class ViewOne(SimplePanel["ControllerOne"]):
    def __init__(self, parent, controller: "ControllerOne"):
        super().__init__(parent, controller, scrollable=False)

    def populate(self):
        """Populate this view."""

        # Use a context manager for container types like a group or grid.
        # A group is a container with a label and a sizer inside. Inside
        # this sizer widgets, or other containers can be placed.
        self.add(Text(binding=self.bind("int_val"), wrap=True), margin=20)
        with self.add(Grid()) as grd:
            grd.add(Text("This is long text", min_width=50))
            grd.add(Text("short", min_width=50))
        self.add(
            LabelledItem(
                "Label text",
                Entry(binding=self.bind("float_val"), validator=float_validator),
            )
        )

        with self.add(Section("Float validators")) as sc:
            sc.add(
                LabelledItem(
                    "Enter a float value",
                    Entry(binding=self.bind("float_val"), validator=float_validator,),
                    item_weight=2,
                )
            )
            with sc.add(Grid()) as grd:
                # the binding binds to an attribute defined in the controller
                # the weight determines how much space a specific item should consume
                # with respect to the other members of the container.

                grd.add(
                    Entry(binding=self.bind("float_val"), validator=float_validator,),
                    weight=4,
                )
                grd.add(
                    Text(binding=self.bind("float_val")),
                    weight=4,
                    ver_align=VerAlign.center,
                )
        with self.add(Section("Int validators")) as sc:
            sc.add(Text("Only integer values are allowed."))
            with sc.add(Grid()) as grd:
                grd.add(
                    Entry(binding=self.bind("int_val"), validator=int_validator,),
                    weight=3,
                    margin=0,
                )
                grd.add(
                    Entry(binding=self.bind("int_val"), validator=int_validator,),
                    weight=1,
                    margin=0,
                )
                grd.add(Text(binding=self.bind("int_val")), weight=1, margin=0)

        with self.add(Grid()) as grd:
            grd.add(Entry(binding=Binding(self._controller, "a_string_value")))
            grd.add(Entry(binding=Binding(self._controller, "a_string_value")))

        with self.add(Grid()) as grd:
            grd.add(AioButton("button one", self._set_value), weight=6)
            grd.add(AioButton("button two,self", self._set_value), weight=6)

        with self.add(Group("Nesting of grids")) as grp:
            with grp.add(Grid()) as grd:
                grd.add(
                    Text(text="Right aligned text"),
                    weight=3,
                    hor_align=HorAlign.right,
                    ver_align=VerAlign.center,
                )
                with grd.add(Grid(VERTICAL), weight=6, margin=0) as vert_grid:
                    vert_grid.add(
                        AioButton("Left aligned button", self._set_value),
                        hor_align=HorAlign.left,
                        margin=4,
                    )
                    vert_grid.add(AioButton("Set number entries.", self._set_value))
                    vert_grid.add(
                        Text(text="Center aligned text with a large margin."),
                        margin=(10, 10, 30, 5),
                        hor_align=HorAlign.center,
                    )
                    vert_grid.add(
                        AioButton(
                            "right aligned button.",
                            self._set_value,
                            enabled=self.bind("a_checkbox_value"),
                        ),
                        weight=2,
                        hor_align=HorAlign.right,
                    )
        self.add(CheckBox("A checkbox", binding=self.bind("a_checkbox_value")))
        self.add(
            CheckBox("The same checkbox value", binding=self.bind("a_checkbox_value"))
        )
        self.add(AioButton("open other window", self._on_open_second_window))
        self.add(AioButton("open third window", self._on_open_third_window))

    async def _on_open_second_window(self, evt):
        await self._controller.open_other_window()

    async def _on_open_third_window(self, evt):
        await self._controller.open_third_window()

    async def _on_open(self, evt):
        await self._controller.open_other_window()

    async def _set_value(self: ViewOne):
        await self._controller.set_value()
