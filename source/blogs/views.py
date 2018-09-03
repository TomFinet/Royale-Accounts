# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView
from django.http import Http404

from .models import Post, PostImage

class BlogPostView(DetailView):
	template_name = 'blogs/post.html'
	context_object_name = 'post'

	def get_context_data(self, *args, **kwargs):
		context = super(BlogPostView, self).get_context_data(*args, **kwargs)
		context['images'] = PostImage.objects.filter(account=context['post'])
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		try:
			instance = Post.objects.get(slug=slug)
		except Account.DoesNotExist:
			raise Http404("Post not found.")
		except Account.MultipleObjectsReturned:
			qs = Post.objects.filter(slug=slug)
			instance = qs.first()
		except:
			raise Http404("Hmmm.")
		return instance
