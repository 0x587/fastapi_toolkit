import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from fastapi_toolkit.define.model import Schema



class User(Schema, table=True):
    id: int = Field(primary_key=True)

    sex: bool = Field(default=True)
    title: str
    name: str
    desc: str
    avatar: Optional[str]
    bg_img: str
    hot_level: int
    star_level: int

    info_blocks: List['InfoBlock'] = Relationship(back_populates='user')
    certified_records: List['CertifiedRecord'] = Relationship(back_populates='user')


class InfoBlock(Schema, table=True):
    id: int = Field(primary_key=True)

    type: str
    title: str
    sub_title: str
    desc: Optional[str]
    tags: str
    show: bool
    time_start: Optional[datetime.date]
    time_end: Optional[datetime.date]

    fk_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates='info_blocks')

    certified_records: List['CertifiedRecord'] = Relationship(back_populates='info_block')


class CertifiedRecord(Schema, table=True):
    id: int = Field(primary_key=True)

    fk_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates='certified_records')

    fk_info_block_id: Optional[int] = Field(default=None, foreign_key="infoblock.id")
    info_block: InfoBlock = Relationship(back_populates='certified_records')

    done: bool
    target_real_name: str
    self_real_name: str
    relation: str
