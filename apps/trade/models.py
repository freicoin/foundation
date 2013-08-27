from django.db import models

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=40)
    parent_category = models.ForeignKey('self', blank=True, null=True, 
                                        related_name="child_categories")

    def __unicode__(self):
        return self.name

class Merchant(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey('Category', related_name='merchants')
    website = models.URLField()
    short_description = models.CharField(max_length=350)
    long_description = models.CharField(max_length=1500)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    validated_by = models.ForeignKey(User, null=True, related_name="merchants_validated")
    validated = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.name
