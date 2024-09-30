
from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..repo.info_block_repo import *


class InfoBlockRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "info_block"
        self.snake_plural_name = "info_blocks"
        self.camel_name = "InfoBlock"
        super().__init__(config, InfoBlock)

    def _get_one(self):
        return get_one

    def _batch_get(self):
        return batch_get

    def _get_all(self):
        return get_all

    def _create_one(self):
        return create_one

    def _update_one(self):
        return update_one

    def _delete_one(self):
        return delete_one
