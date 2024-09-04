# generate_hash: 4c8004fc488a4ba6cecd14ee904e95a3
"""
This file was automatically generated in 2024-09-04 15:53:45.045087
"""
import inner_code.crud.user_crud as user_crud
import inner_code.crud.info_block_crud as info_block_crud
import inner_code.crud.certified_record_crud as certified_record_crud
from ..schemas import SchemaBaseUser, SchemaBaseInfoBlock, SchemaBaseCertifiedRecord

repo_map = {
    SchemaBaseUser: user_crud,
    SchemaBaseInfoBlock: info_block_crud,
    SchemaBaseCertifiedRecord: certified_record_crud,
}