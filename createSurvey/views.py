from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render, redirect, render_to_response, RequestContext

from django.views.generic import View
from .models import Column,Domain,Survey



# Index Page.
class Index(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        return render(request, 'index.html')

#create new survey
class New_survey(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'new_survey.html')

    def post(self, request, *args, **kwargs):
        return render(request, 'new_survey.html')