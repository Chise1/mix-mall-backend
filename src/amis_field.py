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


class MoneyControl(BaseAdminControl):
    """
    存数据库的时候使用分，
    前台显示使用元
    """
    _control_type = "input-number"

    def amis_2_orm(self, value: float) -> int:
        if value:
            return int(value * 100)

    def orm_2_amis(self, value: int) -> float:
        if value:
            return value / 100

    def get_formitem(self, request: Request) -> FormItem:
        if not self._control:
            self._control = NumberItem(type=self._control_type, name=self.name, label=self.label,precision=2)
            if not self._field.null:  # type: ignore
                self._control.required = True
            if self._field.default is not None:  # type: ignore
                self._control.value = self.orm_2_amis(self._field.default)  # type: ignore
        return self._control