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
        result['esame'] = Esame.objects.all()
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
        result['campo_studi'] = CampoStudi.objects.all()
        result['esame'] = Esame.objects.all()
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


        # Ora parliamo delle chiavi esterne con solo un valore Possibile--------------------------------------------
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
            grado_studi = GradoStudi(valore=grado_studi_post[0].capitalize())
            grado_studi.save()
            nuova_persona.grado_studi = grado_studi

        # bisogna salverlo qua
        nuova_persona.save()
        # Ora la parte tosta i multivalore! buona fortuna-----------------------------------------------------------
        lingua_list = json.loads(request.POST["lingua"])
        if len(lingua_list) <= 0:
            nuova_lingua_attuale = LinguaAttuale(persona=nuova_persona)
            nuova_lingua_attuale.lingua = None
            nuova_lingua_attuale.save()
        else:
            for v in lingua_list:
                # esiste quella lingua nel db
                if len(Lingua.objects.filter(valore=v.capitalize())) > 0:
                    nuova_lingua_attuale = LinguaAttuale(persona=nuova_persona)
                    nuova_lingua_attuale.lingua = Lingua.objects.filter(valore=v.capitalize())[0]
                    nuova_lingua_attuale.save()
                else:
                    nuova_lingua = Lingua(valore=v)
                    nuova_lingua.save()
                    nuova_lingua_attuale = LinguaAttuale(persona=nuova_persona)
                    nuova_lingua_attuale.lingua = nuova_lingua
                    nuova_lingua_attuale.save()

        # provo ad usare variabili con stesso nome risparmio codice
        valore_list = json.loads(request.POST["conoscenza_specifica"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = ConoscenzaSpecificaAttuale(persona=nuova_persona)
            nuovo_valore_nullo.conoscenza_specifica = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(ConoscenzaSpecifica.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = ConoscenzaSpecificaAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.conoscenza_specifica = ConoscenzaSpecifica.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = ConoscenzaSpecifica(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = ConoscenzaSpecificaAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.conoscenza_specifica = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["stato"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = StatoAttuale(persona=nuova_persona)
            nuovo_valore_nullo.stato = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Stato.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = StatoAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.stato = Stato.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Stato(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = StatoAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.stato = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["mansione_attuale"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = MansioneAttuale(persona=nuova_persona)
            nuovo_valore_nullo.mansione = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Mansione.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = MansioneAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.mansione = Mansione.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Mansione(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = MansioneAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.mansione = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["mansione_pregresso"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = MansionePregresso(persona=nuova_persona)
            nuovo_valore_nullo.mansione = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Mansione.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = MansionePregresso(persona=nuova_persona)
                    nuovo_valore_gia_esistente.mansione = Mansione.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Mansione(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = MansionePregresso(persona=nuova_persona)
                    nuovo_valore_gia_esistente.mansione = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["mansione_futuro"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = MansioneFuturo(persona=nuova_persona)
            nuovo_valore_nullo.mansione = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Mansione.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = MansioneFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.mansione = Mansione.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Mansione(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = MansioneFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.mansione = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["livello_cariera_attuale"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = LivelloCarieraAttuale(persona=nuova_persona)
            nuovo_valore_nullo.livello_cariera = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(LivelloCariera.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = LivelloCarieraAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.livello_cariera = LivelloCariera.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = LivelloCariera(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = LivelloCarieraAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.livello_cariera = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["livello_cariera_pregresso"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = LivelloCarieraPregresso(persona=nuova_persona)
            nuovo_valore_nullo.livello_cariera = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(LivelloCariera.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = LivelloCarieraPregresso(persona=nuova_persona)
                    nuovo_valore_gia_esistente.livello_cariera = LivelloCariera.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = LivelloCariera(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = LivelloCarieraPregresso(persona=nuova_persona)
                    nuovo_valore_gia_esistente.livello_cariera = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["livello_cariera_futuro"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = LivelloCarieraFuturo(persona=nuova_persona)
            nuovo_valore_nullo.livello_cariera = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(LivelloCariera.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = LivelloCarieraFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.livello_cariera = LivelloCariera.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = LivelloCariera(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = LivelloCarieraFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.livello_cariera = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["ruolo_attuale"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = RuoloAttuale(persona=nuova_persona)
            nuovo_valore_nullo.ruolo = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Ruolo.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = RuoloAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.ruolo = Ruolo.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Ruolo(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = RuoloAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.ruolo = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["ruolo_pregresso"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = RuoloPregresso(persona=nuova_persona)
            nuovo_valore_nullo.ruolo = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Ruolo.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = RuoloPregresso(persona=nuova_persona)
                    nuovo_valore_gia_esistente.ruolo = Ruolo.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Ruolo(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = RuoloPregresso(persona=nuova_persona)
                    nuovo_valore_gia_esistente.ruolo = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["ruolo_futuro"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = RuoloFuturo(persona=nuova_persona)
            nuovo_valore_nullo.ruolo = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Ruolo.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = RuoloFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.ruolo = Ruolo.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Ruolo(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = RuoloFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.ruolo = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["area_operativa_attuale"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = AreaOperativaAttuale(persona=nuova_persona)
            nuovo_valore_nullo.area_operativa = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(AreaOperativa.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = AreaOperativaAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.area_operativa = AreaOperativa.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = AreaOperativa(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = AreaOperativaAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.area_operativa = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["area_operativa_pregresso"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = AreaOperativaPregresso(persona=nuova_persona)
            nuovo_valore_nullo.area_operativa = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(AreaOperativa.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = AreaOperativaPregresso(persona=nuova_persona)
                    nuovo_valore_gia_esistente.area_operativa = AreaOperativa.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = AreaOperativa(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = AreaOperativaPregresso(persona=nuova_persona)
                    nuovo_valore_gia_esistente.area_operativa = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["area_operativa_futuro"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = AreaOperativaFuturo(persona=nuova_persona)
            nuovo_valore_nullo.area_operativa = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(AreaOperativa.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = AreaOperativaFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.area_operativa = AreaOperativa.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = AreaOperativa(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = AreaOperativaFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.area_operativa = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["tipo_contratto_attuale"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = TipoContrattoAttuale(persona=nuova_persona)
            nuovo_valore_nullo.tipo_contratto = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(TipoContratto.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = TipoContrattoAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.tipo_contratto = TipoContratto.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = TipoContratto(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = TipoContrattoAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.tipo_contratto = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["tipo_contratto_pregresso"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = TipoContrattoPregesso(persona=nuova_persona)
            nuovo_valore_nullo.tipo_contratto = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(TipoContratto.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = TipoContrattoPregesso(persona=nuova_persona)
                    nuovo_valore_gia_esistente.tipo_contratto = TipoContratto.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = TipoContratto(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = TipoContrattoPregesso(persona=nuova_persona)
                    nuovo_valore_gia_esistente.tipo_contratto = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["tipo_contratto_futuro"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = TipoContrattoFuturo(persona=nuova_persona)
            nuovo_valore_nullo.tipo_contratto = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(TipoContratto.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = TipoContrattoFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.tipo_contratto = TipoContratto.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = TipoContratto(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = TipoContrattoFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.tipo_contratto = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["benefit_futuro"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = BenefitFuturo(persona=nuova_persona)
            nuovo_valore_nullo.benefit = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Benefit.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = BenefitFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.benefit = Benefit.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Benefit(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = BenefitFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.benefit = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["interesse_futuro"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = InteresseFuturo(persona=nuova_persona)
            nuovo_valore_nullo.interesse = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Interesse.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = InteresseFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.interesse = Interesse.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Interesse(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = InteresseFuturo(persona=nuova_persona)
                    nuovo_valore_gia_esistente.interesse = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["esame_attuale"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = EsameAttuale(persona=nuova_persona)
            nuovo_valore_nullo.esame = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Esame.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = EsameAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.esame = Esame.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Esame(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = EsameAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.esame = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        valore_list = json.loads(request.POST["campo_studi"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = CampoStudiAttuale(persona=nuova_persona)
            nuovo_valore_nullo.campo_studi = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(CampoStudi.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = CampoStudiAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.campo_studi = CampoStudi.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = CampoStudi(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = CampoStudiAttuale(persona=nuova_persona)
                    nuovo_valore_gia_esistente.campo_studi = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()


        return render(request, 'grazie.html',{"azienda":'0'})



class Aziende(View):

    def get(self, request, *args, **kwargs):
        result = {}
        result['citta'] = Citta.objects.all()
        return render(request, "aziende.html", result)

    def post(self, request, *args, **kwargs):
        nuova_azienda = Azienda()

        if request.POST['email'] == "":
            nuova_azienda.email = None
        else:
            nuova_azienda.email = request.POST['email']

        if request.POST['nome_referente'] == "":
            nuova_azienda.nome_referente = None
        else:
            nuova_azienda.nome_referente = request.POST['nome_referente']

        if request.POST['note'] == "":
            nuova_azienda.note = None
        else:
            nuova_azienda.note = request.POST['note']

        # Ora parliamo delle chiavi esterne-------------------------------------------
        citta_sede_post = json.loads(request.POST["citta_sede"])
        if len(citta_sede_post) <= 0:
            nuova_azienda.citta_sede = None
        elif len(Citta.objects.filter(valore=citta_sede_post[0].capitalize())) > 0:
            nuova_azienda.citta_sede = Citta.objects.filter(valore=citta_sede_post[0].capitalize())[0]
        else:
            citta = Citta(valore=citta_sede_post[0].capitalize())
            citta.save()
            nuova_azienda.citta_sede = citta

        nuova_azienda.save()
        # Ora parliamo dei multi valore-------------------------------------------
        valore_list = json.loads(request.POST["altra_sede"])
        if len(valore_list) <= 0:
            nuovo_valore_nullo = AltraSede(azienda=nuova_azienda)
            nuovo_valore_nullo.citta = None
            nuovo_valore_nullo.save()
        else:
            for v in valore_list:
                if len(Citta.objects.filter(valore=v.capitalize())) > 0:
                    nuovo_valore_gia_esistente = AltraSede(azienda=nuova_azienda)
                    nuovo_valore_gia_esistente.citta = Citta.objects.filter(valore=v.capitalize())[0]
                    nuovo_valore_gia_esistente.save()
                else:
                    nuova_valore_nuovo = Citta(valore=v)
                    nuova_valore_nuovo.save()
                    # ora essite nel db quel valore
                    nuovo_valore_gia_esistente = AltraSede(azienda=nuova_azienda)
                    nuovo_valore_gia_esistente.citta = nuova_valore_nuovo
                    nuovo_valore_gia_esistente.save()

        return render(request, 'grazie.html', {"azienda": '1', "id": nuova_azienda.id})


class Lavori(View):

    def get(self, request, *args, **kwargs):
        result = {}
        result['lingua'] = Lingua.objects.all()
        result['campo_studi'] = CampoStudi.objects.all()
        result['esame'] = Esame.objects.all()
        result['livello_cariera'] = LivelloCariera.objects.all()
        result['area_operativa'] = AreaOperativa.objects.all()
        result['tipo_contratto'] = TipoContratto.objects.all()
        result['citta'] = Citta.objects.all()
        return render(request, "lavoro.html", result)

    def post(self, request, *args, **kwargs):
        if "codice_azienda" in request.POST:
            nuovo_lavoro= Lavoro(azienda_id=request.POST["codice_azienda"])
            if request.POST['email_lavoro']== "":
                nuovo_lavoro.email_referente = None
            else:
                nuovo_lavoro.email_referente = request.POST['email_lavoro']

            if request.POST['cerca_distanza']== "":
                nuovo_lavoro.distanza_massima = None
            else:
                nuovo_lavoro.distanza_massima = request.POST['cerca_distanza']

            if request.POST['note_lavoro']== "":
                nuovo_lavoro.note_lavoro = None
            else:
                nuovo_lavoro.note_lavoro = request.POST['note_lavoro']

            nuovo_lavoro.save()
            # Ora parliamo dei multi valore-------------------------------------------
            valore_list = json.loads(request.POST["citta_sede_lavoro"])
            if len(valore_list) <= 0:
                nuovo_valore_nullo = CercaCitta(lavoro=nuovo_lavoro)
                nuovo_valore_nullo.citta = None
                nuovo_valore_nullo.save()
            else:
                for v in valore_list:
                    if len(Citta.objects.filter(valore=v.capitalize())) > 0:
                        nuovo_valore_gia_esistente = CercaCitta(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.citta = Citta.objects.filter(valore=v.capitalize())[0]
                        nuovo_valore_gia_esistente.save()
                    else:
                        nuova_valore_nuovo = Citta(valore=v)
                        nuova_valore_nuovo.save()
                        # ora essite nel db quel valore
                        nuovo_valore_gia_esistente = CercaCitta(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.citta = nuova_valore_nuovo
                        nuovo_valore_gia_esistente.save()

            valore_list = json.loads(request.POST["cerca_lingua"])
            if len(valore_list) <= 0:
                nuovo_valore_nullo = CercaLingua(lavoro=nuovo_lavoro)
                nuovo_valore_nullo.lingua = None
                nuovo_valore_nullo.save()
            else:
                for v in valore_list:
                    if len(Lingua.objects.filter(valore=v.capitalize())) > 0:
                        nuovo_valore_gia_esistente = CercaLingua(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.lingua = Lingua.objects.filter(valore=v.capitalize())[0]
                        nuovo_valore_gia_esistente.save()
                    else:
                        nuova_valore_nuovo = Lingua(valore=v)
                        nuova_valore_nuovo.save()
                        # ora essite nel db quel valore
                        nuovo_valore_gia_esistente = CercaLingua(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.lingua = nuova_valore_nuovo
                        nuovo_valore_gia_esistente.save()

            valore_list = json.loads(request.POST["cerca_campo_studi"])
            if len(valore_list) <= 0:
                nuovo_valore_nullo = CercaCampoStudio(lavoro=nuovo_lavoro)
                nuovo_valore_nullo.lingua = None
                nuovo_valore_nullo.save()
            else:
                for v in valore_list:
                    if len(CampoStudi.objects.filter(valore=v.capitalize())) > 0:
                        nuovo_valore_gia_esistente = CercaCampoStudio(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.campo_studio = CampoStudi.objects.filter(valore=v.capitalize())[0]
                        nuovo_valore_gia_esistente.save()
                    else:
                        nuova_valore_nuovo = CampoStudi(valore=v)
                        nuova_valore_nuovo.save()
                        # ora essite nel db quel valore
                        nuovo_valore_gia_esistente = CercaCampoStudio(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.campo_studio = nuova_valore_nuovo
                        nuovo_valore_gia_esistente.save()

            valore_list = json.loads(request.POST["cerca_esame"])
            if len(valore_list) <= 0:
                nuovo_valore_nullo = CercaEsami(lavoro=nuovo_lavoro)
                nuovo_valore_nullo.esame = None
                nuovo_valore_nullo.save()
            else:
                for v in valore_list:
                    if len(Esame.objects.filter(valore=v.capitalize())) > 0:
                        nuovo_valore_gia_esistente = CercaEsami(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.esame = Esame.objects.filter(valore=v.capitalize())[0]
                        nuovo_valore_gia_esistente.save()
                    else:
                        nuova_valore_nuovo = Esame(valore=v)
                        nuova_valore_nuovo.save()
                        # ora essite nel db quel valore
                        nuovo_valore_gia_esistente = CercaEsami(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.esame = nuova_valore_nuovo
                        nuovo_valore_gia_esistente.save()

            valore_list = json.loads(request.POST["cerca_area_operativa"])
            if len(valore_list) <= 0:
                nuovo_valore_nullo = CercaAreaOperativa(lavoro=nuovo_lavoro)
                nuovo_valore_nullo.area_operativa = None
                nuovo_valore_nullo.save()
            else:
                for v in valore_list:
                    if len(AreaOperativa.objects.filter(valore=v.capitalize())) > 0:
                        nuovo_valore_gia_esistente = CercaAreaOperativa(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.area_operativa = AreaOperativa.objects.filter(valore=v.capitalize())[0]
                        nuovo_valore_gia_esistente.save()
                    else:
                        nuova_valore_nuovo = AreaOperativa(valore=v)
                        nuova_valore_nuovo.save()
                        # ora essite nel db quel valore
                        nuovo_valore_gia_esistente = CercaAreaOperativa(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.area_operativa = nuova_valore_nuovo
                        nuovo_valore_gia_esistente.save()

            valore_list = json.loads(request.POST["cerca_livello_cariera"])
            if len(valore_list) <= 0:
                nuovo_valore_nullo = CercaLivelloCariera(lavoro=nuovo_lavoro)
                nuovo_valore_nullo.livello_cariera = None
                nuovo_valore_nullo.save()
            else:
                for v in valore_list:
                    if len(LivelloCariera.objects.filter(valore=v.capitalize())) > 0:
                        nuovo_valore_gia_esistente = CercaLivelloCariera(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.livello_cariera = LivelloCariera.objects.filter(valore=v.capitalize())[0]
                        nuovo_valore_gia_esistente.save()
                    else:
                        nuova_valore_nuovo = LivelloCariera(valore=v)
                        nuova_valore_nuovo.save()
                        # ora essite nel db quel valore
                        nuovo_valore_gia_esistente = CercaLivelloCariera(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.livello_cariera = nuova_valore_nuovo
                        nuovo_valore_gia_esistente.save()

            valore_list = json.loads(request.POST["cerca_livello_cariera"])
            if len(valore_list) <= 0:
                nuovo_valore_nullo = CercaLivelloCariera(lavoro=nuovo_lavoro)
                nuovo_valore_nullo.livello_cariera = None
                nuovo_valore_nullo.save()
            else:
                for v in valore_list:
                    if len(LivelloCariera.objects.filter(valore=v.capitalize())) > 0:
                        nuovo_valore_gia_esistente = CercaLivelloCariera(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.livello_cariera = LivelloCariera.objects.filter(valore=v.capitalize())[0]
                        nuovo_valore_gia_esistente.save()
                    else:
                        nuova_valore_nuovo = LivelloCariera(valore=v)
                        nuova_valore_nuovo.save()
                        # ora essite nel db quel valore
                        nuovo_valore_gia_esistente = CercaLivelloCariera(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.livello_cariera = nuova_valore_nuovo
                        nuovo_valore_gia_esistente.save()

            valore_list = json.loads(request.POST["cerca_tipo_contratto"])
            if len(valore_list) <= 0:
                nuovo_valore_nullo = CercaTipoContratto(lavoro=nuovo_lavoro)
                nuovo_valore_nullo.tipo_contratto = None
                nuovo_valore_nullo.save()
            else:
                for v in valore_list:
                    if len(TipoContratto.objects.filter(valore=v.capitalize())) > 0:
                        nuovo_valore_gia_esistente = CercaTipoContratto(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.tipo_contratto = TipoContratto.objects.filter(valore=v.capitalize())[0]
                        nuovo_valore_gia_esistente.save()
                    else:
                        nuova_valore_nuovo = TipoContratto(valore=v)
                        nuova_valore_nuovo.save()
                        # ora essite nel db quel valore
                        nuovo_valore_gia_esistente = CercaTipoContratto(lavoro=nuovo_lavoro)
                        nuovo_valore_gia_esistente.tipo_contratto = nuova_valore_nuovo
                        nuovo_valore_gia_esistente.save()
        else:
            return render(request, 'grazie.html', {"azienda": '3', "errore": "no codice Azienda"})

        return render(request, 'grazie.html', {"azienda": '2'})




class Grazie(View):

    def get(self, request, *args, **kwargs):
        return render(request, "grazie.html")

    def post(self, request, *args, **kwargs):
        return render(request, "grazie.html")
