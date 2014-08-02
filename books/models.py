from django.db import models
from django.contrib import auth

# Create your models here.
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
    user = models.ForeignKey(auth.models.User)
    sdate = models.DateField()
    edate = models.DateField()
    count = models.IntegerField(default=3)
    class Meta:
        db_table = 'record'


class HistoryRecord(models.Model):
    book = models.OneToOneField(Book)
    user = models.ForeignKey(auth.models.User)
    sdate = models.DateField()
    edate = models.DateField()
    class Meta:
        db_table = '"history_record"'
