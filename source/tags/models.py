# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

TAG_CHOICES = (
	("level-1", "level-1"),
	("level-2", "level-2"),
	("level-3", "level-3"),
	("level-4", "level-4"),
	("level-5", "level-5"),
	("level-6", "level-6"),
	("level-7", "level-7"),
	("level-8", "level-8"),
	("level-9", "level-9"),
	("level-10", "level-10"),
	("level-11", "level-11"),
	("level-12", "level-12"),
	("level-13", "level-13"),

	("legendary", "legendary"),
	("maxed-out", "maxed-out"),
	("max-level", "max-level"),
	
	("gold", "gold"),
	("gems", "gems"),
)


class Tag(models.Model):
	name = models.CharField(choices=TAG_CHOICES, max_length=20)

	def __str__(self):
		return self.name
