from fast_tmp.amis.formitem import FormItem, Column, NumberItem
from fast_tmp.site import BaseAdminControl
from starlette.requests import Request


class Color(FormItem):
    format: str = "hex"


class ColorControl(BaseAdminControl):
    _control_type = "input-color"

    def get_control(self, request: Request) -> FormItem:
        if not self._control:
            control = super().get_formitem(request)
            color = Color(**control.dict())
            color.format = "rgb"
            self._control = color
        return self._control

    def get_column(self, request: Request) -> Column:
        if not self._column:
            self._column = Column(name=self.name, label=self.label)
            self._column.type = "color"
        return self._column