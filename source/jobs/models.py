# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

JOBS = (
	("Booster", "Booster"),
)

class Job(models.Model):
	position = models.CharField(choices=JOBS, max_length=10)
	commission = models.IntegerField()
	description = models.CharField(max_length=500)
	is_open = models.BooleanField(default=True)

	def __str__(self):
		return "{position} for {commission} percent commission".format(
			position=self.position, commission=self.commission
		)

