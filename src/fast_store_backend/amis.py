from fast_tmp.amis.column import Column
from fast_tmp.site.field import StrControl
from starlette.requests import Request


class HttpImage(StrControl):
    def get_column(self, request: Request) -> Column:
        if not self._column:
            self._column = Column(name=self.name, label=self.label)
            self._column.type = "image"
        return self._column
