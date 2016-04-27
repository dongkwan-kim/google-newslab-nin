# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class VoteRegion(models.Model):
    region_id = models.CharField(max_length=100)

    # region info
    wide_region = models.CharField(max_length=5)
    election_district = models.CharField(max_length=20)
    admin_region = models.CharField(max_length=10)
    
    # analysis result
    minju_trg = models.FloatField()
    minju_avg = models.FloatField()
    minju_act = models.FloatField()
    minju_pas = models.FloatField()
    third_val = models.FloatField()
    sanuri_trg = models.FloatField()
    sanuri_avg = models.FloatField()
    sanuri_act = models.FloatField()
    sanuri_pas = models.FloatField()

class Candidate(models.Model):
    cand_name = models.CharField(max_length=5)
    cand_party_color = models.CharField(max_length=8)
    cand_region_id = models.CharField(max_length=100)
    cand_number = models.IntegerField()
    cand_profile = models.TextField()
    cand_id = models.CharField(max_length=10)

class Meta(models.Model):
    meta_name = models.CharField(max_length=10)
    meta_title = models.CharField(max_length=100)
    meta_type = models.CharField(max_length=15)
    meta_url = models.TextField()
    meta_description = models.TextField()
    meta_image = models.TextField()
