from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=30)
    website = models.URLField()
    short_description = models.CharField(max_length=60)
    long_description = models.CharField(max_length=600)
    foundation_address = models.CharField(max_length=34)
    freicoin_address = models.CharField(max_length=34)
    bitcoin_address = models.CharField(max_length=34)
    email = models.EmailField()

    def __unicode__(self):
        return self.name
