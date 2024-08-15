from fastapi import FastAPI, Security, Depends
from fastapi_pagination import add_pagination, pagination_ctx
from sqlalchemy import select

from inner_code.routers import InnerRouter
from inner_code.config import Config
# from inner_code.auth import AuthFactory
# from inner_code.auth.routes import AuthRouter
# from fastapi_toolkit.define.guard import Guard

from inner_code.setting import get_settings

setting = get_settings()

app = FastAPI()

inner_config = Config()
# auth = AuthFactory.create(key_name="X-WX-OPENID")
# auth_router = AuthRouter(auth)
# guard = Guard(auth)

# inner_config.department.add_guard(Security(auth.require_user()))
# app.include_router(auth_router)
app.include_router(InnerRouter(inner_config))

from typing import List

from fastapi import Depends
from pydantic import BaseModel, TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from inner_code.db import get_db
from inner_code.models import DBPost, DBPostLike
from inner_code.schemas import *


class HomePageView(BaseModel):
    user: 'SchemaBaseUser'
    my_posts: List['SchemaPost']
    like_posts: List['SchemaPost']
    # recent_posts: List['SchemaBasePost']  # newest 10
    # hot_posts: List['SchemaBasePost']  # most like 10


import inner_code.crud.user_crud as u
import inner_code.crud.post_crud as p
import inner_code.crud.post_like_crud as pl


@app.get('/shawn')
async def f(ident: int, db=Depends(get_db)) -> HomePageView:
    db: AsyncSession
    user = await u.get_one(ident, db)
    likes = await pl.get_all_is_user(user, db)
    return HomePageView(
        user=user,
        my_posts=await p.get_all_is_author(user, db),
        like_posts=await p.get_all_has_likes(likes, db),
    )


add_pagination(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
