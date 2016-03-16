from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render, redirect, render_to_response, RequestContext

from django.views.generic import View
from .models import Column,Survey

import json

# import the logging library #per debug scrive nella Console
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Index Page.
class Index(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        return render(request, 'index.html')


# Create New Survey
class NewSurvey(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'new_survey.html')

    def post(self, request, *args, **kwargs):

        # recupero le informazioni arrivate tramite POST
        title_survey = request.POST["question_title"]
        data = json.loads(request.POST["data"])

        new_survey = Survey(name=title_survey, note="Un questionario")
        new_survey.save()

        for i, col in enumerate(data):
            logger.error("colonna "+str(i))
            logger.error(col)
            new_col = Column(label=col["label"], survey=new_survey)
            new_col.option = col["field_options"]
            new_col.type = col["field_type"]
            new_col.required = col["required"]
            if "description" in col["field_options"]:
                new_col.description = col["field_options"]["description"]
            new_col.jsonCode = col
            new_col.num_order = i
            new_col.cid = col["cid"]
            new_col.save()

        return render(request, 'new_survey.html')