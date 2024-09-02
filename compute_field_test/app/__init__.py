import asyncio
import time
from collections import defaultdict

from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination, Page, paginate, pagination_ctx, Params
from pydantic import BaseModel, ConfigDict, TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import Session

from inner_code.db import get_db, get_db_sync
from inner_code.routers import InnerRouter
from inner_code.config import Config
from inner_code.setting import get_settings

setting = get_settings()
inner_config = Config()

app = FastAPI()

app.include_router(InnerRouter(inner_config))

from inner_code.schemas import *
from inner_code.models import *


def computed_field(func, *args, **kw):
    from pydantic import computed_field

    @computed_field(*args, **kw)
    def wrapper(*args, **kw) -> func.__annotations__.get('return'):
        self = args[0]
        return func(*args, **kw, db=self.db)

    return wrapper


# class RangeSession(SchemaRange):
#     model_config = ConfigDict(arbitrary_types_allowed=True)
#     db: Session = Field(exclude=True)


class RangeView(RangeSession):
    @computed_field
    def items(self, db: Session) -> List[SchemaItem]:
        return [SchemaItem.model_validate(i) for i in db.scalars(
            select(DBItem).filter(DBItem.value > self.min_value).filter(DBItem.value < self.max_value)
        )]


import inner_code.crud.range_crud as range_crud


@app.get('/f')
async def f(r=Depends(range_crud.get_one), db: Session = Depends(get_db_sync)):
    return RangeView(**r.__dict__, db=db)


@app.get('/fs')
async def fs(db: Session = Depends(get_db_sync), rs=Depends(range_crud.get_all)) -> Page[int]:
    # a = db.scalars(select(DBRange)).all()
    #
    # return [RangeView(**r.__dict__, db=db) for r in a]
    # return paginate(TypeAdapter(List[RangeView]).validate_python(rs))
    return paginate([1, 2, 3])

add_pagination(app)
# TODO????????????????
@app.get('/asd')
def asd(rs=Depends(range_crud.get_all)) -> Page[int]:
    return paginate(rs, params=Params(page=1, size=50))


add_pagination(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0')
