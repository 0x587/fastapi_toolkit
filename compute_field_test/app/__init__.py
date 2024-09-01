import asyncio
from collections import defaultdict

from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inner_code.db import get_db
from inner_code.routers import InnerRouter
from inner_code.config import Config
from inner_code.setting import get_settings

setting = get_settings()
inner_config = Config()

app = FastAPI()

app.include_router(InnerRouter(inner_config))

add_pagination(app)
from inner_code.schemas import *
from inner_code.models import *
from pydantic import computed_field


class RangeSession(SchemaRange):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: AsyncSession = Field(exclude=True)

    @computed_field
    def items(self) -> List[int]:
        async def f():
            await self.db.scalars(
                select(DBItem).filter(DBItem.value > self.min_value).filter(DBItem.value < self.max_value))
            return [1, 2, 3]

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f())


@app.get('/f')
async def f(db: AsyncSession = Depends(get_db)):
    a = await db.scalars(select(DBRange))
    a = a.one()
    print(a)
    print(SchemaRange.model_validate(a))
    return RangeSession(**SchemaRange.model_validate(a).model_dump(), db=db)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0')
