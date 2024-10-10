import datetime
from typing import List, Optional
from fastapi_toolkit.define import Schema, Field


class User(Schema):
    sex: bool
    title: str
    name: str
    desc: str
    avatar: Optional[str]
    bg_img: str
    hot_level: int
    star_level: int

    info_blocks: List['InfoBlock']
    certified_records: List['CertifiedRecord']


class InfoBlock(Schema):
    type: str
    title: str
    sub_title: str
    desc: str
    tags: str
    show: bool = Field(default=False)
    time_start: datetime.date
    time_end: datetime.date

    user: 'User'
    certified_records: List['CertifiedRecord']


class CertifiedRecord(Schema):
    user: 'User'
    info_block: 'InfoBlock'
    done: bool
    target_real_name: str
    self_real_name: str
    relation: str
