# generate_hash: 33def8532138484f550b63b693f37b83
"""
This file was automatically generated in 2024-08-06 22:49:59.077794
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.course_crud import *


class CourseRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "course"
        self.snake_plural_name = "courses"
        self.camel_name = "Course"
        super().__init__(config)

    def _get_one(self):
        return get_one

    def _get_all(self):
        return get_all

    def _get_link_all(self):
        return get_link_all

    def _create_one(self):
        return create_one

    def _update_one(self):
        return update_one

    def _delete_one(self):
        return delete_one
