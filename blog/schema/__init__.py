import graphene
from datetime import datetime
from ..model import *


class UserSchema(graphene.ObjectType):
    """
        User schema
    """
    id = graphene.Int()
    firstname = graphene.String()
    lastname = graphene.String()
    username = graphene.String()
    created_at = graphene.String()
    posts = graphene.Field(
        graphene.List(lambda: PostSchema)
    )
    comments = graphene.Field(
        graphene.List(lambda: CommentSchema)
    )

    def resolve_posts(self, args, context, info):
        return Post.select().where(Post.user == self)

    def resolve_comments(self, args, context, info):
        return Comment.select().where(Comment.user == self)


class PostSchema(graphene.ObjectType):
    """
        Post schema
    """
    id = graphene.Int()
    user = graphene.Field(lambda: UserSchema)
    title = graphene.String()
    body = graphene.String()
    created_at = graphene.String()
    comments = graphene.Field(
        graphene.List(lambda: CommentSchema)
    )

    def resolve_comments(self, args, context, info):
        return Comment.select().where(Comment.post == self)


class CommentSchema(graphene.ObjectType):
    """
        Comment Schema
    """
    id = graphene.Int()
    user = graphene.Field(UserSchema)
    post = graphene.Field(PostSchema)
    body = graphene.String()
    created_at = graphene.String()


class Query(graphene.ObjectType):
    """
        This is a root query object
    """
    users = graphene.Field(
        type = graphene.List(UserSchema),
        args = {
            'id': graphene.Int(),
            'username': graphene.String(),
        }
    )

    posts = graphene.Field(
        graphene.List(PostSchema),
    )

    comments = graphene.Field(
        graphene.List(CommentSchema)
    )

    def resolve_users(self, args, context, info):
        # Collect args
        id = User.id == args.get('id') if 'id' in args else None
        username = User.username == args.get('username') if 'username' in args else None
        argList = [item for item in [id, username] if item is not None]

        if argList:
            return User.select().where(*argList)

        return User.select()

    def resolve_posts(self, args, context, info):
        return Post.select()

    def resolve_comments(self, args, context, info):
        return Comment.select()


class CreateUser(graphene.Mutation):
    """
        Create user mutation
    """
    class Input:
        firstname = graphene.String()
        lastname = graphene.String()
        username = graphene.String(required=True)

    user = graphene.Field(lambda: UserSchema)

    def mutate(self, args, context, info):
        user = User.create(
            firstname = args.get('firstname'),
            lastname = args.get('lastname'),
            username = args.get('username'),
            created_at = datetime.now(),
        )
        user.save()
        return CreateUser(user = user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
