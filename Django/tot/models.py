from django.db import models

# Create your models here.

class Tot(models.Model):
    accnt = models.CharField(max_length=200)
    yymmdd = models.CharField(max_length=200)
    money = models.IntegerField(default=0)
    def __str__(self):
        return self.accnt

class SM(models.Model):
    yymmdd = models.CharField(max_length=10)
    hhmmss = models.CharField(max_length=10)
    type   = models.CharField(max_length=10)
    val    = models.IntegerField(default=0)
    pubdate= models.DateTimeField('date published')
    def __str__(self):
        return self.type
