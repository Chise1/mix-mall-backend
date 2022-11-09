from fast_tmp.site.base import PageRouter,Page
from fast_tmp.amis.wizard import Wizard,WizardStep
from starlette.requests import Request


class CreateGoodAdmin(PageRouter):
    async def get_app_page(self, request: Request) -> Page:
        return Page(body=Wizard(
            steps=[
                WizardStep(
                    title="商品基本信息",
                    body=[

                    ]
                )
            ]
        ))