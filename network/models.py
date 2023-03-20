from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
import pytz


class User(AbstractUser):
    def get_followers(self):
        filtered_connections = Connection.objects.filter(target=self)
        followers = []
        for connection in filtered_connections:
            followers.append(connection.origin)
        return followers
    
    def get_following(self):
        filtered_connections = Connection.objects.filter(origin=self)
        following = []
        for connection in filtered_connections:
            following.append(connection.target)
        return following


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, related_name="likes")

    def __str__(self):
        return f"{self.creator} tweeted on {self.timestamp}: {self.content[:20]}{'...' if len(self.content) > 20 else ''}"
    

    def frontend_timestamp(self):
        current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        # self.timestamp has a time zone parameter, however datetime.now() has a default value of None for this parameter.
        # I should add a time zone for the datetime.now(), otherwise the substraction will give an error:
        # TypeError: can't subtract offset-naive and offset-aware datetimes
        difference = current_time - self.timestamp
        one_day = datetime.timedelta(days=1)
        if difference < one_day: # if difference less than 1 day
            difference_seconds = int(difference.total_seconds())
            if difference_seconds < 60:
                return  f"{difference_seconds}s"
            elif difference_seconds < 60*60:
                mins = difference_seconds // 60
                return  f"{mins}m"
            else:
                hrs = difference_seconds // (60*60)
                return  f"{hrs}h"
        else: # if difference greater than 1 day
            return self.timestamp
    

    def serialize(self):
        return {
            "id": self.id,
            "creator_email": self.creator.email,
            "creator_fullname": self.creator.first_name + " " + self.creator.last_name,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likers": [user.email for user in self.likers.all()]
        }


class Connection(models.Model):
    origin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.origin} follows {self.target}"
