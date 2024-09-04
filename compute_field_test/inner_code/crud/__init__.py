# generate_hash: 4e090a981e34b93c90eede91e6a9d9fb
"""
This file was automatically generated in 2024-09-04 15:47:01.946020
"""
import inner_code.crud.user_crud as user_crud
import inner_code.crud.item_crud as item_crud
import inner_code.crud.range_crud as range_crud
from ..schemas import SchemaBaseUser, SchemaBaseItem, SchemaBaseRange

repo_map = {
    SchemaBaseUser: user_crud,
    SchemaBaseItem: item_crud,
    SchemaBaseRange: range_crud,
}