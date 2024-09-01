import datetime
from typing import List
from pydantic import Field, BaseModel
from fastapi_toolkit.define import Schema, Controller


class User(Schema):
    name: str
    posts: List['Post']
    comments: List['Comment']
    post_likes: List['PostLike']
    comment_likes: List['CommentLike']
    pass_card: 'PassCard'
    groups: List['Group']


class PassCard(Schema):
    account: int
    user: 'User'


class Group(Schema):
    name: str
    users: List['User']


class Post(Schema):
    text: str
    author: 'User' = Field(alias='user')
    comments: List['Comment']
    likes: List['PostLike'] = Field(alias='post_likes')


class Comment(Schema):
    content: str
    user: 'User'
    post: 'Post'
    likes: List['CommentLike'] = Field(alias='comment_likes')


class PostLike(Schema):
    post: 'Post'
    user: 'User'


class CommentLike(Schema):
    comment: 'Comment'
    user: 'User'


# class HomePageView:
#     user: 'User'
#     like_posts: List['Post']
#     recent_posts: List['Post']  # newest 10
#     hot_posts: List['Post']  # most like 10

class HomePageView(BaseModel):
    user: 'User'
    level: int
    recent_posts: List['Post']  # newest 1
    hot_posts: List['Post']  # most like 1
    my_posts: List['Post']
    like_posts: List['Post']


class UserController(Controller):
    def get_homepage(self, user: User, comment: Comment, count: int) -> HomePageView:
        pass


class FileController(Controller):
    pass
