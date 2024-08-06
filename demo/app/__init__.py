from fastapi import FastAPI, Security
from fastapi_pagination import add_pagination
from ..inner_code.routers import InnerRouter
from ..inner_code.config import Config
from ..inner_code.auth import AuthFactory
from ..inner_code.auth.routes import AuthRouter
# from fastapi_toolkit.define.guard import Guard

from ..inner_code.setting import get_settings

setting = get_settings()
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

app = FastAPI()

inner_config = Config()
auth = AuthFactory.create(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
auth_router = AuthRouter(auth)
# guard = Guard(auth)

inner_config.department.add_guard(Security(auth.require_user(), scopes=['admin']))
app.include_router(auth_router)
app.include_router(InnerRouter(inner_config))

add_pagination(app)

import httpx
from fastapi import HTTPException
import asyncio

sem = asyncio.Semaphore(5)


@app.get("/forward")
async def forward():
    async with sem:
        async with httpx.AsyncClient() as client:
            res = await client.get('http://127.0.0.1:9000/')
            if res.status_code == 200:
                return res.text
            raise HTTPException(status_code=555, detail=res.text)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
