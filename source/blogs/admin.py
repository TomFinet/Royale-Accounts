# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Post, PostImage, PostParagraph

class PostAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug']

	class Meta:
		model = Post

admin.site.register(Post, PostAdmin)


class PostImageAdmin(admin.ModelAdmin):
	list_display = ['__str__']

	class Meta:
		model = PostImage

admin.site.register(PostImage, PostImageAdmin)


class PostParagraphAdmin(admin.ModelAdmin):
	list_display = ['__str__']

	class Meta:
		model = PostParagraph

admin.site.register(PostParagraph, PostParagraphAdmin)