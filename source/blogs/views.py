# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView
from django.http import Http404

from .models import Post

class BlogPostView(DetailView):
	template_name = 'blogs/post.html'
	context_object_name = 'post'

	def get_context_data(self, *args, **kwargs):
		context = super(BlogPostView, self).get_context_data(*args, **kwargs)
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		try:
			instance = Post.objects.get(slug=slug)
		except Post.DoesNotExist:
			raise Http404("Post not found.")
		except Post.MultipleObjectsReturned:
			qs = Post.objects.filter(slug=slug)
			instance = qs.first()
		except:
			raise Http404("Hmmm.")
		instance.add_view()
		return instance
