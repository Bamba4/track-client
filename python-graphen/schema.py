import graphene
import json
from datetime import datetime
import uuid


class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return f"https://cloudinary.com/{self.username}/{self.id}"


# Query
class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "World1"

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        print(info)
        print(info.context)
        return [
                User(id="1", username="Bamba", created_at=datetime.now()),
                User(id="2", username="Matar", created_at=datetime.now()),
                User(id="3", username="Modou", created_at=datetime.now()),
                User(id="4", username="Khady", created_at=datetime.now()),
                User(id="5", username="Lamine", created_at=datetime.now()),
                User(id="6", username="Momar", created_at=datetime.now()),
                User(id="7", username="Kara", created_at=datetime.now()),
                User(id="8", username="Ousmane", created_at=datetime.now()),
                User(id="9", username="Momar", created_at=datetime.now()),
                User(id="10", username="Diakhou", created_at=datetime.now()),
                User(id="11", username="Coumba", created_at=datetime.now()),

        ][:limit]


# Mutation
class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)


class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)
    
    class Arguments:
        title = graphene.String()
        content = graphene.String()
    
    def mutate(self, info, title, content):
        if(info.context.get("is_anonymous")):
            raise Exception("Not authentificated !")
        post = Post(title=title, content=content)
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
  """
     mutation {
        createPost(title: "ff", content: "$content") {
            post{
              title
              content
            }
        }
     }
  """,
  context={"is_anonymous": False}


)
print(result)
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))
