# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    state_type = (
		('pending', 'Pending'),
		('confirm', 'Confirm'),
        ('delete', 'Delete')
	)

    title = models.CharField(max_length=100, null=True, blank=True)
    parent_task = models.ForeignKey("self", null=True,blank=True)
    due_date = models.DateField()
    state = models.CharField(max_length=100,choices=state_type, null=True)
    user = models.ForeignKey(User, null=True,blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title