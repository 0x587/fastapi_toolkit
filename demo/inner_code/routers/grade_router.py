# generate_hash: 6e434d79fe085d6a92bb4af4301e4ee1
"""
This file was automatically generated in 2024-08-06 22:49:59.078230
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.grade_crud import *


class GradeRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "grade"
        self.snake_plural_name = "grades"
        self.camel_name = "Grade"
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
