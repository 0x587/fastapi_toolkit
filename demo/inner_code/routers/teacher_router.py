# generate_hash: 23d9bccd2bf2eff32cac24ab62e53a9e
"""
This file was automatically generated in 2024-08-06 22:49:59.077996
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.teacher_crud import *


class TeacherRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "teacher"
        self.snake_plural_name = "teachers"
        self.camel_name = "Teacher"
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
