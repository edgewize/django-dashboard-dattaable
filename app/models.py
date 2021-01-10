# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wave(models.Model):
    name =  models.CharField(max_length=50)
    site_id = models.CharField(max_length=8)
    in_level = models.IntegerField(default=0)
    awesome_level = models.IntegerField(default=0)