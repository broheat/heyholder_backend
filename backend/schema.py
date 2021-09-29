import graphene
import users.schema
import stock.schema
import post.schema
import graphql_social_auth
import graphql_jwt
from graphql_jwt.shortcuts import get_token, create_refresh_token


class SocialAuth(graphql_social_auth.SocialAuthMutation):
    token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def resolve(cls, root, info, social, **kwargs):
        if social.user.refresh_tokens.count() >= 1:
            return cls(
                token=get_token(social.user),
                refresh_token=social.user.refresh_tokens.last(),
            )
        else:
            return cls(
                token=get_token(social.user),
                refresh_token=create_refresh_token(social.user),
            )


class Mutation(
    users.schema.Mutation,
    stock.schema.Mutation,
    post.schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    social_auth = SocialAuth.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(
    users.schema.Query, stock.schema.Query, post.schema.Query, graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
