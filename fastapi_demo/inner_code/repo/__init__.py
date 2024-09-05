# generate_hash: 1ec500d46275328ce01914182f1708ba
"""
This file was automatically generated in 2024-09-05 10:55:25.315672
"""
import inner_code.repo.user_repo as user_repo
import inner_code.repo.info_block_repo as info_block_repo
import inner_code.repo.certified_record_repo as certified_record_repo
from ..schemas import SchemaBaseUser, SchemaBaseInfoBlock, SchemaBaseCertifiedRecord

repo_map = {
    SchemaBaseUser: user_repo,
    SchemaBaseInfoBlock: info_block_repo,
    SchemaBaseCertifiedRecord: certified_record_repo,
}