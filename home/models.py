from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



# Create your models here.

# The Member manager class
class MemberManager(BaseUserManager):
    """
    Custom user manager (MemberManager) where the unique identifier is the email.
    """
    def create_user(self, email, password, phone=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set for a Member.")
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, phone=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff must be True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser must be True")
        return self.create_user(email, password, phone=phone, **extra_fields)



class Member(AbstractBaseUser, PermissionsMixin) :
    email = models.EmailField(("email address"), unique=True)
    password = models.CharField(max_length=255)
    joined_date = models.DateField(auto_now_add=True)
    phone = models.IntegerField(null=True)
    status = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]

    objects=MemberManager()

    def __str__(self):
        return f"{self.email}"