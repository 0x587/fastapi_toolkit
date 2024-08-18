from fastapi_toolkit.generate import CodeGenerator
from fastapi_toolkit.apis_generate import ApiGenerator

import apis

generator = CodeGenerator('inner_code')
api_g = ApiGenerator(generator)