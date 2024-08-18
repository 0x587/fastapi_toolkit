from typing import List

from fastapi_toolkit.define import Controller
from metadata.models import *
from pydantic import BaseModel


class HomePageView(BaseModel):
    user: 'User'
    recent_posts: List['Post']  # newest 1
    hot_posts: List['Post']  # most like 1
    my_posts: List['Post']
    like_posts: List['Post']


class UserController(Controller):
    def get_homepage(self, user: 'User') -> HomePageView:
        pass
