from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader

app = FastAPI()

open_id_schema = APIKeyHeader(name='X-WX-OPENID', description='openID')


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(open_id_schema)]):
    return {"token": token}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
