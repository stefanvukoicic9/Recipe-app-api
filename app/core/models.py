from logging import exception
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db.models.manager import EmptyManager

from .check_email import check

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_filds):
        '''Create and save new user'''
        if not email:
            raise ValueError("Email is not valid!")
        user = self.model(email=self.normalize_email(email), **extra_filds)
        user.set_password(password)
        user.save(using=self._db)
        return user
        

    def create_superuser(self, email, password):
        """Create and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user model that support using email instead of username'''
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()


    USERNAME_FIELD = 'email'
