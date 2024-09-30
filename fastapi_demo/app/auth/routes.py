from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_toolkit.base.auth.key import Auth

from ..schemas import SchemaBaseUser


class AuthRouter(APIRouter):
    def __init__(self, auth: Auth, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth = auth

        self.add_api_route(
            '/me',
            self._get_me(),
            methods=['GET'])

    def _get_me(self):
        async def get_me(current_user=Depends(self.auth.require_user())) -> SchemaBaseUser:
            return current_user

        return get_me
