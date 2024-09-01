# generate_hash: 9dab0999900c1e1043fc01cac0892534
"""
This file was automatically generated in 2024-09-01 22:59:21.243496
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_toolkit.base.auth.key import Auth

from ..schemas import SchemaBaseUser


class AuthRouter(APIRouter):
    def __init__(self, auth: Auth, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth = auth

        self.add_api_route(
            '/get_user/{username}',
            self._get_user(),
            methods=['GET'])
        self.add_api_route(
            '/register',
            self._register(),
            methods=['PUT'])
        self.add_api_route(
            '/me',
            self._get_me(),
            methods=['GET'])

    def _get_user(self):

        def get_user(user=Depends(self.auth.backend.get_user)) -> SchemaBaseUser:
            if user:
                return user
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        return get_user

    def _register(self):
        async def register(user: SchemaBaseUser):
            return await self.auth.backend.add_user(user)

        return register

    def _get_me(self):
        async def get_me(current_user=Depends(self.auth.require_user())) -> SchemaBaseUser:
            return current_user

        return get_me
