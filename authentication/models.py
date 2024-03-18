from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female')
)
COUNTRY_CHOICES = (
    (1, 'Uzbekistan'),
    (2, 'USA'),
    (3, 'Russia'),
)
AGE_CHOICES = (
    (1, '12-18'),
    (2, '19-32'),
    (3, '33-45'),
    (4, '46-62'),
    (5, '63 >'),
)


class MyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    alternate_email = models.EmailField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    gender = models.PositiveIntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.CharField(max_length=10, blank=True, null=True)
    country = models.PositiveIntegerField(choices=COUNTRY_CHOICES, blank=True, null=True)
    age = models.PositiveIntegerField(choices=AGE_CHOICES, blank=True, null=True)
    followers = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
