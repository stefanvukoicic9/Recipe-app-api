from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

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


class Owner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    photo = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    employment_domain = models.CharField(max_length=255, null=True, blank=True)
    employment_name = models.CharField(max_length=255, null=True, blank=True)
    employment_area = models.CharField(max_length=255, null=True, blank=True)
    employment_role = models.CharField(max_length=255, null=True, blank=True)
    employment_seniority = models.CharField(max_length=255, null=True, blank=True)


class Ingredient(models.Model):
    
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Recipe model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self) -> str:
        return self.name


class RateRecipe(models.Model):
    """Rate Recipe model"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    assessment = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
