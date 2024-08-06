# generate_hash: 42579122cb4c186cff564c67c783a86e
"""
This file was automatically generated in 2024-08-06 22:49:59.079446
"""
from fastapi import APIRouter

from .department_router import DepartmentRouter
from .student_router import StudentRouter
from .course_router import CourseRouter
from .teacher_router import TeacherRouter
from .grade_router import GradeRouter


class InnerRouter(APIRouter):
    def __init__(self, config):
        super().__init__()
        if not config:
            return
        if config.department:
            self.include_router(DepartmentRouter(config.department))
        if config.student:
            self.include_router(StudentRouter(config.student))
        if config.course:
            self.include_router(CourseRouter(config.course))
        if config.teacher:
            self.include_router(TeacherRouter(config.teacher))
        if config.grade:
            self.include_router(GradeRouter(config.grade))


__all__ = [
    'InnerRouter',
]
