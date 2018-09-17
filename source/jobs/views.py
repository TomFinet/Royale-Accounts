# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic import ListView, DetailView

from .models import Job

class JobsListView(ListView):
	template_name = 'jobs/jobs.html'
	paginate_by = 8
	queryset = Job.objects.filter(is_open=True)
	context_object_name = 'job_list'
