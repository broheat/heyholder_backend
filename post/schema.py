from numpy import number
from .types import ParticipantType, PostType, CommentType
import graphene
from .models import Post, Comment, Participant
from stock.models import Stock
from graphql_jwt.decorators import login_required
from django.db.models import Sum

class CreatePostMutation(graphene.Mutation):
    class Arguments:
        code = graphene.String()
        title = graphene.String()
        contents = graphene.String()

    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, **kwargs):
        code = kwargs.get("code")
        title = kwargs.get("title")
        contents = kwargs.get("contents")
        user = info.context.user
        amount = Stock.objects.get(user=user, code=code).amount
        post = Post.objects.create(
            user=user, code=code, title=title, contents=contents, amount=amount
        )
        post.save()
        return CreatePostMutation(post=post)

class ParticipatePostMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        number_of_stock = graphene.Int()
    participant = graphene.Field(ParticipantType)    
    
    @login_required
    def mutate(self,info,**kwargs):
        user = info.context.user
        posting_id = kwargs.get("id")
        number_of_stock = kwargs.get("number_of_stock")
        if not Post.objects.filter(id=posting_id).exists():
            raise PermissionError("글이 없다.")

        post = Post.objects.get(id=posting_id)
        
        try:
            participant = Participant.objects.get(user=user, post=post)
            participant.number_of_stock = number_of_stock
            participant.save()
        except Participant.DoesNotExist:
            participant = Participant.objects.create(user= user, post=post, number_of_stock=number_of_stock)
            participant.save()

        print(participant)
        return ParticipatePostMutation(participant=participant)
        
class CreateCommentMutaion(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        contents = graphene.String()

    comment = graphene.Field(CommentType)

    @login_required
    def mutate(self, info, **kwargs):
        posting_id = kwargs.get("id")
        contents = kwargs.get("contents")
        user = info.context.user
        if not Post.objects.filter(id=posting_id).exists():
            raise PermissionError("글이 없다.")

        post = Post.objects.get(id=posting_id)

        try:
            comment = Comment.objects.create(user=user, post=post, contents=contents)
            comment.save()
        except Post.DoesNotExist:
            raise PermissionError("잘못된 접속 방법입니다.")
        return CreateCommentMutaion(comment=comment)

class Create2CommentMutaion(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        contents = graphene.String()
        parentComment = graphene.ID()

    comment = graphene.Field(CommentType)

    @login_required
    def mutate(self, info, **kwargs):
        id = kwargs.get("id")
        parentComment = kwargs.get("parentComment")
        contents = kwargs.get("contents")
        user = info.context.user
        try:
            comment = Comment.objects.create(
                user=user, post=id, contents=contents, parentComment=parentComment
            )
            comment.save()
        except Post.DoesNotExist:
            raise PermissionError("잘못된 접속 방법입니다.")
        return CreateCommentMutaion(comment=comment)

class Query(graphene.ObjectType):
    allpost = graphene.List(PostType, code=graphene.String(required=True))
    getpost = graphene.Field(PostType, id=graphene.ID(required=True))
    allcomment = graphene.List(CommentType, id=graphene.ID(required=True))
    totalParticipant = graphene.Int(id=graphene.ID(required=True))
    participantShare = graphene.Int(id=graphene.ID(required=True))
    
    @login_required
    def resolve_participantShare(self, info, **kwargs):
        id = kwargs.get("id")
        user = info.context.user
        post = Post.objects.get(id=id)
        
        try:
            participant = Participant.objects.get(user=user, post=post)
            participantShare = participant.number_of_stock
            return participantShare
        
        except Participant.DoesNotExist:
            participantShare = 0
            return participantShare
        
    @login_required
    def resolve_totalParticipant(self, info, **kwargs):
        id = kwargs.get("id")
        post = Post.objects.get(id=id)
        totalParticipant = Participant.objects.filter(post = post).aggregate(Sum("number_of_stock"))[
            "number_of_stock__sum"
        ]
        if totalParticipant is not None:
            return totalParticipant
        else:
            return 0
        
    @login_required
    def resolve_allpost(self, info, **kwargs):
        code = kwargs.get("code")
        return Post.objects.filter(code=code)

    @login_required
    def resolve_getpost(self, info, **kwargs):
        id = kwargs.get("id")
        try:
            post = Post.objects.get(id=id)
            return post
        except Post.DoesNotExist:
            return None

    @login_required
    def resolve_allcomment(self, info, **kwagrs):
        posting_id = kwagrs.get("id")
        post = Post.objects.get(id=posting_id)
        comments = Comment.objects.filter(post=post)
        return comments


class Mutation(graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    create_comment = CreateCommentMutaion.Field()
    create_2comment = Create2CommentMutaion.Field()
    participant_propose = ParticipatePostMutation.Field()
