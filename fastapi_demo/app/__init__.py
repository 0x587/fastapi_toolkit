from collections import defaultdict
from typing import List

from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_toolkit import computed_field
from sqlalchemy.orm import Session

from inner_code.db import get_db, get_db_sync
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

import inner_code.repo.user_repo as user_repo
import inner_code.repo.info_block_repo as info_block_repo
import inner_code.repo.certified_record_repo as certified_record_repo
from inner_code.models import *
from inner_code.schemas import *


class ProfileView(SchemaUser):
    class Block(SchemaInfoBlock):
        cer_users: List[str]

    class InfoGroup(BaseModel):
        title: str
        items: List['ProfileView.Block']

    @computed_field(db_func=get_db_sync)
    def is_vip(self, db: Session) -> bool:
        return False

    @computed_field(db_func=get_db_sync)
    def infos(self, db: Session) -> List[InfoGroup]:
        idict = defaultdict(list)
        for i in db.scalars(info_block_repo.get_user_is_query(self)).all():
            idict[i.type].append(ProfileView.Block(
                **SchemaInfoBlock.model_validate(i).model_dump(exclude={'certified_records', 'user'}),
                cer_users=[db.scalars(user_repo.get_certified_records_id_is_query(r.id)).first().avatar for r in
                           i.certified_records]
            ))
        return [ProfileView.InfoGroup(title=k, items=v) for k, v in idict.items()]

    @computed_field(db_func=get_db_sync)
    def relationships(self, db: Session) -> List[str]:
        inner_users = db.scalars(select(DBUser).filter(DBUser.id < 0)).all()
        return [u.avatar for u in inner_users]


@app.get('/profile')
async def get_profile(user=Depends(auth.require_user())) -> ProfileView:
    return ProfileView.model_validate(user)
    # # 五个假号
    # inner_users = (await db.scalars(select(DBUser).filter(DBUser.id < 0))).all()
    # idict = defaultdict(list)
    # for i in await info_block_crud.get_user_is(user, db):
    #     idict[i.type].append(ProfileView.Block(
    #         **SchemaInfoBlock.model_validate(i).model_dump(exclude={'certified_records', 'user'}),
    #         cer_users=[(await user_crud.get_certified_records_id_is(r.id, db))[0].avatar for r in i.certified_records]
    #     ))
    # return ProfileView(
    #     **user.model_dump(),
    #     is_vip=False,
    #     relationships=[u.avatar for u in inner_users],
    #     infos=[ProfileView.InfoGroup(title=k, items=v) for k, v in idict.items()]
    # )


add_pagination(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0')
