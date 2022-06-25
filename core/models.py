from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from uuid import uuid4
import os
# Create your models here.


def image_file_path(instance, filename):
    suffix = filename.split('.')[-1]
    filename = f'{uuid4()}.{suffix}'
    return os.path.join("upload/images", filename)

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if email is not None:
            user = self.model(email=self.normalize_email(email), **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

        raise ValueError("Email is required!")

    def create_superuser(self, email, password=None, **extra_fields):
        if email is not None:
            user = self.create_user(email=email, password=password, **extra_fields)
            user.is_staff = True
            user.is_superuser = True
            user.save(using= self._db)
            return user

        raise ValueError("Email is required!")

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=120)
    bio = models.TextField()
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to=image_file_path, null=True, blank=True)
    password = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=image_file_path, null=True)

    def __str__(self):
        return self.title


class Content(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    publish = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag')

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    body = models.TextField()

    def __str__(self) -> str:
        return str(self.id)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return self.content.title


class Bookmark(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

