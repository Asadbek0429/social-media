from math import ceil

from django.contrib.auth.models import User
from django.db.models import F, Q
from django.shortcuts import render, redirect
from authentication.models import MyUser
from .models import Post, FollowUser, Comment, LikePost
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


@login_required(login_url='/auth/login/')
def home_view(request):
    user = MyUser.objects.filter(user_id=request.user.id).first()

    followers = FollowUser.objects.filter(follower=user)
    followers_pk = []
    for follower in followers:
        followers_pk.append(follower.following.id)
    follow_users = MyUser.objects.exclude(Q(id=user.id) | Q(id__in=followers_pk))[:4]

    search = request.GET.get('text')
    page = int(request.GET.get('p', 1))
    if search:
        author = MyUser.objects.filter(user__username=search).first()
        query = f"SELECT * FROM blog_post WHERE is_published=true and author_id={author.id} ORDER BY created_at DESC"
        posts = CPaginator(Post, 2, page, query)
    else:
        query = f"SELECT * FROM blog_post WHERE is_published=true and author_id in {tuple(followers_pk)} ORDER BY created_at DESC"
        posts = CPaginator(Post, 2, page, query)

    if request.method == "POST":
        data = request.POST
        if request.FILES:
            obj = Post.objects.create(image=request.FILES['image'], author=user)
            obj.save()
            return redirect('/')
        elif data.get('message'):
            obj = Comment.objects.create(author=user, message=data['message'], post_id=data['post_id'])
            obj.save()
            return redirect(f"/#{data['post_id']}")

    d = {
        'posts': posts,
        'follow_users': follow_users,
        'user': user,
    }

    return render(request, 'index.html', d)


@login_required(login_url='/auth/login/')
def setting_view(request):
    user = MyUser.objects.filter(user=request.user).first()

    if request.method == "POST":
        if request.POST.get('old_password'):
            data = request.POST
            user = authenticate(username=user.user.username, password=data['old_password'])
            if user and data['password1'] != '' and data['password1'] == data['password2']:
                user.password = make_password(data['password1'])
                user.save()
        elif request.POST.get('phone_number'):
            data = request.POST
            user1 = User.objects.filter(username=user.user.username).first()
            user1.email = data['email']
            user1.save()
            user.phone_number = data['phone_number']
            user.save()
        elif request.POST.get('alternate_email'):
            data = request.POST
            user = User.objects.filter(username=user.user.username).first()
            user.username = data['username']
            user.email = data['email']
            user.alternate_email = data['alternate_email']
            user.save()
        elif request.POST.get('first_name'):
            data = request.POST
            user1 = User.objects.filter(id=user.user.id).first()
            user1.first_name = data['first_name']
            user1.last_name = data['last_name']
            user1.username = data['username']
            user.age = data.get('age')
            user.gender = data.get('gender')
            user.birth_date = data['birth_date']
            user.country = data.get('country')
            user.city = data['city']
            if request.FILES:
                user.profile_picture = request.FILES['profile_picture']

            user.save(
                update_fields=['profile_picture', 'age', 'gender', 'birth_date', 'country', 'city'])
            user1.save(update_fields=['first_name', 'last_name', 'username'])

        return redirect('/setting')

    d = {
        'user': user
    }

    return render(request, 'account-setting.html', d)


@login_required(login_url='/auth/login/')
def profile_view(request):
    pk = request.GET.get('pk')
    user = MyUser.objects.filter(user_id=request.user.id).first()
    follower = MyUser.objects.filter(id=pk).first()
    posts = Post.objects.filter(author_id=pk)
    followers = FollowUser.objects.filter(following_id=pk)
    following = FollowUser.objects.filter(follower_id=pk)

    d = {
        'pk': int(pk),
        'user': user,
        'follower': follower,
        'posts': posts,
        'is_follower': following.filter(follower=user),
        'followers': followers,
        'following': following,
    }

    return render(request, 'profile.html', d)


def follow(request):
    _next = request.GET.get('next', '/')
    follower = MyUser.objects.filter(user=request.user)
    following = MyUser.objects.filter(id=request.GET.get('f_id'))
    obj = FollowUser.objects.filter(follower=follower.first(), following=following.first())
    if obj:
        follower.update(following=F('following') - 1)
        following.update(followers=F('followers') - 1)
        obj.delete()
    else:
        follower.update(following=F('following') + 1)
        following.update(followers=F('followers') + 1)
        data = FollowUser.objects.create(follower=follower.first(), following=following.first())
        data.save()
    return redirect(_next)


def like(request):
    author = MyUser.objects.filter(user=request.user).first()
    post = Post.objects.filter(id=request.GET.get('id'))
    obj = LikePost.objects.filter(author=author, post=post.first())
    if obj:
        post.update(like_count=F('like_count') - 1)
        obj.delete()
    else:
        post.update(like_count=F('like_count') + 1)
        data = LikePost.objects.create(author=author, post_id=request.GET.get('id'))
        data.save()
    return redirect(f'/#{post.first().id}')


class CPaginator:
    def __init__(self, model, limit, page, query):
        self.limit = limit
        self.model = model
        self.query = query
        self.p = page
        self.count = 0

    def page(self):
        self.count = self.model.objects.raw("SELECT Count(*) as id " + self.query[self.query.find("FROM"):])[0].id
        comments = Comment.objects.all()
        posts = self.model.objects.raw(self.query + f" LIMIT {self.limit * self.p}")
        for post in posts:
            post.comments = comments.filter(post_id=post.id)
        return posts

    def has_next(self):
        return self.p < ceil(self.count / self.limit)

    def next_page_number(self):
        return str(self.p + 1)
