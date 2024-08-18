from fastapi import FastAPI, Security, Depends
from fastapi_pagination import add_pagination, pagination_ctx
from sqlalchemy import select

from inner_code.routers import InnerRouter
from inner_code.config import Config
from inner_code.auth import AuthFactory
from inner_code.auth.routes import AuthRouter
# from fastapi_toolkit.define.guard import Guard

from inner_code.setting import get_settings

setting = get_settings()

app = FastAPI()

inner_config = Config()
auth = AuthFactory.create(key_name="X-WX-OPENID")
auth_router = AuthRouter(auth)
# guard = Guard(auth)

# inner_config.department.add_guard(Security(auth.require_user()))
app.include_router(auth_router)
app.include_router(InnerRouter(inner_config))

from typing import List

from fastapi import Depends
from pydantic import BaseModel, TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from inner_code.db import get_db
from inner_code.models import *
from inner_code.schemas import *


class HomePageView(BaseModel):
    user: 'SchemaBaseUser'
    recent_posts: List['SchemaBasePost']  # newest 1
    hot_posts: List['SchemaBasePost']  # most like 1
    my_posts: List['SchemaBasePost']
    like_posts: List['SchemaBasePost']


import inner_code.crud.user_crud as u
import inner_code.crud.post_crud as p
import inner_code.crud.post_like_crud as pl
from sqlalchemy import func

import asyncio
from cachetools import cached


@cached(cache={})
def _f_get_adapter():
    print(123)
    return (TypeAdapter(List[SchemaBasePost]), TypeAdapter(List[SchemaBasePost]),
            TypeAdapter(List[SchemaBasePost]), TypeAdapter(List[SchemaBasePost]))


@app.get('/shawn')
async def f(ident: int, db=Depends(get_db)) -> HomePageView:
    db: AsyncSession
    user = await u.get_one(ident, db)
    likes = await pl.get_user_is(user, db)
    my_post_query = p.get_author_is_query(user)
    like_post_query = p.get_likes_has_query(likes)
    recent_post_query = p.get_author_is_query(user)
    recent_post_query = recent_post_query.order_by(DBPost.created_at.desc())
    hot_post_query = select(DBPost).outerjoin(DBPost.likes).group_by(DBPost).order_by(func.count(DBPost.likes).desc())

    my_post, like_post, recent_post, hot_posts = await asyncio.gather(
        db.scalars(my_post_query),
        db.scalars(like_post_query),
        db.scalars(recent_post_query),
        db.scalars(hot_post_query),
    )

    my_post_adapter, like_post_adapter, recent_post_adapter, hot_posts_adapter = _f_get_adapter()
    return HomePageView(
        user=user,
        my_posts=my_post_adapter.validate_python(my_post.all()),
        like_posts=like_post_adapter.validate_python(like_post.all()),
        recent_posts=recent_post_adapter.validate_python(recent_post.all()),
        hot_posts=hot_posts_adapter.validate_python(hot_posts.all())
    )


add_pagination(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
