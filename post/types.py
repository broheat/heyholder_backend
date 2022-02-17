from graphene_django import DjangoObjectType
from .models import Participant, Post, Comment

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class ParticipantType(DjangoObjectType):
    class Meta:
        model = Participant