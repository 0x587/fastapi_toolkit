import datetime
from typing import List

from fastapi_toolkit.define import Schema


class Student(Schema):
    name: str
    pass_card: 'PassCard'
    group: 'Group'
    courses: List['Course']


class PassCard(Schema):
    account: int
    student: 'Student'


class Group(Schema):
    name: str
    students: List['Student']


class Course(Schema):
    name: str
    students: List['Student']
