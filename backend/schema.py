import graphene
import users.schema, stock.schema, post.schema
import graphql_social_auth
import graphql_jwt

class Mutation(users.schema.Mutation, stock.schema.Mutation, post.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    social_auth = graphql_social_auth.SocialAuthJWT.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class Query(users.schema.Query, stock.schema.Query, post.schema.Query, graphene.ObjectType):
    pass



schema = graphene.Schema(query=Query, mutation=Mutation)