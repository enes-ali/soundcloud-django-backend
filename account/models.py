from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import _user_has_perm, _user_has_module_perms



class AccountManager(BaseUserManager):
    def _create_user(self, email, username, password, name, surname, age, gender, save):
        if (email == None or username == None or password == None or name == None 
            or surname == None or age == None or gender == None):
            raise ValueError("You cannot provide null fields")
        
        email = self.normalize_email(email)

        user = self.model(username=username, email=email, name=name, surname=surname,
            age=age, gender=gender)
        user.set_password(password)
        
        if save: 
            user.save(using=self._db)
        return user
        

    def create_user(self, email, username, password, name, surname, age, gender):
        return self._create_user(email, username, password, name, surname, age, gender, True)

    def create_superuser(self, email, username, password, name, surname, age, gender):
        user = self._create_user(email, username, password, name, surname, age, gender, False)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=24)

    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    age =  models.PositiveIntegerField()
    
    # Id of a location node from geoencoding api
    location_node_id = models.BigIntegerField(verbose_name="loaction node id")

    MALE = 'ML'
    FEMALE = 'FM'
    OTHER = 'OT'
    NONE = 'NONE'
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
        (NONE, "I don't want to provide")
    ]
    
    gender = models.CharField(max_length=4, choices=GENDER_CHOICES)
    join_date = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'name', 'surname', 'age', 'gender']


    def has_perm(self, perm, obj=None):
        if self.is_superuser and self.is_active:
            return True
        return _user_has_perm(self, perm, obj)


    def has_module_perms(self, app_label):
        if self.is_superuser and self.is_active:
            return True
        return _user_has_module_perms(self, app_label)
    