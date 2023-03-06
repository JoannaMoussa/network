from django.test import TestCase
from .models import User, Post, Connection

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):

        #Create users
        user_1 = User.objects.create(id=1, email="ron@example.com",username="Ron")
        user_2 = User.objects.create(id=2, email="daniel@example.com",username="Daniel")
        user_3 = User.objects.create(id=3, email="sam@example.com",username="Sam")
        user_4 = User.objects.create(id=4, email="jad@example.com",username="Jad")

        #create posts
        post_1 = Post.objects.create(id=1, creator=user_4, content="tweet1")
        post_1.likers.set([user_1, user_2])

        post_2 = Post.objects.create(id=2, creator=user_3, content="tweet2")

        post_3 = Post.objects.create(id=3, creator=user_2, content="tweet3")
        post_3.likers.set([user_4])

        post_4 = Post.objects.create(id=4, creator=user_1, content="tweet4")
        post_4.likers.set([user_2, user_3])

        post_4 = Post.objects.create(id=5, creator=user_4, content="tweet5")
        post_4.likers.set([user_2])

        #create connections
        connection_1 = Connection.objects.create(origin=user_1, target=user_2)
        connection_2 = Connection.objects.create(origin=user_3, target=user_1)
        connection_3 = Connection.objects.create(origin=user_2, target=user_3)
        connection_4 = Connection.objects.create(origin=user_4, target=user_1)
        connection_5 = Connection.objects.create(origin=user_1, target=user_3)

    def test_user_posts_count(self):
        user = User.objects.get(username="Jad")
        self.assertEqual(user.posts.count(), 2)

    def test_user_posts_content(self):
        user = User.objects.get(username="Jad")
        posts = user.posts.all().order_by("timestamp")
        posts_content = []
        for post in posts:
            posts_content.append(post.content)
        self.assertEqual(posts_content, ["tweet1", "tweet5"])
    
    def test_user_likes_count(self):
        user = User.objects.get(username="Daniel")
        self.assertEqual(user.likes.count(), 3)

    def test_post_likes_count(self):
        post = Post.objects.get(id=1)
        self.assertEqual(len(post.likers.all()), 2)

    def test_followers_length(self):
        user = User.objects.get(username="Ron")
        self.assertEqual(len(user.get_followers()), 2)

    def test_followers_usernames(self):
        user = User.objects.get(username="Ron")
        users_queryset = user.get_followers()
        # Using set because order of followers doesn't matter 
        followers_usernames = set()
        for user_object in users_queryset:
            followers_usernames.add(user_object.username)
        self.assertEqual(followers_usernames, {"Sam", "Jad"})

    def test_following_length(self):
        user = User.objects.get(username="Sam")
        self.assertEqual(len(user.get_following()), 1)

    def test_following_usernames(self):
        user = User.objects.get(username="Ron")
        users_queryset = user.get_following()
        # Using set because order of followers doesn't matter 
        following_usernames = set()
        for user_object in users_queryset:
            following_usernames.add(user_object.username)
        self.assertEqual(following_usernames, {"Daniel", "Sam"})

    
