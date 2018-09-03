# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from royaleaccounts.utils import unique_slug_generator

import os
from PIL import Image

def get_filename_extension(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def image_upload_path(instance, filename):
	new_filename = instance.slug
	name, ext = get_filename_extension(filename)
	final_filename = '{name}{ext}'.format(name=name, ext=ext)
	return 'blog/posts/{new_filename}/{final_filename}'.format(
		new_filename=new_filename, 
		final_filename=final_filename
	 )

class Post(models.Model):
	slug = models.SlugField(blank=True, null=True, unique=True)

	title = models.CharField(max_length=255)
	title_img = models.ImageField(upload_to=image_upload_path)
	author = models.CharField(max_length=25, default="Rob Rangal")
	description = models.CharField(max_length=500, blank=True, null=True)
	content = models.TextField()

	views = models.IntegerField()
	read_time = models.SmallIntegerField(default=5)
	written_the = models.DateTimeField(auto_add_now=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("blogs:post", kwargs={"slug": self.slug})

	def get_slug_title(self):
		return self.title.replace(' ', '-')

	def add_view(self):
		self.views += 1
		self.save()

	def first_letter(self):
		return self.content[0]

# Assigns a slug to a Post object, if its slug field is emtpy, before saving.
def account_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance, 1)

pre_save.connect(account_pre_save_receiver, sender=Post)








