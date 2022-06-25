
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("network/<str:user>", views.profile, name="profile"),
    path("following",views.following, name= "following"),


    #API Routes
    path("newpost", views.newPost, name="newpost"),
    path("newcomment", views.newComment, name="newcomment"),
    path("newrelation", views.newRelation, name = "relation"),
    path("updatepost",views.updatePost, name = "updatepost"),
    path("deletepost", views.deletePost, name = "deletepost"),
    path("likepost", views.newLike, name = "newlike")
]
