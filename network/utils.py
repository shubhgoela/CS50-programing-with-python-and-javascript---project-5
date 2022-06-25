
from .models import User, Post, Follow, Comment, Like

def getPostData(posts,user):
    dict = {}
    for i in range(posts.count()-1,-1,-1 ):
        #print("user : " ,user), print("post : ", posts[i])
        dict[f"{posts[i].id}"] = {"user" : posts[i].user.username,
                        "txt" : posts[i].post, 
                        "num_likes" : posts[i].likes.count(),
                        "num_comments" : posts[i].post_comments.count(),
                        #"comments" : [Comment.comment for Comment in posts[i].post_comments.all()],
                        "comments" : postComments(posts[i]),
                        "user_likes" : False,
                        "timestamp" : posts[i].timestamp
                         } 
        try:
            Like.objects.get(user = User.objects.get(username = user), post = posts[i])
        except:
            dict[f"{posts[i].id}"]["user_likes"] = False
        else:
            dict[f"{posts[i].id}"]["user_likes"] = True
    return dict

def postComments(post):
    dict = {}
    if post.post_comments.count() > 0:
        for j in range(0,post.post_comments.count()):
            #print(j)
            dict[f"{j}"] = { "user" : post.post_comments.all()[j].user.username,
                            "comment" : post.post_comments.all()[j].comment,
                            "timestamp" : post.post_comments.all()[j].timestamp }
    return dict


# here user = request.user i.e. the user who is calling the data
# following contains the list of users who the profile follows
# followers contains the list of user who follow the profile
def getProfileData(profile, user):
    try:
        following = Follow.objects.get(user = profile).getfollows()
    except:
        following = {"num" : 0, "follows" : {}}
    #print("following : ", following)
    followers = getfollowers(profile)
    #print("followers : ", followers)
    dict = { "user_active" : user.username ,
             "username" : profile.username,
             "self" : True if user.username == profile.username else False,
             #"num_following" : len(Follow.objects.get(user = profile).getfollows()),
             #"num_followers" : len(getfollowers(profile)),
             "num_following" : following["num"],
             "num_followers" : followers["num"],
             "following" : following["follows"],
             "followers" : followers["followers"],
             "profile_follows_user" : True if user.username in following["follows"] else False,
             "user_follows_profile": True if user.username in followers["followers"] else False,
             "posts" : getPostData(profile.posts.all(),user)
    }
     #print("dictionary created : ", dict)
    return dict

def getfollowers(profile):
    try:
        f = profile.following.all()
    except:
        f = {"num" : 0, "followers" : {}}
        return f
    #print(f)
    d = set()
    for i in range(0,f.count()):
        #print(f"f[{i}] : {f[i]}")
        if not profile.username == f[i].user.username:
            d.add(f[i].user.username)
    d = {"num" : len(d), "followers" : d}
    return d

def getfollowingPost(following, user):
    data = {}
    data1 = {}
    #print("following :", following)
    for i in following:
         #print(i)
        data.update(getPostData(User.objects.get(username = i).posts.all(),user))
    sorted_keys = sorted(data, key=lambda x: (data[x]['timestamp']), reverse=True)
    #print("sorted keys:", sorted_keys)
    for j in sorted_keys:
        data1[j] = (data[j])
    #print("following data : ", data1)
    return data1