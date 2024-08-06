# generate_hash: 027790ea683f01d549170c204c81c3ef
"""
This file was automatically generated in 2024-08-06 22:49:59.077565
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.student_crud import *


class StudentRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "student"
        self.snake_plural_name = "students"
        self.camel_name = "Student"
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
