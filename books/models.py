from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from books.forms import UserCreateForm

# Create your models here.
class ProfileBase(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        parents = [ b for b in bases if isinstance(b, ProfileBase) ]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field): fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
            UserAdmin.form = UserCreateForm
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)

class ProfileUser(object):
    __metaclass__ = ProfileBase

class OracleUser(ProfileUser):
    telephone = models.CharField(max_length=22)
    team_manager = models.CharField(max_length=20)
    team_manager_email = models.EmailField(max_length=50)
    administrator = models.CharField(max_length=20)
    admin_email = models.EmailField(max_length=50)


class Book(models.Model):
    identifier = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    class Meta:
        db_table = 'books'

    def __unicode__(self):
        return self.name


class Record(models.Model):
    book = models.OneToOneField(Book)
    user = models.ForeignKey(User)
    sdate = models.DateField()
    edate = models.DateField()
    count = models.IntegerField(default=3)
    class Meta:
        db_table = 'record'


class HistoryRecord(models.Model):
    book = models.OneToOneField(Book)
    user = models.ForeignKey(User)
    sdate = models.DateField()
    edate = models.DateField()
    class Meta:
        db_table = 'history_record'
