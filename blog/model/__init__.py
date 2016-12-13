from peewee import *
from faker import Faker
from datetime import datetime
from random import randint

fake = Faker()
db = SqliteDatabase('blog.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    firstname = CharField(null = True)
    lastname = CharField(null = True)
    username = CharField(unique = True)
    created_at = DateTimeField()


class Post(BaseModel):
    user = ForeignKeyField(User)
    title = CharField()
    body = CharField()
    created_at = DateTimeField()


class Comment(BaseModel):
    user = ForeignKeyField(User)
    post = ForeignKeyField(Post)
    body = CharField()
    created_at = DateTimeField()


tables = [User, Post, Comment]


def get_any(list):
    index = randint(0, len(list) - 1)
    return list[index]


def populate_database():
    users = []

    db.connect()
    db.drop_tables(tables, safe = True)
    db.create_tables(tables)

    with db.atomic():
        for _ in range(0, 10):
            user = User.create(
                firstname = fake.first_name(),
                lastname = fake.last_name(),
                username = fake.user_name(),
                created_at = datetime.now()
            )
            user.save()
            users.append(user)
            print(user.username)

        for user in users:
            for _ in range(0, randint(0, 12)):
                post = Post.create(
                    user = user,
                    title = fake.sentence(nb_words=3),
                    body = fake.text(),
                    created_at = datetime.now()
                )
                post.save()
                print(post.title)

                for _ in range(0, randint(0, 5)):
                    comment = Comment.create(
                        user = get_any(users),
                        post = post,
                        body = fake.text(max_nb_chars=35),
                        created_at = datetime.now()
                    )
                    comment.save()
                    print(comment.body)
