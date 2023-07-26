from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name,tc, password=None,password2=None):
        """
        Creates and saves a User with the given email, name,tc and password
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,tc, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","tc"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class Profile(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    pimage = models.ImageField(upload_to='profile/images', default="static/picture1.jpg")
    profileimage = models.ImageField(upload_to='profile/images', default="static/profile2.avif")


class PersonalInfo(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    Date_of_Birth= models.DateTimeField(max_length=200)
    Gender = models.CharField(max_length=200)
    place=models.CharField(max_length=200)

class Education(models.Model):
   user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
   pass

class Experiance(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    pass

class Skills(models.Model):
    pass
