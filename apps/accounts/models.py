from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    """Custom user manager for the Account model.
    """
    #create_user is a method that creates a regular user with the specified attributes. It checks if the email and username are provided, and if not, it raises a ValueError. It then creates a user instance, sets the password, and saves it to the database.
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),#normalize_email is a method provided by BaseUserManager that normalizes the email address by converting it to lowercase and removing any leading or trailing whitespace.
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    #create_superuser is a method that creates a superuser (admin user) with the specified attributes. It calls the create_user method to create a regular user and then sets additional flags to indicate that the user is an admin, active, staff, and superadmin.
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    """Custom user model that extends AbstractBaseUser.
    """
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    #required fields for custom user model
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' #specifies the field that will be used as the unique identifier for authentication instead of the default username field.
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager() #specifies that the custom user manager (MyAccountManager) will be used for managing user instances of this model.

    def __str__(self):
        return self.email 
    
    #permissions
    def has_perm(self, perm, obj=None):#returns True if the user has the specified permission. In this implementation, it simply returns True, indicating that the user has all permissions.
        return self.is_admin
    
    def has_module_perms(self, add_label):#returns True if the user has permissions to view the app specified by app_label. In this implementation, it simply returns True, indicating that the user has permissions to view all apps.
        return True
