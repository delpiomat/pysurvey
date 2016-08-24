from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response # RequestContext # non va

from django.views.generic import View
from createSurvey.models import *

# per eccezioni
from django.core.exceptions import ObjectDoesNotExist

# eccezioni per pagina 404
from django.http import Http404

from django.db import DataError

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

# for ajax json
from django.http import QueryDict

# for random
import random
import string

# per query django piu complesse
from django.db.models import Q

# pergestire parte di racomandazione e corelazioni
from jobsurvey.recommendation import *

# import the logging library #per debug scrive nella Console
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


#Per ogni campo del questionario studente restituisce possibili valori
def find_all_option_student():
    # inizio questionario
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
    return result


def create_modify_student_persona_survey_by_post(request, user, is_new_user, is_admin=False):
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


    # Ora parliamo delle chiavi esterne con solo un valore Possibile-------------------------
    livello_pc_post = json.loads(request.POST["livello_pc"])
    if len(livello_pc_post) <= 0:
        nuova_persona.livello_uso_computer = None
    elif len( LivelloPC.objects.filter(valore=livello_pc_post[0].capitalize()) ) > 0:
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

    # controllo EXCEPTION db
    try:
        # bisogna salverlo qua
        nuova_persona.save()
        #collego account al sondaggio
        if (is_new_user):
            # nuovo utente
            user.survey = nuova_persona
            user.save()
        elif is_admin:
            logger.error("admin modifica persona studente")
            # un admin che fa modifiche
            #ATTENZIONE SE SI CAMBIA con una post l'id del vecchio sondaggio esplode tutto
            # non conosciamo l'identita dell'utene quindi dobbiamo leggerlo dalla POST
            #per l'utente non lo facciamo salta la sicurezza
            old_survey = Persona.objects.get(pk=request.POST["id_survey"])
            try:
                nuova_persona.email = old_survey.email
                user = Account.objects.get(survey=old_survey)
                user.survey = nuova_persona
                user.save()
                nuova_persona.save()
                #eccezione gestisci il vecchio modo senza controllo accessi e autenticazioni
            except ObjectDoesNotExist:
                logger.error("account non esiste quindi non aggiungiamo l'account ma lo eliminiamo comunque ADMIN")
            old_survey.delete()
        elif user.type==0:
            old_survey = Persona.objects.get(pk=user.account.survey_id)
            try:
                # assegno vecchia email
                nuova_persona.email = old_survey.email
                nuova_persona.save()
                # aggiorno utente
                logger.error("caro utente collego all account il nuovo sondaggio")
                user.survey = nuova_persona
                user.save()
                # cancello vecchio sondaggio
                old_survey.delete()
            except ObjectDoesNotExist:
                logger.error("account non esiste quindi non aggiungiamo l'account ma lo eliminiamo comunque NON ADMIN")
    except DataError:
        logger.error("Dati inseriti male")

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


class ModifyStudente(View):

    # solo se autenticato come admin o utente
    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):

        result={}
        result = find_all_option_student()

        # per creare copie uso url GET
        copy = {}
        copy['id'] = ""
        copy['cap'] = ""
        copy['email'] = ""
        copy['citta'] = ""
        copy['anno_nascita'] = ""
        copy['note'] = ""
        copy['voto_finale'] = ""

        copy['esperienze_pregresse'] = False #si no
        copy['desc_esperienze_pregresse'] = ""
        copy['numero_attivita_svolte'] = ""
        copy['numero_mesi_attivita_svolte'] = ""

        copy['possibilita_trasferirsi'] = False #si no
        copy['stipendio_futuro'] = ""

        logger.error("modifica studente ")
        # controllo se autenticato
        if request.user.is_authenticated:
            logger.error("Sono autenticato studente")
            #controllo se passato id
            if 'id' in kwargs:
                #controllo se utente con quell ide oppure amministratore BISOGNA IMPOSTARE SUPERUSER A 1
                if (request.user.is_superuser==1) or (request.user.account.type==0 and int(request.user.account.survey.id) == int(kwargs['id'])):
                    logger.error("Posso modificare!")
                    copy['id'] = kwargs['id']
                    studente_copia=Persona.objects.select_related().get(pk=kwargs['id'])
                    if studente_copia.cap != None:
                        copy['cap'] = studente_copia.cap
                    if studente_copia.email != None:
                        copy['email'] = studente_copia.email
                    if studente_copia.citta != None:
                        copy['citta'] = studente_copia.citta
                    if studente_copia.anno_nascita != None:
                        copy['anno_nascita'] = studente_copia.anno_nascita
                    if studente_copia.note != None:
                        copy['note'] = studente_copia.note
                    if studente_copia.voto_finale != None:
                        copy['voto_finale'] = studente_copia.voto_finale
                    if studente_copia.esperienze_pregresse != None:
                        copy['esperienze_pregresse'] = studente_copia.esperienze_pregresse
                    if studente_copia.desc_esperienze_pregresse != None:
                        copy['desc_esperienze_pregresse'] = studente_copia.desc_esperienze_pregresse
                    if studente_copia.numero_attivita_svolte != None:
                        copy['numero_attivita_svolte'] = studente_copia.numero_attivita_svolte
                    if studente_copia.numero_mesi_attivita_svolte != None:
                        copy['numero_mesi_attivita_svolte'] = studente_copia.numero_mesi_attivita_svolte
                    if studente_copia.possibilita_trasferirsi != None:
                        copy['possibilita_trasferirsi'] = studente_copia.possibilita_trasferirsi
                    if studente_copia.stipendio_futuro != None:
                        copy['stipendio_futuro'] = studente_copia.stipendio_futuro

                    #chiavi esterne
                    copy['zona'] = ""
                    copy['grado_studi'] = ""
                    copy['livello_pc'] = ""
                    if studente_copia.zona != None:
                        copy['zona'] = studente_copia.zona.valore
                    if studente_copia.grado_studi != None:
                        copy['grado_studi'] = studente_copia.grado_studi.valore
                    if studente_copia.livello_uso_computer != None:
                        copy['livello_pc'] = studente_copia.livello_uso_computer.valore

                    # per campi multivalore esterni alla tabella studente
                    copy['esame'] = ""
                    copy['campo_studi'] = ""
                    copy['lingua'] = ""
                    copy['conoscenza_specifica'] = ""
                    copy['stato'] = ""
                    copy['benefit_fututo'] = ""
                    copy['interesse_futuro'] = ""

                    copy['esame'] = EsameAttuale.objects.select_related().filter(persona_id=copy['id']).exclude(esame=None)
                    copy['campo_studi'] = CampoStudiAttuale.objects.select_related().filter(persona_id=copy['id']).exclude(campo_studi=None)
                    copy['lingua'] = LinguaAttuale.objects.select_related().filter(persona_id=copy['id']).exclude(lingua=None)
                    copy['conoscenza_specifica'] = ConoscenzaSpecificaAttuale.objects.select_related().filter(persona_id=copy['id']).exclude(conoscenza_specifica=None)
                    copy['stato'] = StatoAttuale.objects.select_related().filter(persona_id=copy['id']).exclude(stato=None)
                    copy['benefit_futuro'] = BenefitFuturo.objects.select_related().filter(persona_id=copy['id']).exclude(benefit=None)
                    copy['interesse_futuro'] = InteresseFuturo.objects.select_related().filter(persona_id=copy['id']).exclude(interesse=None)

                    copy['mansione_attuale'] = ""
                    copy['mansione_pregressa'] = ""
                    copy['mansione_futura'] = ""

                    copy['mansione_attuale'] = MansioneAttuale.objects.select_related().filter(persona_id=copy['id']).exclude(mansione=None)
                    copy['mansione_pregressa'] = MansionePregresso.objects.select_related().filter(persona_id=copy['id']).exclude(mansione=None)
                    copy['mansione_futura'] = MansioneFuturo.objects.select_related().filter(persona_id=copy['id']).exclude(mansione=None)


                    copy['livello_cariera_attuale'] = ""
                    copy['livello_cariera_pregressa'] = ""
                    copy['livello_cariera_futura'] = ""

                    copy['livello_cariera_attuale'] = LivelloCarieraAttuale.objects.select_related().filter(persona_id=copy['id']).exclude(livello_cariera=None)
                    copy['livello_cariera_pregressa'] = LivelloCarieraPregresso.objects.select_related().filter(persona_id=copy['id']).exclude(livello_cariera=None)
                    copy['livello_cariera_futura'] = LivelloCarieraFuturo.objects.select_related().filter(persona_id=copy['id']).exclude(livello_cariera=None)


                    copy['ruolo_attuale'] = ""
                    copy['ruolo_pregressa'] = ""
                    copy['ruolo_futura'] = ""

                    copy['ruolo_attuale'] = RuoloAttuale.objects.select_related().filter(persona_id=copy['id']).exclude(ruolo=None)
                    copy['ruolo_pregressa'] = RuoloPregresso.objects.select_related().filter(persona_id=copy['id']).exclude(ruolo=None)
                    copy['ruolo_futura'] = RuoloFuturo.objects.select_related().filter(persona_id=copy['id']).exclude(ruolo=None)


                    copy['area_operativa_attuale'] = ""
                    copy['area_operativa_pregressa'] = ""
                    copy['area_operativa_futura'] = ""

                    copy['area_operativa_attuale'] = AreaOperativaAttuale.objects.select_related().filter(persona_id=copy['id']).exclude(area_operativa=None)
                    copy['area_operativa_pregressa'] = AreaOperativaPregresso.objects.select_related().filter(persona_id=copy['id']).exclude(area_operativa=None)
                    copy['area_operativa_futura'] = AreaOperativaFuturo.objects.select_related().filter(persona_id=copy['id']).exclude(area_operativa=None)

                    copy['tipo_contratto_attuale'] = ""
                    copy['tipo_contratto_pregressa'] = ""
                    copy['tipo_contratto_futura'] = ""

                    copy['tipo_contratto_attuale'] = TipoContrattoAttuale.objects.select_related().filter(persona_id=copy['id']).exclude(tipo_contratto=None)
                    copy['tipo_contratto_pregressa'] = TipoContrattoPregesso.objects.select_related().filter(persona_id=copy['id']).exclude(tipo_contratto=None)
                    copy['tipo_contratto_futura'] = TipoContrattoFuturo.objects.select_related().filter(persona_id=copy['id']).exclude(tipo_contratto=None)
                else:
                    logger.error("NON PUO MODIFICARE")
        result["copy"] = copy

        return render(request, "studenti.html", result)

    # POST solo se autenticato come admin o utente
    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):

        #si tratta di un utente corretto
        if request.user.is_superuser==1:
            create_modify_student_persona_survey_by_post(request, request.user, False, True)
        elif request.user.account.type==0:
            logger.error("Sei un utente con una post")
            create_modify_student_persona_survey_by_post(request, request.user.account, False, False)
        else:
            logger.error("Non Sei nessuno! cosa volevi fare? una Post su studenti:")
        return render(request, 'index.html')



# per sondaggio
class Studenti(View):

    # non deve essere autenticato
    def get(self, request, *args, **kwargs):

        # controllo errori per registrazione
        error = None
        if 'error' in kwargs:
            error = kwargs['error']

        # inizio questionario
        result = {}
        result = find_all_option_student()
        result['error'] = error

        return render(request, "studenti.html", result)

    # non deve essere autenticato
    def post(self, request, *args, **kwargs):
        # logger.error("la post! ")

        # nuovo sondaggio quindi creo account
        post = request.POST

        #creo utente nuovo
        nuovo_user = None
        username = None
        password = None
        name = None

        if request.POST['email']== "":
            return redirect('studenti', 'Email non valida inserita')

        # problema se la mail facoltativa
        name = post['email']
        username = post['email']
        password = gen_password()
        user_count = Account.objects.filter(username=username).count()
        if user_count != 0:
            return redirect('studenti', 'Email gia esistente')
        nuovo_user = Account(is_active=False, first_name=name, username=username, email=post['email'])
        nuovo_user.set_password(password)
        nuovo_user.activationCode = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        nuovo_user.save()

        # invio mail
        send_verification_email(request, nuovo_user, False, password)

        # inserisco dati sondiaggio in questo caso lo creo nuovo
        create_modify_student_persona_survey_by_post(request, nuovo_user, True)

        return render(request, 'grazie.html',{"azienda":'0'})


# tutti i tag e possibilita per azienda
def find_all_option_azienda():
    # Cerco cose per Azienda
    result = {}
    result['citta'] = Citta.objects.all()
    return result


def create_modify_azienda_sondaggio_azienda_by_post(request,user,is_new_user,is_admin=False):
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

    # salvo oggetto nuovo sondaggio
    nuova_azienda.save()

    #collego account al sondaggio
    if (is_new_user):
        logger.error("Nuovo utente crea Sondaggio azienda")
        # nuovo utente
        user.azienda = nuova_azienda
        user.save()
    elif is_admin or user.type==1:
        logger.error("admin modifica Sondaggio azienda")
        # un admin che fa modifiche
        #ATTENZIONE SE SI CAMBIA con una post l'id del vecchio sondaggio esplode tutto
        # non conosciamo l'identita dell'utene quindi dobbiamo leggerlo dalla POST
        #per l'utente non lo facciamo salta la sicurezza
        #se l'account non esiste (retrocompatibilita)
        try:
            if is_admin:
                logger.error("admin modifica Sondaggio azienda")
                old_survey = Azienda.objects.get(pk=request.POST["id_survey"])
                # cambio SIGNIFICATO di user!!! ATTENTO
                user = Account.objects.get(azienda=old_survey)
            else:
                logger.error("Azienda modifica Sondaggio azienda")
                old_survey = Azienda.objects.get(pk=user.azienda_id)
            #problema della mail non modificabile
            nuova_azienda.email = old_survey.email
            nuova_azienda.save()
            #problema di mantenere offerte di lavoro vecchie
            job_offers = Lavoro.objects.filter(azienda=old_survey)
            for job in job_offers:
                job.azienda = nuova_azienda
                job.save()
                logger.error("Job riagganciato")
            if is_admin:
                logger.error("Admin salva azienda modificata")
                user.azienda = nuova_azienda
                user.save()
            else:
                logger.error("Utente Azienda salva azienda modificata")
                user.azienda = nuova_azienda
                user.save()
        except ObjectDoesNotExist:
            logger.error("Account non esiste quindi non aggiungiamo l'account ma eliminiamo comunque sondaggio azienda")
        old_survey.delete()
    else:
        # caso che non deve mai accadere
        logger.error("Qualcuno di strano vuol modifcare azienda")

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

# modifica dati azienda
class ModifyAzienda(View):

    # solo se autenticato come admin o utente
    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):

        result={}
        result = find_all_option_azienda()

        # per creare copie uso url GET
        copy = {}
        copy['id'] = ""
        copy['email'] = ""
        copy['citta'] = ""
        copy['altra_sede'] = ""
        copy['note'] = ""
        copy['nome_referente'] = ""

        logger.error("modifca Azienda ")

        # controllo se autenticato
        if request.user.is_authenticated:
            logger.error("Sono autenticato Azienda")
            #controllo se passato id
            if 'id' in kwargs:
                #controllo se Utente e azienda(quindi tipo 1) con quell ID oppure amministratore BISOGNA IMPOSTARE SUPERUSER A 1
                if (request.user.is_superuser==1) or (request.user.account.type==1 and int(request.user.account.azienda.id) == int(kwargs['id'])):
                    logger.error("Posso modificare Azineda questionario")
                    copy['id'] = kwargs['id']
                    azienda_copia = Azienda.objects.select_related().get(pk=kwargs['id'])
                    if azienda_copia.email != None:
                        copy['email'] = azienda_copia.email
                    if azienda_copia.note != None:
                        copy['note'] = azienda_copia.note
                    if azienda_copia.nome_referente != None:
                        copy['nome_referente'] = azienda_copia.nome_referente

                    #esterno singolo
                    if azienda_copia.citta_sede != None:
                        copy['citta'] = azienda_copia.citta_sede.valore

                    # esterno multiplo
                    copy['altra_sede'] = AltraSede.objects.select_related().filter(azienda_id=copy['id']).exclude(citta=None)

                    result["copy"] = copy

                else:
                    logger.error("NON PUO MODIFICARE")
        result["copy"] = copy

        return render(request, "aziende.html", result)

    # solo se autenticato come admin o utente Azienda
    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):

    #si tratta di un utente corretto
        if request.user.is_superuser == 1:
            logger.error("Super user vuole modificare azienda accede al metodo")
            create_modify_azienda_sondaggio_azienda_by_post(request, request.user, is_new_user=False, is_admin=True)
        elif request.user.account.type == 1:
            logger.error("Azienda vuole modifcare azienda accede al metodo")
            create_modify_azienda_sondaggio_azienda_by_post(request, request.user.account, is_new_user=False, is_admin=False)
        else:
            logger.error("un altro tipo di utente!")
        return render(request, 'index.html')


class Aziende(View):

    def get(self, request, *args, **kwargs):

        # opzioni tag per azienda
        result = {}
        result = find_all_option_azienda()

        # controllo errori per registrazione
        error = None
        if 'error' in kwargs:
            error = kwargs['error']

        result['error']=error

        return render(request, "aziende.html", result)

    def post(self, request, *args, **kwargs):

        # parte creazione nuovo Accont
        # nuovo sondaggio quindi creo account
        post = request.POST

        #creo utente nuovo
        nuovo_user = None
        username = None
        password = None
        name = None

        if request.POST['email']== "":
            return redirect('aziende', 'Email non valida inserita')

        # problema se la mail facoltativa
        name = post['email']
        username = post['email']
        password = gen_password()
        user_count = Account.objects.filter(username=username).count()
        if user_count != 0:
            return redirect('aziende', 'Email gia esistente')
        nuovo_user = Account(is_active=False, first_name=name, username=username, email=post['email'], type=1) # type 1 per azienda
        nuovo_user.set_password(password)
        nuovo_user.activationCode = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        nuovo_user.save()

        # invio mail
        logger.error('invio mail azienda nuova')
        send_verification_email(request, nuovo_user, True, password) # una Azienda Va true per messaggio diverso Mail

        # inserisco dati sondiaggio AZIENDA in questo caso lo creo nuovo Stesso metodo per fare modificare vecchio sondaggio
        create_modify_azienda_sondaggio_azienda_by_post(request, nuovo_user, True)

        return render(request, 'grazie.html',{"azienda":'1'})

# ----------------Offerte Lavoro ------------------------------------------------------------------

# tutti i tag e possibilita per offerete di lavoro
def find_all_option_lavoro():
    # Cerco cose per offeerte di lavoro
    result = {}
    result['lingua'] = Lingua.objects.all()
    result['campo_studi'] = CampoStudi.objects.all()
    result['esame'] = Esame.objects.all()
    result['livello_cariera'] = LivelloCariera.objects.all()
    result['area_operativa'] = AreaOperativa.objects.all()
    result['tipo_contratto'] = TipoContratto.objects.all()
    result['citta'] = Citta.objects.all()

    return result

# serve ad inserire nuove offerte di lavoro o modificarle
def create_modify_lavoro_sondaggio_by_post(request, account, is_new_survey, is_admin):

    if "codice_azienda" in request.POST:
        # creo nuova offerta di lavoro
        nuovo_lavoro= Lavoro(azienda_id=request.POST["codice_azienda"])

        # inserirsco valori singoli se presenti
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

        # inserisco nel db
        nuovo_lavoro.save()
        # Ora parliamo di Attributi multi valore-------------------------------------------

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




# modifica dati offerta di lavoro
class ModifyLavoro(View):

    # solo se autenticato come admin o utente
    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):

        result={}
        result = find_all_option_lavoro()
        result['error']=''

        # per creare copie uso url GET
        copy = {}
        copy['id'] = ""
        copy['codice_azienda'] = ""
        copy['email_referente'] = ""
        copy['distanza'] = ""
        copy['note'] = ""

        copy['lingua'] = ""
        copy['campo_studi'] = ""
        copy['esame'] = ""
        copy['livello_cariera'] = ""
        copy['area_operativa'] = ""
        copy['tipo_contratto'] = ""
        copy['citta'] = ""

        # passo nella lista copy le parti gia esistenti da copiare
        if 'id' in kwargs:
            copy['id'] = kwargs['id']
            lavoro_copia = Lavoro.objects.select_related().get(pk=kwargs['id'])
            if lavoro_copia.email_referente != None:
                copy['email_referente'] = lavoro_copia.email_referente
            if lavoro_copia.distanza_massima != None:
                copy['distanza_massima'] = lavoro_copia.distanza_massima
            if lavoro_copia.note_lavoro != None:
                copy['note_lavoro'] = lavoro_copia.note_lavoro

            # chiave esterna
            if lavoro_copia.azienda_id != None:
                copy['codice_azienda'] = lavoro_copia.azienda_id

            # esterno multiplo
                copy['citta'] = CercaCitta.objects.select_related().filter(lavoro_id=copy['id']).exclude(citta=None)
                copy['lingua'] = CercaLingua.objects.select_related().filter(lavoro_id=copy['id']).exclude(lingua=None)
                copy['campo_studi'] = CercaCampoStudio.objects.select_related().filter(lavoro_id=copy['id']).exclude(campo_studio=None)
                copy['esame'] = CercaEsami.objects.select_related().filter(lavoro_id=copy['id']).exclude(esame=None)

                copy['livello_cariera'] = CercaLivelloCariera.objects.select_related().filter(lavoro_id=copy['id']).exclude(livello_cariera=None)
                copy['area_operativa'] = CercaAreaOperativa.objects.select_related().filter(lavoro_id=copy['id']).exclude(area_operativa=None)
                copy['tipo_contratto'] = CercaTipoContratto.objects.select_related().filter(lavoro_id=copy['id']).exclude(tipo_contratto=None)

            result["copy"] = copy

        else:
            logger.error("id offerta lavoro non valido")
            result = {}
            result['error'] = "offerta di lavoro non valida"

        # controllo se autenticato
        if request.user.is_authenticated:
            logger.error("Sono autenticato Azienda? per modificare offerta lavoro")
            #controllo se passato id

            #controllo se Utente e azienda(quindi tipo 1) con quell ID oppure amministratore BISOGNA IMPOSTARE SUPERUSER A 1
            if (request.user.is_superuser==1) or (request.user.account.type==1 and int(request.user.account.azienda.id) == int(copy['codice_azienda'])):
                logger.error("Posso modificare offerta lavoro questionario")
                result["copy"] = copy

            else:
                logger.error("NON PUO MODIFICARE")
                result = {}
                result['error'] = "Utente non valido per modifcare offerta di lavoro corrente"

        else:
            result = {}
            result['error'] = "Non sei autenticato"

        return render(request, "lavoro.html", result)

    # solo se autenticato come admin o utente Azienda
    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):

    #si tratta di un utente corretto
        if request.user.is_superuser == 1:
            logger.error("Super user vuole modificare sondaggio accede al metodo")
            create_modify_lavoro_sondaggio_by_post(request, request.user, is_new_survey=False, is_admin=True)
        elif request.user.account.type == 1:
            logger.error("Azienda vuole modifcare sondaggio accede al metodo")
            create_modify_lavoro_sondaggio_by_post(request, request.user.account, is_new_survey=False, is_admin=False)
        else:
            logger.error("un altro tipo di utente!")
        return render(request, 'index.html')



class Lavori(View):

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        result = {}
        result = find_all_option_lavoro()

        # imposto di default codice azienda
        copy = {}
        copy['codice_azienda']=""
        if request.user.account.azienda_id:
            copy['codice_azienda'] = request.user.account.azienda_id
        else:
            logger.error("qualcuno di sbagliato cerca di fare sondaggio offerte di lavoro")
        result['copy']=copy

        return render(request, "lavoro.html", result)

    @method_decorator(login_required(login_url='log_in'))
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

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        return render(request, "grazie.html")

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
        return render(request, "grazie.html")

def all_aziende():
    result = {}

    # aziende
    list_aziende = Azienda.objects.all().select_related()

    # altra sede
    list_altra_sede = AltraSede.objects.all().select_related()

    for a in list_aziende:
        if a.citta_sede != None:
            citta_sede = a.citta_sede.valore
        else:
            citta_sede = "None"
        result[a.id] = {'id': a.id, 'note': a.note, 'citta_sede': citta_sede, 'email': a.email,
                        "nome_referente": a.nome_referente, 'altra_sede': "", 'data': a.pub_date}

    for las in list_altra_sede:
        if las.citta != None:
            if result[las.azienda.id]['altra_sede'] != "":
                result[las.azienda.id]['altra_sede'] += "," + las.citta.valore
            else:
                result[las.azienda.id]['altra_sede'] += las.citta.valore
        else:
            result[las.azienda.id]['altra_sede'] += "None"

    return result

class RisultatiAziende(View):

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        result = {}
        # se non admin pagina non trovata
        if request.user.is_superuser != 1:
            raise Http404("Solo un admin puo vedere questa pagina")
        result = all_aziende()
        return render(request, "risultati.html", {"result": result, "type": 1})

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
        # se non admin pagina non trovata
        if request.user.is_superuser != 1:
            raise Http404("Solo un admin puo effettuare questa richiesta")
        if request.method == 'POST':
            if "id" in request.POST:
                azienda = Azienda.objects.get(pk=int(request.POST["id"]))
                azienda.delete()

            response_data = {}

            response_data['msg'] = 'Azienda eliminato con id: ' + request.POST["id"]

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"niente da vedere": "errore!"}),
                content_type="application/json"
            )

def all_job():
    result = {}
    # lavori
    list_lavori = Lavoro.objects.all().select_related()

    for l in list_lavori:
        result[l.id] = {"id": l.id, 'id_azienda': l.azienda_id,
                        'note_azienda': l.azienda.note, "email_riferimento_azienda": l.azienda.email,
                        'email_riferimento_lavoro': l.email_referente, "citta_lavoro": "", 'lingua': "",
                        'campo_studi': "", 'esami': "", 'area_operativa': "", 'livello_cariera': "",
                        'tipo_contratto': "", 'distanza': l.distanza_massima, 'note': l.note_lavoro,
                        'data': l.pub_date}

    # citta lavoro
    list_citta_lavoro = CercaCitta.objects.all().select_related()
    for lcs in list_citta_lavoro:
        if lcs.citta != None:
            if result[lcs.lavoro.id]['citta_lavoro'] != "":
                result[lcs.lavoro.id]['citta_lavoro'] += "," + lcs.citta.valore
            else:
                result[lcs.lavoro.id]['citta_lavoro'] += lcs.citta.valore
        else:
            result[lcs.lavoro.id]['citta_lavoro'] += "None"

    # lingua cerca lavoro
    list_lingua = CercaLingua.objects.all().select_related()
    for ll in list_lingua:
        if ll.lingua != None:
            if result[ll.lavoro.id]['lingua'] != "":
                result[ll.lavoro.id]['lingua'] += "," + ll.lingua.valore
            else:
                result[ll.lavoro.id]['lingua'] += ll.lingua.valore
        else:
            result[ll.lavoro.id]['lingua'] += "None"

    # campo studi cerca lavoro
    list_campo_studi = CercaCampoStudio.objects.all().select_related()
    for lcs in list_campo_studi:
        if lcs.campo_studio != None:
            if result[lcs.lavoro.id]['campo_studi'] != "":
                result[lcs.lavoro.id]['campo_studi'] += "," + lcs.campo_studio.valore
            else:
                result[lcs.lavoro.id]['campo_studi'] += lcs.campo_studio.valore
        else:
            result[lcs.lavoro.id]['campo_studi'] += "None"

    # esami cerca lavoro
    list_esami = CercaEsami.objects.all().select_related()
    for le in list_esami:
        if le.esame != None:
            if result[le.lavoro.id]['esami'] != "":
                result[le.lavoro.id]['esami'] += "," + le.esame.valore
            else:
                result[le.lavoro.id]['esami'] += le.esame.valore
        else:
            result[le.lavoro.id]['esami'] += "None"

    # area_operativa cerca lavoro
    list_area_operativa = CercaAreaOperativa.objects.all().select_related()
    for lao in list_area_operativa:
        if lao.area_operativa != None:
            if result[lao.lavoro.id]['area_operativa'] != "":
                result[lao.lavoro.id]['area_operativa'] += "," + lao.area_operativa.valore
            else:
                result[lao.lavoro.id]['area_operativa'] += lao.area_operativa.valore
        else:
            result[lao.lavoro.id]['area_operativa'] += "None"

    # livello_cariera cerca lavoro
    list_livello_cariera = CercaLivelloCariera.objects.all().select_related()
    for llc in list_livello_cariera:
        if llc.livello_cariera != None:
            if result[llc.lavoro.id]['livello_cariera'] != "":
                result[llc.lavoro.id]['livello_cariera'] += "," + llc.livello_cariera.valore
            else:
                result[llc.lavoro.id]['livello_cariera'] += llc.livello_cariera.valore
        else:
            result[llc.lavoro.id]['livello_cariera'] += "None"

    # tipo_contratto cerca lavoro
    list_tipo_contratto = CercaTipoContratto.objects.all().select_related()
    for ltc in list_tipo_contratto:
        if ltc.tipo_contratto != None:
            if result[ltc.lavoro.id]['tipo_contratto'] != "":
                result[ltc.lavoro.id]['tipo_contratto'] += "," + ltc.tipo_contratto.valore
            else:
                result[ltc.lavoro.id]['tipo_contratto'] += ltc.tipo_contratto.valore
        else:
            result[ltc.lavoro.id]['tipo_contratto'] += "None"

    return result

class RisultatiOffertaLavoro(View):
    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        result = {}
        # se non admin pagina non trovata
        if request.user.is_superuser != 1:
            raise Http404("Solo un admin puo vedere questa pagina")
        result = all_job()

        return render(request, "risultati.html", {"result": result, "type": 2})

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
        if request.user.is_superuser != 1:
            raise Http404("Solo un admin puo effettuare questa richiesta")
        if request.method == 'POST':
            if "id" in request.POST:
                lavoro = Lavoro.objects.get(pk=int(request.POST["id"]))
                lavoro.delete()

            response_data = {}

            response_data['msg'] = 'Lavoro eliminato con id: ' + request.POST["id"]

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"nothing to see": "errore imprevisto"}),
                content_type="application/json"
            )

# mette in una lista/dizionario tutti gli studenti inseriti
def all_student():
    result = {}
    # studenti
    list_studenti = Persona.objects.all().select_related()

    # chiavi esterne
    # Zona
    list_zona = Zona.objects.all().select_related()
    # Zona
    list_conoscenza_pc = LivelloPC.objects.all().select_related()

    for s in list_studenti:

        zona_tmp = "None"
        if s.zona != None:
            zona_tmp = s.zona.valore
        grado_studi_tmp = "None"
        if s.grado_studi != None:
            grado_studi_tmp = s.grado_studi.valore
        livello_uso_computer_tmp = "None"
        if s.livello_uso_computer != None:
            livello_uso_computer_tmp = s.livello_uso_computer.valore

        result[s.id] = {"id": s.id, 'cap': s.cap,
                        'email': s.email, "anno": s.anno_nascita, 'citta': s.citta, "zona": zona_tmp,
                        'grado_studi': grado_studi_tmp, 'voto': s.voto_finale, 'esami': "", 'campo_studi': "",
                        'livello_pc': livello_uso_computer_tmp, 'lingua': "", 'conoscenza_specifica': "",
                        'stato': "", 'note': s.note, 'mansione_attuale': "", 'livello_cariera_attuale': "",
                        'ruolo_attuale': "", 'area_operativa_attuale': "",
                        'tipo_contratto_attuale': "", 'lavoro_passato': s.esperienze_pregresse,
                        'numero_attivita_svolte': s.numero_attivita_svolte,
                        'mesi_attivita_svolte': s.numero_mesi_attivita_svolte,
                        'descrizione_esperienza_pregressa': s.desc_esperienze_pregresse, 'mansione_pregressa': "",
                        'livello_cariera_pregressa': "", 'ruolo_pregressa': "", 'area_operativa_pregressa': "",
                        'tipo_contratto_pregressa': "", 'mansione_futura': "", 'livello_cariera_futura': "",
                        'ruolo_futura': "", 'area_operativa_futura': "", 'tipo_contratto_futura': "", 'benefit': "",
                        'stipendio': s.stipendio_futuro, 'interesse': "",
                        'possibilita_trasferirsi': s.possibilita_trasferirsi,
                        'data': s.pub_date}

    # esami
    list_esami = EsameAttuale.objects.all().select_related()
    for le in list_esami:
        if le.esame != None:
            if result[le.persona.id]['esami'] != "":
                result[le.persona.id]['esami'] += "," + le.esame.valore
            else:
                result[le.persona.id]['esami'] += le.esame.valore
        else:
            result[le.persona.id]['esami'] += "None"

            # lingua
    list_lingua = LinguaAttuale.objects.all().select_related()
    for ll in list_lingua:
        if ll.lingua != None:
            if result[ll.persona.id]['lingua'] != "":
                result[ll.persona.id]['lingua'] += "," + ll.lingua.valore
            else:
                result[ll.persona.id]['lingua'] += ll.lingua.valore
        else:
            result[ll.persona.id]['lingua'] += "None"

    # campo studi
    list_campo_studi = CampoStudiAttuale.objects.all().select_related()
    for lcs in list_campo_studi:
        if lcs.campo_studi != None:
            if result[lcs.persona.id]['campo_studi'] != "":
                result[lcs.persona.id]['campo_studi'] += "," + lcs.campo_studi.valore
            else:
                result[lcs.persona.id]['campo_studi'] += lcs.campo_studi.valore
        else:
            result[lcs.persona.id]['campo_studi'] += "None"

    # conoscenza_specifica
    list_conoscenza_specifica = ConoscenzaSpecificaAttuale.objects.all().select_related()
    for lcs in list_conoscenza_specifica:
        if lcs.conoscenza_specifica != None:
            if result[lcs.persona.id]['conoscenza_specifica'] != "":
                result[lcs.persona.id]['conoscenza_specifica'] += "," + lcs.conoscenza_specifica.valore
            else:
                result[lcs.persona.id]['conoscenza_specifica'] += lcs.conoscenza_specifica.valore
        else:
            result[lcs.persona.id]['conoscenza_specifica'] += "None"

    # stato
    list_stato = StatoAttuale.objects.all().select_related()
    for ls in list_stato:
        if ls.stato != None:
            if result[ls.persona.id]['stato'] != "":
                result[ls.persona.id]['stato'] += "," + ls.stato.valore
            else:
                result[ls.persona.id]['stato'] += ls.stato.valore
        else:
            result[ls.persona.id]['stato'] += "None"

    # mansione attuale
    list_mansione_attuale = MansioneAttuale.objects.all().select_related()
    for lma in list_mansione_attuale:
        if lma.mansione != None:
            if result[lma.persona.id]['mansione_attuale'] != "":
                result[lma.persona.id]['mansione_attuale'] += "," + lma.mansione.valore
            else:
                result[lma.persona.id]['mansione_attuale'] += lma.mansione.valore
        else:
            result[lma.persona.id]['mansione_attuale'] += "None"
    # mansione pregressa
    list_mansione_pregressa = MansionePregresso.objects.all().select_related()
    for lmp in list_mansione_pregressa:
        if lmp.mansione != None:
            if result[lmp.persona.id]['mansione_pregressa'] != "":
                result[lmp.persona.id]['mansione_pregressa'] += "," + lmp.mansione.valore
            else:
                result[lmp.persona.id]['mansione_pregressa'] += lmp.mansione.valore
        else:
            result[lmp.persona.id]['mansione_pregressa'] += "None"
    # mansione futura
    list_mansione_futura = MansioneFuturo.objects.all().select_related()
    for lmf in list_mansione_futura:
        if lmf.mansione != None:
            if result[lmf.persona.id]['mansione_futura'] != "":
                result[lmf.persona.id]['mansione_futura'] += "," + lmf.mansione.valore
            else:
                result[lmf.persona.id]['mansione_futura'] += lmf.mansione.valore
        else:
            result[lmf.persona.id]['mansione_futura'] += "None"

    # livello_cariera attuale
    list_livello_cariera_attuale = LivelloCarieraAttuale.objects.all().select_related()
    for llca in list_livello_cariera_attuale:
        if llca.livello_cariera != None:
            if result[llca.persona.id]['livello_cariera_attuale'] != "":
                result[llca.persona.id]['livello_cariera_attuale'] += "," + llca.livello_cariera.valore
            else:
                result[llca.persona.id]['livello_cariera_attuale'] += llca.livello_cariera.valore
        else:
            result[llca.persona.id]['livello_cariera_attuale'] += "None"

    # livello_cariera pregressa
    list_livello_cariera_pregressa = LivelloCarieraPregresso.objects.all().select_related()
    for llcp in list_livello_cariera_pregressa:
        if llcp.livello_cariera != None:
            if result[llcp.persona.id]['livello_cariera_pregressa'] != "":
                result[llcp.persona.id]['livello_cariera_pregressa'] += "," + llcp.livello_cariera.valore
            else:
                result[llcp.persona.id]['livello_cariera_pregressa'] += llcp.livello_cariera.valore
        else:
            result[llcp.persona.id]['livello_cariera_pregressa'] += "None"

    # livello_cariera futura
    list_livello_cariera_futura = LivelloCarieraFuturo.objects.all().select_related()
    for llcf in list_livello_cariera_futura:
        if llcf.livello_cariera != None:
            if result[llcf.persona.id]['livello_cariera_futura'] != "":
                result[llcf.persona.id]['livello_cariera_futura'] += "," + llcf.livello_cariera.valore
            else:
                result[llcf.persona.id]['livello_cariera_futura'] += llcf.livello_cariera.valore
        else:
            result[llcf.persona.id]['livello_cariera_futura'] += "None"

    # ruolo_attuale
    list_ruolo_attuale = RuoloAttuale.objects.all().select_related()
    for lra in list_ruolo_attuale:
        if lra.ruolo != None:
            if result[lra.persona.id]['ruolo_attuale'] != "":
                result[lra.persona.id]['ruolo_attuale'] += "," + lra.ruolo.valore
            else:
                result[lra.persona.id]['ruolo_attuale'] += lra.ruolo.valore
        else:
            result[lra.persona.id]['ruolo_attuale'] += "None"

    # ruolo pregressa
    list_ruolo_pregressa = RuoloPregresso.objects.all().select_related()
    for lrp in list_ruolo_pregressa:
        if lrp.ruolo != None:
            if result[lrp.persona.id]['ruolo_pregressa'] != "":
                result[lrp.persona.id]['ruolo_pregressa'] += "," + lrp.ruolo.valore
            else:
                result[lrp.persona.id]['ruolo_pregressa'] += lrp.ruolo.valore
        else:
            result[lrp.persona.id]['ruolo_pregressa'] += "None"

    # ruolo futura
    list_ruolo_futura = RuoloFuturo.objects.all().select_related()
    for lrf in list_ruolo_futura:
        if lrf.ruolo != None:
            if result[lrf.persona.id]['ruolo_futura'] != "":
                result[lrf.persona.id]['ruolo_futura'] += "," + lrf.ruolo.valore
            else:
                result[lrf.persona.id]['ruolo_futura'] += lrf.ruolo.valore
        else:
            result[lrf.persona.id]['ruolo_futura'] += "None"

    # area_operativa attuale
    list_area_operativa_attuale = AreaOperativaAttuale.objects.all().select_related()
    for laoa in list_area_operativa_attuale:
        if laoa.area_operativa != None:
            if result[laoa.persona.id]['area_operativa_attuale'] != "":
                result[laoa.persona.id]['area_operativa_attuale'] += "," + laoa.area_operativa.valore
            else:
                result[laoa.persona.id]['area_operativa_attuale'] += laoa.area_operativa.valore
        else:
            result[laoa.persona.id]['area_operativa_attuale'] += "None"

    # area_operativa pregressa
    list_area_operativa_pregressa = AreaOperativaPregresso.objects.all().select_related()
    for laop in list_area_operativa_pregressa:
        if laop.area_operativa != None:
            if result[laop.persona.id]['area_operativa_pregressa'] != "":
                result[laop.persona.id]['area_operativa_pregressa'] += "," + laop.area_operativa.valore
            else:
                result[laop.persona.id]['area_operativa_pregressa'] += laop.area_operativa.valore
        else:
            result[laop.persona.id]['area_operativa_pregressa'] += "None"

    # area_operativa futura
    list_area_operativa_futura = AreaOperativaFuturo.objects.all().select_related()
    for laof in list_area_operativa_futura:
        if laof.area_operativa != None:
            if result[laof.persona.id]['area_operativa_futura'] != "":
                result[laof.persona.id]['area_operativa_futura'] += "," + laof.area_operativa.valore
            else:
                result[laof.persona.id]['area_operativa_futura'] += laof.area_operativa.valore
        else:
            result[laof.persona.id]['area_operativa_futura'] += "None"

    # tipo_contratto attuale
    list_tipo_contratto_attuale = TipoContrattoAttuale.objects.all().select_related()
    for ltca in list_tipo_contratto_attuale:
        if ltca.tipo_contratto != None:
            if result[ltca.persona.id]['tipo_contratto_attuale'] != "":
                result[ltca.persona.id]['tipo_contratto_attuale'] += "," + ltca.tipo_contratto.valore
            else:
                result[ltca.persona.id]['tipo_contratto_attuale'] += ltca.tipo_contratto.valore
        else:
            result[ltca.persona.id]['tipo_contratto_attuale'] += "None"

    # tipo_contratto prgresso
    list_tipo_contratto_pregresso = TipoContrattoPregesso.objects.all().select_related()
    for ltcp in list_tipo_contratto_pregresso:
        if ltcp.tipo_contratto != None:
            if result[ltcp.persona.id]['tipo_contratto_pregressa'] != "":
                result[ltcp.persona.id]['tipo_contratto_pregressa'] += "," + ltcp.tipo_contratto.valore
            else:
                result[ltcp.persona.id]['tipo_contratto_pregressa'] += ltcp.tipo_contratto.valore
        else:
            result[ltcp.persona.id]['tipo_contratto_pregressa'] += "None"

    # tipo_contratto futura
    list_tipo_contratto_futura = TipoContrattoFuturo.objects.all().select_related()
    for ltcf in list_tipo_contratto_futura:
        if ltcf.tipo_contratto != None:
            if result[ltcf.persona.id]['tipo_contratto_futura'] != "":
                result[ltcf.persona.id]['tipo_contratto_futura'] += "," + ltcf.tipo_contratto.valore
            else:
                result[ltcf.persona.id]['tipo_contratto_futura'] += ltcf.tipo_contratto.valore
        else:
            result[ltcf.persona.id]['tipo_contratto_futura'] += "None"

    # benefit
    list_benefit = BenefitFuturo.objects.all().select_related()
    for lb in list_benefit:
        if lb.benefit != None:
            if result[lb.persona.id]['benefit'] != "":
                result[lb.persona.id]['benefit'] += "," + lb.benefit.valore
            else:
                result[lb.persona.id]['benefit'] += lb.benefit.valore
        else:
            result[lb.persona.id]['benefit'] += "None"

    # interesse
    list_interesse_futuro = InteresseFuturo.objects.all().select_related()
    for lif in list_interesse_futuro:
        if lif.interesse != None:
            if result[lif.persona.id]['interesse'] != "":
                result[lif.persona.id]['interesse'] += "," + lif.interesse.valore
            else:
                result[lif.persona.id]['interesse'] += lif.interesse.valore
        else:
            result[lif.persona.id]['interesse'] += "None"

    return result


class RisultatiStudenti(View):

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        result = {}
        # se non admin pagina non trovata
        if request.user.is_superuser != 1:
            raise Http404("Solo un admin puo vedere questa pagina")
        result = all_student()

        return render(request, "risultati.html", {"result": result, "type": 0})

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
        if request.user.is_superuser != 1:
            raise Http404("Solo un admin puo effettuare questa richiesta")
        if request.method == 'POST':
            if "id" in request.POST:
                studente = Persona.objects.get(pk=int(request.POST["id"]))
                studente.delete()

            response_data = {}

            response_data['msg'] = 'Studente eliminato con id: ' + request.POST["id"]

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )

# la singola Azienda vuole vedere le sue offerte di lavoro
class AziendaOffertaLavoro(View):
    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):

        result={}

        if request.user.account.azienda_id:
            # lavori della azienda cercata
            codice_id_azienda = request.user.account.azienda_id
            list_lavori = Lavoro.objects.filter(azienda=codice_id_azienda).select_related()

            logger.error("Vettore offerte lavoro lungo:"+str(len(list_lavori)) +" con id azienda"+ str(request.user.account.azienda_id))
        else:
            logger.error("errore id utente")
                    # controllo errori per registrazione
            return

        for l in list_lavori:

            result[l.id] = {"id": l.id, 'id_azienda': l.azienda_id,
                            'note_azienda': l.azienda.note,"email_riferimento_azienda": l.azienda.email ,
                            'email_riferimento_lavoro': l.email_referente, "citta_lavoro":  "", 'lingua': "",
                            'campo_studi': "", 'esami': "", 'area_operativa': "", 'livello_cariera': "",
                            'tipo_contratto': "", 'distanza': l.distanza_massima, 'note': l.note_lavoro,
                            'data': l.pub_date}

            #tutto dentro il ciclo for

            # citta lavoro
            list_citta_lavoro = CercaCitta.objects.filter(lavoro=l).select_related()
            for lcs in list_citta_lavoro:
                if lcs.citta != None:
                    if result[lcs.lavoro.id]['citta_lavoro'] != "":
                        result[lcs.lavoro.id]['citta_lavoro'] += ","+lcs.citta.valore
                    else:
                        result[lcs.lavoro.id]['citta_lavoro'] += lcs.citta.valore
                else:
                    result[lcs.lavoro.id]['citta_lavoro'] += "None"

            # lingua cerca lavoro
            list_lingua = CercaLingua.objects.filter(lavoro=l).select_related()
            for ll in list_lingua:
                if ll.lingua != None:
                    if result[ll.lavoro.id]['lingua'] != "":
                        result[ll.lavoro.id]['lingua'] += ","+ll.lingua.valore
                    else:
                        result[ll.lavoro.id]['lingua'] += ll.lingua.valore
                else:
                    result[ll.lavoro.id]['lingua'] += "None"

            # campo studi cerca lavoro
            list_campo_studi = CercaCampoStudio.objects.filter(lavoro=l).select_related()
            for lcs in list_campo_studi:
                if lcs.campo_studio != None:
                    if result[lcs.lavoro.id]['campo_studi'] != "":
                        result[lcs.lavoro.id]['campo_studi'] += ","+lcs.campo_studio.valore
                    else:
                        result[lcs.lavoro.id]['campo_studi'] += lcs.campo_studio.valore
                else:
                    result[lcs.lavoro.id]['campo_studi'] += "None"

            # esami cerca lavoro
            list_esami = CercaEsami.objects.filter(lavoro=l).select_related()
            for le in list_esami:
                if le.esame != None:
                    if result[le.lavoro.id]['esami'] != "":
                        result[le.lavoro.id]['esami'] += ","+le.esame.valore
                    else:
                        result[le.lavoro.id]['esami'] += le.esame.valore
                else:
                    result[le.lavoro.id]['esami'] += "None"

            # area_operativa cerca lavoro
            list_area_operativa = CercaAreaOperativa.objects.filter(lavoro=l).select_related()
            for lao in list_area_operativa:
                if lao.area_operativa != None:
                    if result[lao.lavoro.id]['area_operativa'] != "":
                        result[lao.lavoro.id]['area_operativa'] += ","+lao.area_operativa.valore
                    else:
                        result[lao.lavoro.id]['area_operativa'] += lao.area_operativa.valore
                else:
                    result[lao.lavoro.id]['area_operativa'] += "None"

            # livello_cariera cerca lavoro
            list_livello_cariera = CercaLivelloCariera.objects.filter(lavoro=l).select_related()
            for llc in list_livello_cariera:
                if llc.livello_cariera != None:
                    if result[llc.lavoro.id]['livello_cariera'] != "":
                        result[llc.lavoro.id]['livello_cariera'] += ","+llc.livello_cariera.valore
                    else:
                        result[llc.lavoro.id]['livello_cariera'] += llc.livello_cariera.valore
                else:
                    result[llc.lavoro.id]['livello_cariera'] += "None"

            # tipo_contratto cerca lavoro
            list_tipo_contratto = CercaTipoContratto.objects.filter(lavoro=l).select_related()
            for ltc in list_tipo_contratto:
                if ltc.tipo_contratto != None:
                    if result[ltc.lavoro.id]['tipo_contratto'] != "":
                        result[ltc.lavoro.id]['tipo_contratto'] += ","+ltc.tipo_contratto.valore
                    else:
                        result[ltc.lavoro.id]['tipo_contratto'] += ltc.tipo_contratto.valore
                else:
                    result[ltc.lavoro.id]['tipo_contratto'] += "None"

        return render(request, "risultati.html", {"result": result, "type": 2})

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if "id" in request.POST:
                lavoro = Lavoro.objects.get(pk=int(request.POST["id"]))
                lavoro.delete()

            response_data = {}

            response_data['msg'] = 'Lavoro eliminato con id: ' + request.POST["id"]

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"nothing to see": "errore imprevisto"}),
                content_type="application/json"
            )


# type puo essere 0 studente, 1 azienda, 2 lavoro
def result_csv(request, *args, **kwargs):
    # bisogna essere admin per i csv
    if request.user.is_superuser != 1:
        raise Http404("Solo un admin puo vedere questa pagina")
    try:
        if int(kwargs['type']) == 0:
            survey = all_student()
            # nomi dei campi
            col_list = ['id', 'cap', 'email', 'anno', 'citta', 'zona','grado_studi', 'voto', 'esami', 'campo_studi',
                        'livello_pc', 'lingua'"", 'conoscenza_specifica', 'stato', 'note', 'mansione_attuale',
                        'livello_cariera_attuale', 'ruolo_attuale', 'area_operativa_attuale', 'tipo_contratto_attuale',
                        'lavoro_passato', 'numero_attivita_svolte', 'mesi_attivita_svolte',
                        'descrizione_esperienza_pregressa', 'mansione_pregressa', 'livello_cariera_pregressa',
                        'ruolo_pregressa', 'area_operativa_pregressa', 'tipo_contratto_pregressa', 'mansione_futura',
                        'livello_cariera_futura', 'ruolo_futura', 'area_operativa_futura', 'tipo_contratto_futura',
                        'benefit', 'stipendio', 'interesse', 'possibilita_trasferirsi', 'data']
            filename ='studenti_risultati'

        elif int(kwargs['type']) == 1:
            survey = all_aziende()
            # nomi dei campi
            col_list = ['id', 'note', 'citta_sede', 'email', 'nome_referente', 'altra_sede', 'data']

            filename = 'aziende_risultati'

        elif int(kwargs['type']) == 2:
            survey = all_job()
            # nomi dei campi
            col_list = ['id', 'id_azienda', 'note_azienda', 'email_riferimento_azienda', 'email_riferimento_lavoro',
                        'citta_lavoro', 'lingua', 'campo_studi', 'esami', 'area_operativa', 'livello_cariera',
                        'tipo_contratto', 'distanza', 'note', 'data']

            filename = 'offerte_lavoro_risultati'

        else:
            logger.error("CSV vuoto, con kwargs vale:")
            logger.error(kwargs['type'])
            return redirect('index')

        # valori dei campi
        logger.error("CSV Inserisco liste vuote")

    except:
        logger.error("Problema nel CSV")


    filename = filename.replace(" ", "_")
    return export_csv_SJA(survey, col_list, filename + ".csv")


# da alcune info su un studente in maniera anonima
def infostd(id_student):
    student = {}

    try:# controllo che esista

        student_obj = Persona.objects.get(pk=id_student)
        # attributo singolo
        student["id"] = 'None'
        student['cap'] = 'None'
        student["anno"] = 'None'
        student['citta'] = 'None'
        student['voto'] = 'None'
        student['note'] = 'None'
        student['numero_attivita_svolte'] = 'None'
        student['mesi_attivita_svolte'] = 'None'
        student['descrizione_esperienza_pregressa'] = 'None'
        student['possibilita_trasferirsi'] = 'None'
        student['stipendio'] = 'None'

        #attributo singolo da chiave esterna
        student["zona"] = ''
        student['grado_studi'] =''
        student['livello_pc'] = ''

        # valori multipli da chiavi esterne
        student['esami'] = ''
        student['campo_studi'] = ''
        student['lingua'] = ''
        student['conoscenza_specifica'] = ''
        student['stato'] = ''
        student['mansione_attuale'] = ''
        student['livello_cariera_attuale'] = ''
        student['ruolo_attuale' ] = ''
        student['area_operativa_attuale'] = ''
        student['tipo_contratto_attuale'] = ''
        student['lavoro_passato'] = ''
        student['mansione_pregressa'] = ''
        student['livello_cariera_pregressa'] = ''
        student['ruolo_pregressa'] = ''
        student['area_operativa_pregressa'] = ''
        student['tipo_contratto_pregressa'] = ''
        student['mansione_futura'] = 'None'
        student['livello_cariera_futura'] = ''
        student['ruolo_futura'] = 'None'
        student['area_operativa_futura'] = ''
        student['tipo_contratto_futura'] = ''
        student['benefit'] = ''
        student['interesse'] = ''

        # valoriaziamo la lista
        if student_obj.id:
            student["id"] = student_obj.id
        if student_obj.cap:
            student['cap'] = student_obj.cap
        if student_obj.anno_nascita:
            student["anno"] = student_obj.anno_nascita
        if student_obj.citta:
            student['citta'] = student_obj.citta
        if student_obj.voto_finale:
            student['voto'] = student_obj.voto_finale
        if student_obj.note:
            student['note'] = student_obj.note
        if student_obj.numero_attivita_svolte:
            student['numero_attivita_svolte'] = student_obj.numero_attivita_svolte
        if student_obj.numero_mesi_attivita_svolte:
            student['mesi_attivita_svolte'] = student_obj.numero_mesi_attivita_svolte
        if student_obj.desc_esperienze_pregresse:
            student['descrizione_esperienza_pregressa'] = student_obj.desc_esperienze_pregresse
        if student_obj.possibilita_trasferirsi:
            student['possibilita_trasferirsi'] = student_obj.possibilita_trasferirsi
        if student_obj.stipendio_futuro:
            student['stipendio'] = student_obj.stipendio_futuro

        # chiavi esterne
        if student_obj.zona:
            student["zona"] = student_obj.zona.valore
        if student_obj.grado_studi:
            student['grado_studi'] = student_obj.grado_studi.valore
        if student_obj.livello_uso_computer:
            student['livello_pc'] = student_obj.livello_uso_computer.valore


        #valore attributi multi valore
        # esami
        list_esami = EsameAttuale.objects.filter(persona=id_student).select_related()
        for le in list_esami:
            if le.esame != None:
                if student['esami'] != "":
                    student['esami'] += "," + le.esame.valore
                else:
                    student['esami'] += le.esame.valore
            else:
                student['esami'] += "None"

        # lingua
        list_lingua = LinguaAttuale.objects.filter(persona=id_student).select_related()
        for ll in list_lingua:
            if ll.lingua != None:
                if student['lingua'] != "":
                    student['lingua'] += "," + ll.lingua.valore
                else:
                    student['lingua'] += ll.lingua.valore
            else:
                student['lingua'] += "None"

        # campo studi
        list_campo_studi = CampoStudiAttuale.objects.filter(persona=id_student).select_related()
        for lcs in list_campo_studi:
            if lcs.campo_studi != None:
                if student['campo_studi'] != "":
                    student['campo_studi'] += "," + lcs.campo_studi.valore
                else:
                    student['campo_studi'] += lcs.campo_studi.valore
            else:
                student['campo_studi'] += "None"

        # conoscenza_specifica
        list_conoscenza_specifica = ConoscenzaSpecificaAttuale.objects.filter(persona=id_student).select_related()
        for lcs in list_conoscenza_specifica:
            if lcs.conoscenza_specifica != None:
                if student['conoscenza_specifica'] != "":
                    student['conoscenza_specifica'] += "," + lcs.conoscenza_specifica.valore
                else:
                    student['conoscenza_specifica'] += lcs.conoscenza_specifica.valore
            else:
                student['conoscenza_specifica'] += "None"

        # stato
        list_stato = StatoAttuale.objects.filter(persona=id_student).select_related()
        for ls in list_stato:
            if ls.stato != None:
                if student['stato'] != "":
                    student['stato'] += "," + ls.stato.valore
                else:
                    student['stato'] += ls.stato.valore
            else:
                student['stato'] += "None"

        # mansione attuale
        list_mansione_attuale = MansioneAttuale.objects.filter(persona=id_student).select_related()
        for lma in list_mansione_attuale:
            if lma.mansione != None:
                if student['mansione_attuale'] != "":
                    student['mansione_attuale'] += "," + lma.mansione.valore
                else:
                    student['mansione_attuale'] += lma.mansione.valore
            else:
                student['mansione_attuale'] += "None"

        # mansione pregressa
        list_mansione_pregressa = MansionePregresso.objects.filter(persona=id_student).select_related()
        for lmp in list_mansione_pregressa:
            if lmp.mansione != None:
                if student['mansione_pregressa'] != "":
                    student['mansione_pregressa'] += "," + lmp.mansione.valore
                else:
                    student['mansione_pregressa'] += lmp.mansione.valore
            else:
                student['mansione_pregressa'] += "None"

        # mansione futura
        list_mansione_futura = MansioneFuturo.objects.filter(persona=id_student).select_related()
        for lmf in list_mansione_futura:
            if lmf.mansione != None:
                if student['mansione_futura'] != "":
                    student['mansione_futura'] += "," + lmf.mansione.valore
                else:
                    student['mansione_futura'] += lmf.mansione.valore
            else:
                student['mansione_futura'] += "None"

        # livello_cariera attuale
        list_livello_cariera_attuale = LivelloCarieraAttuale.objects.filter(persona=id_student).select_related()
        for llca in list_livello_cariera_attuale:
            if llca.livello_cariera != None:
                if student['livello_cariera_attuale'] != "":
                    student['livello_cariera_attuale'] += "," + llca.livello_cariera.valore
                else:
                    student['livello_cariera_attuale'] += llca.livello_cariera.valore
            else:
                student['livello_cariera_attuale'] += "None"

        # livello_cariera pregressa
        list_livello_cariera_pregressa = LivelloCarieraPregresso.objects.filter(persona=id_student).select_related()
        for llcp in list_livello_cariera_pregressa:
            if llcp.livello_cariera != None:
                if student['livello_cariera_pregressa'] != "":
                    student['livello_cariera_pregressa'] += "," + llcp.livello_cariera.valore
                else:
                    student['livello_cariera_pregressa'] += llcp.livello_cariera.valore
            else:
                student['livello_cariera_pregressa'] += "None"

        # livello_cariera futura
        list_livello_cariera_futura = LivelloCarieraFuturo.objects.filter(persona=id_student).select_related()
        for llcf in list_livello_cariera_futura:
            if llcf.livello_cariera != None:
                if student['livello_cariera_futura'] != "":
                    student['livello_cariera_futura'] += "," + llcf.livello_cariera.valore
                else:
                    student['livello_cariera_futura'] += llcf.livello_cariera.valore
            else:
                student['livello_cariera_futura'] += "None"

        # ruolo_attuale
        list_ruolo_attuale = RuoloAttuale.objects.filter(persona=id_student).select_related()
        for lra in list_ruolo_attuale:
            if lra.ruolo != None:
                if student['ruolo_attuale'] != "":
                    student['ruolo_attuale'] += "," + lra.ruolo.valore
                else:
                    student['ruolo_attuale'] += lra.ruolo.valore
            else:
                student['ruolo_attuale'] += "None"

        # ruolo pregressa
        list_ruolo_pregressa = RuoloPregresso.objects.filter(persona=id_student).select_related()
        for lrp in list_ruolo_pregressa:
            if lrp.ruolo != None:
                if student['ruolo_pregressa'] != "":
                    student['ruolo_pregressa'] += "," + lrp.ruolo.valore
                else:
                    student['ruolo_pregressa'] += lrp.ruolo.valore
            else:
                student['ruolo_pregressa'] += "None"

        # ruolo futura
        list_ruolo_futura = RuoloFuturo.objects.filter(persona=id_student).select_related()
        for lrf in list_ruolo_futura:
            if lrf.ruolo != None:
                if student['ruolo_futura'] != "":
                    student['ruolo_futura'] += "," + lrf.ruolo.valore
                else:
                    student['ruolo_futura'] += lrf.ruolo.valore
            else:
                student['ruolo_futura'] += "None"

        # area_operativa attuale
        list_area_operativa_attuale = AreaOperativaAttuale.objects.filter(persona=id_student).select_related()
        for laoa in list_area_operativa_attuale:
            if laoa.area_operativa != None:
                if student['area_operativa_attuale'] != "":
                    student['area_operativa_attuale'] += "," + laoa.area_operativa.valore
                else:
                    student['area_operativa_attuale'] += laoa.area_operativa.valore
            else:
                student['area_operativa_attuale'] += "None"

        # area_operativa pregressa
        list_area_operativa_pregressa = AreaOperativaPregresso.objects.filter(persona=id_student).select_related()
        for laop in list_area_operativa_pregressa:
            if laop.area_operativa != None:
                if student['area_operativa_pregressa'] != "":
                    student['area_operativa_pregressa'] += "," + laop.area_operativa.valore
                else:
                    student['area_operativa_pregressa'] += laop.area_operativa.valore
            else:
                student['area_operativa_pregressa'] += "None"

        # area_operativa futura
        list_area_operativa_futura = AreaOperativaFuturo.objects.filter(persona=id_student).select_related()
        for laof in list_area_operativa_futura:
            if laof.area_operativa != None:
                if student['area_operativa_futura'] != "":
                    student['area_operativa_futura'] += "," + laof.area_operativa.valore
                else:
                    student['area_operativa_futura'] += laof.area_operativa.valore
            else:
                student['area_operativa_futura'] += "None"

        # tipo_contratto attuale
        list_tipo_contratto_attuale = TipoContrattoAttuale.objects.filter(persona=id_student).select_related()
        for ltca in list_tipo_contratto_attuale:
            if ltca.tipo_contratto != None:
                if student['tipo_contratto_attuale'] != "":
                    student['tipo_contratto_attuale'] += "," + ltca.tipo_contratto.valore
                else:
                    student['tipo_contratto_attuale'] += ltca.tipo_contratto.valore
            else:
                student['tipo_contratto_attuale'] += "None"

        # tipo_contratto prgresso
        list_tipo_contratto_pregresso = TipoContrattoPregesso.objects.filter(persona=id_student).select_related()
        for ltcp in list_tipo_contratto_pregresso:
            if ltcp.tipo_contratto != None:
                if student['tipo_contratto_pregressa'] != "":
                    student['tipo_contratto_pregressa'] += "," + ltcp.tipo_contratto.valore
                else:
                    student['tipo_contratto_pregressa'] += ltcp.tipo_contratto.valore
            else:
                student['tipo_contratto_pregressa'] += "None"

        # tipo_contratto futura
        list_tipo_contratto_futura = TipoContrattoFuturo.objects.filter(persona=id_student).select_related()
        for ltcf in list_tipo_contratto_futura:
            if ltcf.tipo_contratto != None:
                if student['tipo_contratto_futura'] != "":
                    student['tipo_contratto_futura'] += "," + ltcf.tipo_contratto.valore
                else:
                    student['tipo_contratto_futura'] += ltcf.tipo_contratto.valore
            else:
                student['tipo_contratto_futura'] += "None"

        # benefit
        list_benefit = BenefitFuturo.objects.filter(persona=id_student).select_related()
        for lb in list_benefit:
            if lb.benefit != None:
                if student['benefit'] != "":
                    student['benefit'] += "," + lb.benefit.valore
                else:
                    student['benefit'] += lb.benefit.valore
            else:
                student['benefit'] += "None"

        # interesse
        list_interesse_futuro = InteresseFuturo.objects.filter(persona=id_student).select_related()
        for lif in list_interesse_futuro:
            if lif.interesse != None:
                if student['interesse'] != "":
                    student['interesse'] += "," + lif.interesse.valore
                else:
                    student['interesse'] += lif.interesse.valore
            else:
                student['interesse'] += "None"

    except ObjectDoesNotExist:
        logger.error("Info non possibili il Studente non esiste, ritorno None")
        return None

    return student



# da alcune info su un certo lavoro
def infojob(id_job):

    job={}
    job['id'] = 'None'
    job['id_azienda'] = 'None'
    job['citta_sede'] = 'None'
    job['citta_lavoro'] = ''
    job['lingua'] = ''
    job['campo_studi'] = ''
    job['esami'] = ''
    job['area_operativa'] = ''
    job['tipo_contratto'] = ''
    job['livello_cariera'] = ''
    job['distanza'] = 'None'

    try:# controllo che esista

        job_obj = Lavoro.objects.get(pk=id_job)

        if job_obj.id:
            job['id'] = job_obj.id
        if job_obj.azienda_id:
            job['id_azienda'] = job_obj.azienda_id
        if job_obj.azienda.citta_sede:
            job['citta_sede'] = job_obj.azienda.citta_sede.valore
        if job_obj.distanza_massima:
            job['distanza'] = job_obj.distanza_massima

        # attributi multivalore

        # citta lavoro
        list_citta_lavoro = CercaCitta.objects.filter(lavoro=id_job).select_related()
        for lcs in list_citta_lavoro:
            if lcs.citta is not None:
                if job['citta_lavoro'] != "":
                    job['citta_lavoro'] += "," + lcs.citta.valore
                else:
                    job['citta_lavoro'] += lcs.citta.valore
            else:
                job['citta_lavoro'] += "None"

        # lingua cerca lavoro
        list_lingua = CercaLingua.objects.filter(lavoro=id_job).select_related()
        for ll in list_lingua:
            if ll.lingua != None:
                if job['lingua'] != "":
                    job['lingua'] += "," + ll.lingua.valore
                else:
                    job['lingua'] += ll.lingua.valore
            else:
                job['lingua'] += "None"

        # campo studi cerca lavoro
        list_campo_studi = CercaCampoStudio.objects.filter(lavoro=id_job).select_related()
        for lcs in list_campo_studi:
            if lcs.campo_studio != None:
                if job['campo_studi'] != "":
                    job['campo_studi'] += "," + lcs.campo_studio.valore
                else:
                    job['campo_studi'] += lcs.campo_studio.valore
            else:
                job['campo_studi'] += "None"

        # esami cerca lavoro
        list_esami = CercaEsami.objects.filter(lavoro=id_job).select_related()
        for le in list_esami:
            if le.esame != None:
                if job['esami'] != "":
                    job['esami'] += "," + le.esame.valore
                else:
                    job['esami'] += le.esame.valore
            else:
                job['esami'] += "None"

        # area_operativa cerca lavoro
        list_area_operativa = CercaAreaOperativa.objects.filter(lavoro=id_job).select_related()
        for lao in list_area_operativa:
            if lao.area_operativa != None:
                if job['area_operativa'] != "":
                    job['area_operativa'] += "," + lao.area_operativa.valore
                else:
                    job['area_operativa'] += lao.area_operativa.valore
            else:
                job['area_operativa'] += "None"

        # livello_cariera cerca lavoro
        list_livello_cariera = CercaLivelloCariera.objects.filter(lavoro=id_job).select_related()
        for llc in list_livello_cariera:
            if llc.livello_cariera != None:
                if job['livello_cariera'] != "":
                    job['livello_cariera'] += "," + llc.livello_cariera.valore
                else:
                    job['livello_cariera'] += llc.livello_cariera.valore
            else:
                job['livello_cariera'] += "None"

        # tipo_contratto cerca lavoro
        list_tipo_contratto = CercaTipoContratto.objects.filter(lavoro=id_job).select_related()
        for ltc in list_tipo_contratto:
            if ltc.tipo_contratto != None:
                if job['tipo_contratto'] != "":
                    job['tipo_contratto'] += "," + ltc.tipo_contratto.valore
                else:
                    job['tipo_contratto'] += ltc.tipo_contratto.valore
            else:
                job['tipo_contratto'] += "None"

    except ObjectDoesNotExist:
        logger.error("Info non possibili il lavoro non esiste, ritorno None")
        return None

    return job

# Parte di raccomandazione
class RecomStudente(View):

    # solo se autenticato come admin o utente
    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):

        # carico i dati di ogni offerta di lavoro, ma solo alcune info per mantenere anonimato
        # bisogna creare una funzione che passa i 5 valori necessari. La funzione deve dipendere dal Account collegato
        result = {0: infojob(23), 1: infojob(13), 2: infojob(14), 4: infojob(15), 5: infojob(16)}

        return render(request, "recommendation_student.html", {"result": result})

    # solo se autenticato come admin o utente Azienda
    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):

        return render(request, 'recommendation_student.html')

# Parte di Correlazione
class CorrelationStudente(View):

    # solo se autenticato come admin o utente
    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        # passato un id da request restituisco l'utente piu correlato con il prodotto scalare
        students={}
        #tutti gli studenti tranne quello interessato
        students = Persona.objects.filter(~Q(id=kwargs['id']))
        score = -1
        tmp = 0
        similar_std_id = kwargs['id']
        for s in students:
            tmp = stud_prodotto_scalare(kwargs['id'], s.id)
            if(tmp>score):
                score = tmp
                similar_std_id = s.id
        result = {0: infostd(similar_std_id)}

        return render(request, "similar_student.html", {"result": result})

    # solo se autenticato come admin o utente Azienda
    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):

        return render(request, 'similar_student.html')