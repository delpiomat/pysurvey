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

# per test
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
            logger.error(str(a)+"adasdasdasd")
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
        return render(request, 'studenti_value.html',result)


# per sondaggio
class Studenti(View):

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

        return render(request, "studenti.html", result)

    def post(self, request, *args, **kwargs):
        logger.error("la post! ")


        for key in request.POST:
            logger.error(key)
            logger.error("value "+request.POST[key])

        nuova_persona = Persona()
        if request.POST['cap']== "":
            nuova_persona.cap = None
        else:
            nuova_persona.cap = request.POST['cap']

        if request.POST['anno']== "":
            nuova_persona.anno_nascita = None
        else:
            nuova_persona.anno_nascita = request.POST['anno']

        if request.POST['citta']== "":
            nuova_persona.citta = None
        else:
            nuova_persona.citta = request.POST['citta']

        if request.POST['email']== "":
            nuova_persona.email = None
        else:
            nuova_persona.email = request.POST['email']

        if request.POST['voto']== "":
            nuova_persona.voto_finale = None
        else:
            nuova_persona.voto_finale = request.POST['voto']

        if request.POST['note']== "":
            nuova_persona.note = None
        else:
            nuova_persona.note = request.POST['note']

        if request.POST['optionsRadios']== "true":
            nuova_persona.esperienze_pregresse = True
        else:
            nuova_persona.esperienze_pregresse = False

        if request.POST['numero_attivita_svolte']== "":
            nuova_persona.numero_attivita_svolte = None
        else:
            nuova_persona.numero_attivita_svolte = request.POST['numero_attivita_svolte']

        if request.POST['numero_mesi_attivita_svolte']== "":
            nuova_persona.numero_mesi_attivita_svolte = None
        else:
            nuova_persona.numero_mesi_attivita_svolte = request.POST['numero_mesi_attivita_svolte']

        if request.POST['desc_esperienze_pregresso']== "":
            nuova_persona.desc_esperienze_pregresse = None
        else:
            nuova_persona.desc_esperienze_pregresse = request.POST['desc_esperienze_pregresso']

        if request.POST['stipendio_futuro']== "":
            nuova_persona.stipendio_futuro = None
        else:
            nuova_persona.stipendio_futuro = request.POST['stipendio_futuro']

        if request.POST['possibilita_trasferirsi_option']== "true":
            nuova_persona.possibilita_trasferirsi = True
        else:
            nuova_persona.possibilita_trasferirsi = False


        # Ora parliamo delle chiavi esterne con solo un valore Possibile
        livello_pc_post = json.loads(request.POST["livello_pc"])
        if len(livello_pc_post) <= 0:
            nuova_persona.livello_uso_computer = None
        elif len( LivelloPC.objects.filter(valore=livello_pc_post[0].capitalize()) ) > 0 :
            nuova_persona.livello_uso_computer = LivelloPC.objects.filter(valore=livello_pc_post[0].capitalize())[0]
        else:
            livello_pc = LivelloPC(valore=livello_pc_post[0].capitalize())
            livello_pc.save()
            nuova_persona.livello_uso_computer = livello_pc


        zona_post = json.loads(request.POST["zona"])
        if len(zona_post) <= 0:
            nuova_persona.zona = None
        elif len(Zona.objects.filter(valore=zona_post[0].capitalize())) > 0:
            nuova_persona.zona = Zona.objects.filter(valore=zona_post[0].capitalize())[0]
        else:
            zona = Zona(valore=zona_post[0].capitalize())
            zona.save()
            nuova_persona.zona = zona

        grado_studi_post = json.loads(request.POST["grado_studi"])
        if len(grado_studi_post) <= 0:
            nuova_persona.grado_studi_post = None
        elif len(GradoStudi.objects.filter(valore=grado_studi_post[0].capitalize())) > 0:
            nuova_persona.grado_studi = GradoStudi.objects.filter(valore=grado_studi_post[0].capitalize())[0]
        else:
            grado_studi = LivelloPC(valore=GradoStudi[0].capitalize())
            grado_studi.save()
            nuova_persona.grado_studi = grado_studi



        nuova_persona.save()

        return render(request, 'grazie.html')



class Grazie(View):

    def get(self, request, *args, **kwargs):
        return render(request, "grazie.html")

    def post(self, request, *args, **kwargs):
        return render(request, "grazie.html")
