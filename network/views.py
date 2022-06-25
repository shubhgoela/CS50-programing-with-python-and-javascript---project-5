import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from datetime import datetime


from .models import User, Post, Follow, Comment, Like
from .utils import getPostData, getProfileData, getfollowers, getfollowingPost

def index(request):
    #print(" index function called")
    dataprime = {}
    data = getPostData(Post.objects.all(), request.user)
    #print(data)
    l = list(data.keys())
    paginator = Paginator(l, 10)
    if request.GET.get('page'):
        try:
            page_obj = paginator.get_page(request.GET.get('page'))
        except:
            page_obj = paginator.get_page(1)
    else:
        page_obj = paginator.get_page(1)
    for i in page_obj:
        dataprime[i] = data[i]
     #print("page object : ",page_obj)
     #print("page_obj.has_next : ", page_obj.has_next)
     #print(dataprime)
    return render(request, "network/index.html",{
        "page" : "All Posts",
        "data" : dataprime,
        "page_obj" : page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# url called network/user
# user is the username of the profile being called
def profile(request, user):
    profile = User.objects.get(username = user)
    data = getProfileData(profile, request.user)
     #print(data)
    dataprime = {}
    l = list(data["posts"].keys())
    paginator = Paginator(l, 10) # Show 25 contacts per page.
    if request.GET.get('page'):
        try:
            page_obj = paginator.get_page(request.GET.get('page'))
        except:
            page_obj = paginator.get_page(1)
    else:
        page_obj = paginator.get_page(1)
    for i in page_obj:
        dataprime[i] = data["posts"][i]
     #print("page object : ",page_obj)
     #print("page_obj.has_next : ", page_obj.has_next)
     #print(dataprime)
    return render(request, "network/index.html",{
        "page" : "profile",
        "profile" : data,
        "data" : dataprime,
        "page_obj" : page_obj
    })


@login_required(login_url='/login')
def following(request):
    profile = User.objects.get(username = request.user)
    try:
        f = Follow.objects.get(user = profile).getfollows()["follows"]
    except:
        f = {}
    finally:
        data = getfollowingPost(f, request.user)
     #print(data)
    dataprime = {}
    l = list(data.keys())
    paginator = Paginator(l, 10) # Show 25 contacts per page.
    if request.GET.get('page'):
        try:
            page_obj = paginator.get_page(request.GET.get('page'))
        except:
            page_obj = paginator.get_page(1)
    else:
        page_obj = paginator.get_page(1)
    for i in page_obj:
        dataprime[i] = data[i]
     #print("page object : ",page_obj)
     #print("page_obj.has_next : ", page_obj.has_next)
     #print(dataprime)
    return render(request, "network/index.html",{
        "page" : "Following",
        "data" : data,
        "page_obj" : page_obj
    })

#------------------------------------------------------------------------------------------------------
#------------------------------------------------API---------------------------------------------------
#------------------------------------------------------------------------------------------------------

@login_required
def newPost(request):    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    #name = request.user
    #print(request.user)
    if request.user.is_authenticated:
        data = json.loads(request.body)
        #print("Data:" , data)
        if data["NewPostData"] :
            post = Post(
                user = request.user,
                post = data["NewPostData"],
            )
            post.save()
             #print('new added Data : ', post)
            #print(type(request.POST["NewPostData"]))
            #print(request.POST)
             #print("Data:" , data)
            return JsonResponse({"message": "Post data added."}, status=200)
        else:
             #print("Post data empty")
            return JsonResponse({"error": "Post data is empty."}, status=400)
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required(login_url='/login')
def newComment(request):    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    #name = request.user
    #print(request.user)
    if request.user.is_authenticated:
        data = json.loads(request.body)
         #print("Data:" , data)
        if data["NewCommentData"] :
            cmt = Comment(
                user = request.user,
                post = Post.objects.get(id = int(data["post"])),
                comment = data["NewCommentData"]
            )
            cmt.save()
             #print('new added Data : ', cmt, f"post number - {cmt.post.id}")
            #print(type(request.POST["NewPostData"]))
            #print(request.POST)
             #print("Data:" , data)
            return JsonResponse({"message": "Comment data added."}, status=200)
        else:
             #print("Post data empty")
            return JsonResponse({"error": "Comment data is empty."}, status=400)
    else:
        return HttpResponseRedirect(reverse("login"))






@login_required(login_url='/login')
def newRelation(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    if request.user.is_authenticated:
        data = json.loads(request.body)
         #print("data : ", data)
        if data["NewRelationData"] == "follow":
            if request.user.username == data['profile']:
                return JsonResponse({"error": "Dennied : Cannot follow self"}, status=400)
            else:
                try:
                    f = Follow.objects.get(user = request.user) 
                    f.follows.add(User.objects.get(username = data["profile"]))
                    f.save()  
                     #print(f)
                except:
                    return JsonResponse({"error": "Data could not be added"}, status=400)
                else:
                    return JsonResponse({"message" : "Data added"}, status=200)
        else:
            if request.user.username == data['profile']:
                return JsonResponse({"error": "Dennied : Cannot unfollow self"}, status=400)
            else: 
                try:
                    f = Follow.objects.get(user = request.user) 
                    f.follows.remove(User.objects.get(username = data["profile"]))
                    f.save()
                     #print(f)
                except:
                    return JsonResponse({"error": "Data could not be removed"}, status=400)
                else:
                    return JsonResponse({"message" : "Data removed"}, status=200)
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required(login_url='/login')
def updatePost(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    if request.user.is_authenticated:
        data = json.loads(request.body)
         #print("data : ", data)
         #print(f"id = {int(data['id'])}, dtype = {type(int(data['id']))}")
        p_id = int(data['id'])
        try:
            p = Post.objects.get(id = p_id)
        except:
            return JsonResponse({"error":"Post not found"}, status=400)
        else:
            if p.user.username == request.user.username:
                if data["PostData"]:
                    p.post = data["PostData"]
                    p.timestamp = datetime.now()
                    p.save()  
                     #print(p)
                    return JsonResponse({"message" : "Post updated"}, status=200)
                else:
                    return JsonResponse({"error" : "Post blank"}, status=400)
            else:
                return JsonResponse({"error": "Denied"}, status=400)
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required(login_url='/login')
def deletePost(request):
    if request.method !="POST":
        return JsonResponse({"error" : "POST method required"}, status=400)
    
    if request.user.is_authenticated:
        data = json.loads(request.body)
         #print("data : ", data)
         #print(f"id = {int(data['id'])}, dtype = {type(int(data['id']))}")
        try:
            p = Post.objects.get(id = int(data['id']))
        except:
            return JsonResponse({"error":"Post not found"}, status=400)
        else:
            if p.user.username == request.user.username:
                    p.delete()  
                    return JsonResponse({"message" : "Post deleted succesfully"}, status=200)
            else:
                return JsonResponse({"error": "Denied"}, status=400)
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required(login_url='/login')
def newLike(request):
    if request.method != "POST":
        return JsonResponse({"error" : "POST request required"}, status=400)
    data = json.loads(request.body)
     #print("data : ", data)
    if request.user.is_authenticated:
        try:
            p = Post.objects.get(id=data['id'])
            u = User.objects.get(username = request.user.username)
        except:
            return JsonResponse({"error" : "error fetching data"})
        else:
            if data["NewLikeData"] == "unlike":
                try:
                    l = Like.objects.get(user = u, post = p)
                except:
                    return JsonResponse({"error" : "Like data not found"})
                else:
                    l.delete()
                    return JsonResponse({"message" : "Like data deleted"})
            else:
                try:
                    l = Like(user = u, post = p)
                except:
                    return JsonResponse({"error" : "Like data not added"})
                else:
                    l.save()
                    return JsonResponse({"message" : "Like data added"})
    else:
        return HttpResponseRedirect(reverse("login"))