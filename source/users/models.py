# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
)

from uuid import uuid4

class UserManager(BaseUserManager):
	def create_user(self, email, password=None, 
		is_active=True, is_staff=False, is_admin=False):
		
		if not email:
			raise ValueError("Users must have an email")
		if not password:
			raise ValueError("Users must have a password")

		user_obj = self.model(
			email = self.normalize_email(email)
		)

		user_obj.set_password(password)
		user_obj.active = is_active
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.save(using=self._db)
		return user_obj

	def create_staff(self, email, password=None):
		user_obj = self.create_user(email, password=password, is_staff=True)
		return user_obj

	def create_superuser(self, email, password=None):
		user_obj = self.create_user(email, password=password, 
			is_staff=True, is_admin=True)
		return user_obj


class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	# cart = models. so that each user has a cart

	USERNAME_FIELD = 'email'

	objects = UserManager()

	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True


class GuestEmail(models.Model):
	email = models.EmailField()
	timestamp = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.email


class AccessTokenManager(models.Manager):

	def new_or_get(self, user):
		token = None
		created = False
		qs = self.get_queryset().filter(user=user)
		if qs.count() == 1:
			token = token.first()
		else:
			token = self.model.objects.create(user=user)
			created = True

		return token, created

# Used to store tokens for one time links for password reset and account validation
class AccessToken(models.Model):
	user = models.ForeignKey(User)
	token = models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now=True)

	objects = AccessTokenManager()

	def __str__(self):
		return self.token

	def save(self, *args, **kwargs):
		if not self.token:
			self.token = str(uuid4())
		return super(AccessToken, self).save(*args, **kwargs)

	def is_valid(self):
		pass








