# generate_hash: 4b4156fd7b43580231fcfeb954d0d052
"""
This file was automatically generated in 2024-08-06 22:49:59.066984
"""
import uuid
import datetime
from typing import List, Optional

from fastapi_toolkit.define import Schema
from pydantic import Field, UUID4
from .custom_types import  (
    StudentMode
)


class SchemaBaseDepartment(Schema):
    """pk"""
    id: UUID4 = Field(default_factory=uuid.uuid4)

    """fields"""
    name: str = Field(nullable=False)


class SchemaDepartment(SchemaBaseDepartment):
    """relationships"""


class SchemaBaseStudent(Schema):
    """pk"""
    id: UUID4 = Field(default_factory=uuid.uuid4)

    """fields"""
    name: str = Field(nullable=False)

    mode: StudentMode = Field(nullable=False)


class SchemaStudent(SchemaBaseStudent):
    """relationships"""
    grades: List["SchemaBaseGrade"]


class SchemaBaseCourse(Schema):
    """pk"""
    id: UUID4 = Field(default_factory=uuid.uuid4)

    """fields"""
    name: str = Field(nullable=False)


class SchemaCourse(SchemaBaseCourse):
    """relationships"""
    grades: List["SchemaBaseGrade"]
    teachers: List["SchemaBaseTeacher"]


class SchemaBaseTeacher(Schema):
    """pk"""
    id: UUID4 = Field(default_factory=uuid.uuid4)

    """fields"""

class SchemaTeacher(SchemaBaseTeacher):
    """relationships"""
    course: "SchemaBaseCourse"


class SchemaBaseGrade(Schema):
    """pk"""
    id: UUID4 = Field(default_factory=uuid.uuid4)

    """fields"""
    grade: float = Field(nullable=False)


class SchemaGrade(SchemaBaseGrade):
    """relationships"""
    student: "SchemaBaseStudent"
    course: "SchemaBaseCourse"



SchemaBaseDepartment.model_rebuild()
SchemaDepartment.model_rebuild()
SchemaBaseStudent.model_rebuild()
SchemaStudent.model_rebuild()
SchemaBaseCourse.model_rebuild()
SchemaCourse.model_rebuild()
SchemaBaseTeacher.model_rebuild()
SchemaTeacher.model_rebuild()
SchemaBaseGrade.model_rebuild()
SchemaGrade.model_rebuild()
