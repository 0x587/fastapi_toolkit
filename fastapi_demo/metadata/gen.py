import models

from fastapi_toolkit.generate import CodeGenerator

generator = CodeGenerator('inner_code')
generator.force_rewrite = True
generator.generate(True, True, False, 'key')
