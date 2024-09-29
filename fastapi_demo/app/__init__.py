from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.router import InnerRouter
from app.config import Config
from app.setting import get_settings

setting = get_settings()
inner_config = Config()

app = FastAPI()
app.include_router(InnerRouter(inner_config))

add_pagination(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0')
