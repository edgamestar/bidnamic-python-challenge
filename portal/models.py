from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass


class Campaign(models.Model):
    campaign_id = models.CharField(max_length=20, unique=True)
    structure_value = models.CharField(max_length=15)
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'campaign'
        ordering = ['campaign_id']


class AdGroup(models.Model):
    ad_group_id = models.CharField(max_length=20, unique=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT, db_column='campaign')
    alias = models.CharField(max_length=250)
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'ad_group'
        ordering = ['ad_group_id']
        unique_together = ['ad_group_id', 'campaign']


class SearchTerm(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT, db_column='campaign')
    ad_group = models.ForeignKey(AdGroup, on_delete=models.PROTECT, db_column='ad_group')
    search_term = models.CharField(max_length=200)
    clicks = models.IntegerField()
    cost = models.FloatField()
    conversion_value = models.FloatField()
    conversions = models.IntegerField()
    date = models.DateField()

    class Meta:
        db_table = 'search_term'
        ordering = ['-date']
        unique_together = ['campaign', 'ad_group', 'search_term', 'clicks', 'cost', 'conversion_value', 'conversions']
