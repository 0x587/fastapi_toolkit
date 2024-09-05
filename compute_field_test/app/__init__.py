from typing import List

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_toolkit import Depends, computed_field
from fastapi_toolkit.base.endpoint import Endpoint

from inner_code.db import get_db, get_db_sync
from inner_code.routers import InnerRouter
from inner_code.config import Config
from inner_code.setting import get_settings
from inner_code.schemas import *
from inner_code.models import *
from inner_code.crud import repo_map

setting = get_settings()
inner_config = Config()

app = FastAPI()
# app.include_router(InnerRouter(inner_config))
endpoints = Endpoint(repo_map)


@endpoints.get_one(app, '/get_a_item_view')
@endpoints.get_many(app, '/get_many_item_view')
class ItemView(SchemaItem):
    @computed_field(db_func=get_db_sync)
    def ranges(self, db: Session) -> List[SchemaRange]:
        return [
            SchemaRange.model_validate(r) for r in db.scalars(
                select(DBRange).filter(DBRange.min_value < self.value).filter(DBRange.max_value > self.value)
            )
        ]


@endpoints.get_one(app, '/get_a_range_view')
@endpoints.get_many(app, '/get_many_range_view')
class RangeView(SchemaRange):
    @computed_field(db_func=get_db_sync)
    def items(self, db: Session) -> List[ItemView]:
        return [ItemView(**i.__dict__) for i in db.scalars(
            select(DBItem).filter(DBItem.value > self.min_value).filter(DBItem.value < self.max_value)
        )]


@endpoints.get_one(app, '/get_a_item_and_range_view')
class RangeAndItemView(BaseModel):
    pass


add_pagination(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0')
