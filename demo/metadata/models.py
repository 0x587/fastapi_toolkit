import datetime
from typing import List

from fastapi_toolkit.define import Schema


class User(Schema):
    name: str
    sex: bool
    title: str
    desc: str
    hot_level: int
    start_level: int
    avatar: str

    info_blocks: List['InfoBlock']
    certified_info_blocks: List['InfoBlock']


class InfoBlock(Schema):
    user: User
    type: str
    title: str
    sub_title: str
    desc: str
    # tags: List[str]
    time_start: datetime.date
    time_end: datetime.date

    certified_users: List['User']

# class CertifiedRecord(Schema):
#     user: User
#     info_block: InfoBlock
