# generate_hash: ab50c672c8b5d05b7ed2d0b575cad44a
"""
This file was automatically generated in 2024-08-06 22:49:59.077304
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.department_crud import *


class DepartmentRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "department"
        self.snake_plural_name = "departments"
        self.camel_name = "Department"
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
