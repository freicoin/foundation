from django.db import models

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=40)
    parent_category = models.ForeignKey('self', blank=True, null=True, 
                                        related_name="child_categories")

    @property
    def validated(self):
        return self.merchants.filter(validated_by__isnull=False)

    @property
    def candidates(self):
        return self.merchants.filter(validated_by__isnull=True
                                     ).filter(validated__isnull=True)
    @property
    def blocked(self):
        return self.merchants.filter(validated_by__isnull=True
                                     ).filter(validated__isnull=False)

    @property
    def inner_merchants(self):
        total = self.merchants.count()
        for cat in self.child_categories.all():
            total += cat.inner_merchants
        return total

    @property
    def inner_validated(self):
        total = self.validated.count()
        for cat in self.child_categories.all():
            total += cat.inner_validated
        return total

    @property
    def inner_candidates(self):
        total = self.candidates.count()
        for cat in self.child_categories.all():
            total += cat.inner_candidates
        return total

    @property
    def inner_blocked(self):
        total = self.blocked.count()
        for cat in self.child_categories.all():
            total += cat.inner_blocked
        return total

    def __unicode__(self):
        return self.name

class Merchant(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey('Category', related_name='merchants')
    website = models.URLField()
    short_description = models.CharField(max_length=350)
    long_description = models.CharField(max_length=1500)

    created = models.DateTimeField(auto_now_add=True)
    validated = models.DateTimeField(null=True)
    validated_by = models.ForeignKey(User, null=True, related_name="merchants_validated")
    user = models.ForeignKey(User)

    @property
    def validation_state(self):
        if self.validated_by:
            return 'validated'
        elif self.validated:
            return 'blocked'
        else:
            return 'candidate'

    def __unicode__(self):
        return self.name
