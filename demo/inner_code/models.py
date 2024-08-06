# generate_hash: 7be4dbd0051064ef821e962ba9c454dc
"""
This file was automatically generated in 2024-08-06 22:49:59.063187
"""
import uuid
import datetime
import enum
from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, dialects
from sqlalchemy.sql import sqltypes

from .db import Base
from .custom_types import  (
    StudentMode
)


class DBDepartment(Base):
    __tablename__ = "department"

    id: Mapped[uuid.UUID] = mapped_column(sqltypes.UUID, primary_key=True)

    name: Mapped[str] = mapped_column(sqltypes.String, nullable=False)


class DBStudent(Base):
    __tablename__ = "student"

    id: Mapped[uuid.UUID] = mapped_column(sqltypes.UUID, primary_key=True)

    name: Mapped[str] = mapped_column(sqltypes.String, nullable=False)

    mode: Mapped[StudentMode] = mapped_column(dialects.postgresql.ENUM(StudentMode), nullable=False)

    grades: Mapped[List["DBGrade"]] = relationship(back_populates="student")


class DBCourse(Base):
    __tablename__ = "course"

    id: Mapped[uuid.UUID] = mapped_column(sqltypes.UUID, primary_key=True)

    name: Mapped[str] = mapped_column(sqltypes.String, nullable=False)

    grades: Mapped[List["DBGrade"]] = relationship(back_populates="course")

    teachers: Mapped[List["DBTeacher"]] = relationship(back_populates="course")


class DBTeacher(Base):
    __tablename__ = "teacher"

    id: Mapped[uuid.UUID] = mapped_column(sqltypes.UUID, primary_key=True)

    course: Mapped['DBCourse'] = relationship(back_populates="teachers")
    fk_course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("course.id"), nullable=False)


class DBGrade(Base):
    __tablename__ = "grade"

    id: Mapped[uuid.UUID] = mapped_column(sqltypes.UUID, primary_key=True)

    grade: Mapped[float] = mapped_column(sqltypes.Float, nullable=False)

    student: Mapped['DBStudent'] = relationship(back_populates="grades")
    fk_student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("student.id"), nullable=False)

    course: Mapped['DBCourse'] = relationship(back_populates="grades")
    fk_course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("course.id"), nullable=False)


