from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    bio = models.TextField(blank=True)
    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    user = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "posts")
    post = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Post : {self.post}"

# model to store list of users who the user follows
class Follow(models.Model):
    user = models.OneToOneField("User", on_delete = models.CASCADE, null=False)
    follows = models.ManyToManyField("User", related_name = "following", null=True)

    def __str__(self):
        f = [user.username for user in self.follows.all()]
        return f"{self.user} follows :  {f}"
    
    def getfollows(self):
        set1 = set([user.username for user in self.follows.all().all()])
        set2 = set({self.user.username}) 
        #print("set1 : ", set1)
        #print("set2 : ", set2)
        #print("set difference : ", set1-set2)
        f = set1-set2
        data = {"num" : len(f), "follows" : f }
        #print(f"Num of followers : {len(f)}, {f}")
        return data

class Comment(models.Model):
    user = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "user_comments")
    post = models.ForeignKey("Post", on_delete = models.CASCADE, related_name = "post_comments")
    comment = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment : {self.comment}"

class Like(models.Model):
    user = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "liked_post")
    post = models.ForeignKey("Post", on_delete = models.CASCADE, related_name = "likes")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} like {self.post}"