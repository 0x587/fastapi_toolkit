# generate_hash: 3fdef314dd82bc3c4c0fb979c3bb8fc0
"""
This file was automatically generated in 2024-10-10 15:04:55.307388
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..repo.certified_record_repo import *


class CertifiedRecordRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "certified_record"
        self.snake_plural_name = "certified_records"
        self.camel_name = "CertifiedRecord"
        super().__init__(config, SchemaBaseCertifiedRecord, SchemaCertifiedRecord)

    def _get_one(self):
        return get_one

    def _batch_get(self):
        return batch_get

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
