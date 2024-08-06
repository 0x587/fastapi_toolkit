from fastapi_toolkit.define import Schema
from typing import List

from enum import Enum


class User(Schema):
    sex: bool


class StudentMode(Enum):
    online = 1
    offline = 2


class Department(Schema):
    name: str


class Student(Schema):
    name: str
    grades: List['Grade']
    mode: StudentMode


class Course(Schema):
    name: str
    grades: List['Grade']
    teacher: List['Teacher']


class Teacher(Schema):
    courses: Course


class Grade(Schema):
    student: Student
    course: Course
    grade: float
