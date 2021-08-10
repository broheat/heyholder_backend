from graphene_django import DjangoObjectType
from .models import Post, Comment

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
