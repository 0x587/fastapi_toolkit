from pydantic import BaseModel, Field


class Schema(BaseModel):
    class Config:
        from_attributes = True
