from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserCustomManager(BaseUserManager):
    def create_user(self, number, name, password=None):
        if not number:
            raise ValueError('User must have number ')

        user = self.model(number=number, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, number, name, password):
        user = self.create_user(number, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    object = UserCustomManager()

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = ['name']

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def __str__(self):
        return self.name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Food(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.name

class Order(models.Model):
    food = models.ManyToManyField(Food)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):  # __unicode__ on Python 2
        return " (%s)" % (
            ", ".join(fod.name for fod in self.food.all()),
        )
