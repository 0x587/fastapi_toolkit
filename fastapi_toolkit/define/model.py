from pydantic import BaseModel as PydanticBaseModel, Field


class BaseModel(PydanticBaseModel):
    class Config:
        from_attributes = True
