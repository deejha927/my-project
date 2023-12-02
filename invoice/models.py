from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


# Create your models here.
class User(AbstractBaseUser):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    username = models.CharField(max_length=200, validators=[MinLengthValidator(3)], unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200, validators=[MinLengthValidator(6)])
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "username"
    objects = UserManager()

    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Invoices(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=200)
    date = models.DateField()


class Items(models.Model):
    invoices = models.ForeignKey(Invoices, on_delete=models.CASCADE, related_name="items")
    desc = models.TextField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
