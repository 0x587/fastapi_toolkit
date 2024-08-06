# generate_hash: 74466e35a14018e9b5d2e987bc74d319
"""
This file was automatically generated in 2024-08-06 22:49:59.087072
"""
import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_toolkit.base.auth import Auth

from ..db import get_db
from .models import SchemaUser, SchemaUserCreate, Token


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
            '/token',
            self._get_token(),
            methods=['POST'])
        self.add_api_route(
            '/me',
            self._get_me(),
            methods=['GET'])

    def _get_user(self):

        def get_user(user=Depends(self.auth.backend.get_user)) -> SchemaUser:
            if user:
                return user
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        return get_user

    def _register(self):
        async def register(user: SchemaUserCreate):
            return await self.auth.backend.add_user(user, self.auth.get_password_hash(user.password))

        return register

    def _get_token(self):
        async def get_token(form_data: OAuth2PasswordRequestForm = Depends(),
                            db=Depends(get_db)) -> Token:
            user = await self.auth.authenticate_user(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect username or password",
                )
            user.last_login_at = datetime.datetime.utcnow()
            await db.commit()
            access_token = self.auth.create_access_token(data={"sub": user.username})
            return Token(access_token=access_token, token_type="bearer")
        return get_token

    def _get_me(self):
        async def get_me(current_user=Depends(self.auth.require_user())) -> SchemaUser:
            return current_user

        return get_me
