from django.db import models
from authentication.models import MyUser


class Post(models.Model):
    image = models.ImageField(upload_to='posts/')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    like_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    @classmethod
    def all_(cls):
        return cls.objects.raw("SELECT * FROM blog_post")

    @classmethod
    def get_(cls, pk):
        query = f"SELECT * FROM blog_post WHERE id={pk}"
        return cls.objects.raw(query)[0]

    @classmethod
    def create_(cls, **data):
        query = f"INSERT INTO blog_post (image, author) VALUES ({data['image']}, {data['author']})"
        return cls.objects.raw(query)

    @classmethod
    def delete_(cls, pk):
        query = f"DELETE FROM blog_post WHERE id={pk}"
        return cls.objects.raw(query)

    @classmethod
    def filter_(cls, author=None, is_published=None):
        if author and is_published:
            query = f"SELECT * FROM blog_post WHERE author_id={author} and is_published={is_published}"
        elif author:
            query = f"SELECT * FROM blog_post WHERE author_id={author}"
        else:
            query = f"SELECT * FROM blog_post WHERE is_published={is_published}"
        return cls.objects.raw(query)


class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post.id)


class LikePost(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post.id)


class FollowUser(models.Model):
    follower = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.following.user.username
