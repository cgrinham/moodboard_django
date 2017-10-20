from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class UserImage(models.Model):
    owner = models.ForeignKey(User)
    filename = models.CharField(max_length=100)
    directory = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return "%s : %s" % (self.owner, self.filename)
