import asyncio
import time
from collections import defaultdict
from typing_extensions import Doc
from typing import TypeVar, Callable, Coroutine, Any, Annotated, Union, Generator

from fastapi import FastAPI
from fastapi_pagination import add_pagination, Page, paginate, pagination_ctx, Params
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_toolkit import computed_field

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

T = TypeVar("T")


def Depends(  # noqa: N802
        dependency: Annotated[
            Optional[
                Union[Callable[..., Coroutine[Any, Any, T]], Callable[..., T]]
            ],
            Doc(
                """
                A "dependable" callable (like a function).
    
                Don't call it directly, FastAPI will call it for you, just pass the object
                directly.
                """
            ),
        ] = None,
        *,
        use_cache: Annotated[
            bool,
            Doc(
                """
                By default, after a dependency is called the first time in a request, if
                the dependency is declared again for the rest of the request (for example
                if the dependency is needed by several dependencies), the value will be
                re-used for the rest of the request.
    
                Set `use_cache` to `False` to disable this behavior and ensure the
                dependency is called again (if declared more than once) in the same request.
                """
            ),
        ] = True,
) -> T:
    from fastapi import Depends
    return Depends(dependency, use_cache=use_cache)


class ItemView(SchemaItem):
    @computed_field(db_func=get_db_sync)
    def ranges(self, db: Session) -> List[SchemaRange]:
        return [
            SchemaRange.model_validate(r) for r in db.scalars(
                select(DBRange).filter(DBRange.min_value < self.value).filter(DBRange.max_value > self.value)
            )
        ]


class RangeView(SchemaRange):
    @computed_field(db_func=get_db_sync)
    def items(self, db: Session) -> List[ItemView]:
        return [ItemView(**i.__dict__) for i in db.scalars(
            select(DBItem).filter(DBItem.value > self.min_value).filter(DBItem.value < self.max_value)
        )]


import inner_code.crud.range_crud as range_crud
import inner_code.crud.item_crud as item_crud


@app.get('/ss')
async def fr(r=Depends(range_crud.get_one), i=Depends(item_crud.get_one)) -> RangeView:
    print(r.id)
    print(i.id)
    return RangeView(**r.__dict__)


@app.get('/r')
async def fr(r=Depends(range_crud.get_one)) -> RangeView:
    return RangeView(**r.__dict__)


@app.post('/rs', response_model=Page[RangeView])
async def frs(rs=Depends(range_crud.get_all)):
    rs.items = [RangeView(**r.__dict__) for r in rs.items]
    return rs


@app.post('/i', response_model=ItemView)
def fs(i=Depends(item_crud.get_one)):
    return i


add_pagination(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0')
