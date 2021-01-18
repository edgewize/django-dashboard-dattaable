# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wave(models.Model):
    name =  models.CharField(max_length=99)
    site_id = models.CharField(max_length=9)
    nws_gage = models.CharField(max_length=9, default='0000')
    in_level = models.IntegerField(default=0)
    awesome_level = models.IntegerField(default=0)
