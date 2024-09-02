import asyncio
import time
from collections import defaultdict
from typing_extensions import Doc
from typing import TypeVar, Callable, Coroutine, Any, Annotated, Union

from fastapi import FastAPI
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


def f1() -> int:
    return 1


async def f2() -> int:
    return 1


v1 = Depends(f1)
v2 = Depends(f2)


class RangeView(RangeSession):
    @computed_field
    def items(self, db: Session) -> List[SchemaItem]:
        return [SchemaItem.model_validate(i) for i in db.scalars(
            select(DBItem).filter(DBItem.value > self.min_value).filter(DBItem.value < self.max_value)
        )]


import inner_code.crud.range_crud as range_crud


@app.get('/f')
async def f(r=Depends(range_crud.get_one), db: Session = Depends(get_db_sync)) -> RangeView:
    return RangeView(**r.__dict__, db=db)


def aaa() -> int:
    return 123


@app.post('/fs')
async def fs(rs=Depends(range_crud.get_all), db: Session = Depends(get_db_sync)) -> Page[RangeView]:
    rs.items = [RangeView(**r.__dict__, db=db) for r in rs.items]
    return TypeAdapter(Page[RangeView]).validate_python(rs)


add_pagination(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0')
