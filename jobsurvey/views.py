from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render, redirect, render_to_response, RequestContext

from django.views.generic import View
from createSurvey.models import *

# for login
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User

# check if login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

# for list of items in a page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# for Json format
import json

# for utility
from createSurvey.utils import *

# import the logging library #per debug scrive nella Console
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class StudentiValore(View):

    def get(self, request, *args, **kwargs):
        result = {}
        result['zona'] = Zona.objects.all()
        result['livello_pc'] = LivelloPC.objects.all()
        result['grado_studi'] = GradoStudi.objects.all()
        result['stato'] = Stato.objects.all()
        result['lingua'] = Lingua.objects.all()
        result['conoscenza_specifica'] = ConoscenzaSpecifica.objects.all()
        result['mansione'] = Mansione.objects.all()
        result['livello_cariera'] = LivelloCariera.objects.all()
        result['area_operativa'] = AreaOperativa.objects.all()
        result['tipo_contratto'] = TipoContratto.objects.all()
        result['benefit'] = Benefit.objects.all()
        result['ruolo'] = Ruolo.objects.all()
        result['interesse'] = Interesse.objects.all()

        return render(request, "studenti_value.html", result)

    def post(self, request, *args, **kwargs):
        logger.error("la post! ")
        logger.error(request)
        for a in request:
            logger.error(a)
        return render(request, 'studenti_value.html')

