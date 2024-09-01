from collections import defaultdict

from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inner_code.db import get_db
from inner_code.routers import InnerRouter
from inner_code.config import Config
from inner_code.setting import get_settings
from inner_code.auth import AuthFactory
from inner_code.auth.routes import AuthRouter

setting = get_settings()
inner_config = Config()

app = FastAPI()
auth = AuthFactory.create(key_name="X-WX-OPENID")
auth_router = AuthRouter(auth)

app.include_router(auth_router)
app.include_router(InnerRouter(inner_config))

import inner_code.crud.user_crud as user_crud
import inner_code.crud.info_block_crud as info_block_crud
import inner_code.crud.certified_record_crud as certified_record_crud
from inner_code.models import *
from inner_code.schemas import *


class ProfileView(SchemaUser):
    class Block(SchemaInfoBlock):
        cer_users: List[str]

    class InfoGroup(BaseModel):
        title: str
        items: List['ProfileView.Block']

    relationships: List[str] = Field(default_factory=list)
    is_vip: bool
    infos: List['InfoGroup']


@app.get('/profile')
async def get_profile(user=Depends(auth.require_user()), db: AsyncSession = Depends(get_db)) -> ProfileView:
    # 五个假号
    inner_users = (await db.scalars(select(DBUser).filter(DBUser.id < 0))).all()
    idict = defaultdict(list)
    for i in await info_block_crud.get_user_is(user, db):
        idict[i.type].append(ProfileView.Block(
            **SchemaInfoBlock.model_validate(i).model_dump(exclude={'certified_records', 'user'}),
            cer_users=[(await user_crud.get_certified_records_id_is(r.id, db))[0].avatar for r in i.certified_records]
        ))
    return ProfileView(
        **user.model_dump(),
        is_vip=False,
        relationships=[u.avatar for u in inner_users],
        infos=[ProfileView.InfoGroup(title=k, items=v) for k, v in idict.items()]
    )


add_pagination(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0')
