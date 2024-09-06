# generate_hash: a6b114bf9220af3870f04ef037a69a60
"""
This file was automatically generated in 2024-09-06 16:25:17.804483
"""
import inner_code.repo.user_repo as user_repo
import inner_code.repo.item_repo as item_repo
import inner_code.repo.range_repo as range_repo
from ..schemas import SchemaBaseUser, SchemaBaseItem, SchemaBaseRange

repo_map = {
    SchemaBaseUser: user_repo,
    SchemaBaseItem: item_repo,
    SchemaBaseRange: range_repo,
}