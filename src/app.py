import os

os.environ.setdefault("FASTAPI_SETTINGS_MODULE", "fast_store_backend.settings")  # 请勿在此配置前面加 import

from tortoise.contrib.fastapi import register_tortoise
from fast_tmp.site import register_model_site

from fast_tmp.conf import settings
from fast_tmp.factory import create_app
from fast_store_backend.router import default_router

app = create_app()
app.title = "fast_store_backend"
app.include_router(default_router, prefix="/api")


from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



register_tortoise(app, config=settings.TORTOISE_ORM, generate_schemas=True)
if settings.DEBUG:
    from starlette.staticfiles import StaticFiles

    app.mount("/static", StaticFiles(directory="static"), name="static")  # 注册admin页面需要的静态文件，

if __name__ == "__main__":
    import uvicorn  # type:ignore

    uvicorn.run(app, debug=True, port=8000, lifespan="on")
