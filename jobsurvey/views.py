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

# for ajax json
from django.http import QueryDict

# for random
import random
import string

# import the logging library #per debug scrive nella Console
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


# per sondaggio
class Studenti(View):

    def get(self, request, *args, **kwargs):

        # controllo errori per registrazione
        error = None
        if 'error' in request.GET:
            error = request.GET['error']
        result = None
        if 'result' in request.GET:
            result = request.GET['result']
        c = {'error': error, 'result': result}
        c.update(csrf(request))

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

        if 'id' in kwargs:
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

        result["copy"] = copy

        return render(request, "studenti.html", result)

    def post(self, request, *args, **kwargs):
        #logger.error("la post! ")

        # nuovo sondaggio quindi creo account
        post = request.POST

        #creo utente nuovo
        new_user=None
        if not request.user.is_authenticated():
            username = None
            password = None
            name = None

            if request.POST['email']== "":
                return render(request, 'studenti.html', {"error": 'No email inserita'})

            # problema se la mail facoltativa
            name = post['email']
            username = post['email']
            password = gen_password()
            user_count = Account.objects.filter(username=username).count()
            if user_count != 0:
                return render(request, 'studenti.html', {"error": 'Email gia esistente'})
            nuovo_user = Account(is_active=False, first_name=name, username=username, email=post['email'])
            nuovo_user.set_password(password)
            nuovo_user.activationCode = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            nuovo_user.save()

            # invio mail
            send_verification_email(request, nuovo_user, False, password)

        #stampa tutti valori della post
        '''
        for key in request.POST:
            logger.error(key)
            logger.error("value "+request.POST[key])
        '''

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
        #collego account al sondaggio
        if not request.user.is_authenticated:
            # nuovo utente
            new_user.survey = nuova_persona
            new_user.save()
        elif request.user.account.type==0:
            update_usr = Account.objects.get(pk=request.user.id)
            # cancello vecchio sondaggio
            old_survey = Persona.objects.get(pk=update_usr.survey_id)
            old_survey.delete()
            # aggiorno utente
            update_usr.survey = nuova_persona
            update_usr.save()
        else:
            logger.error("admin modifica persona studente")
            # un admin che fa modifiche
            #ATTENZIONE SE SI CAMBIA con una post l'id del vecchio sondaggio esplode tutto
            # non conosciamo l'identita dell'utene quindi dobbiamo leggerlo dalla POST
            #per l'utente non lo facciamo salta la sicurezza
            old_survey = Persona.objects.get(pk=request.POST["id_survey"])
            update_usr = Account.objects.get(old_survey)
            update_usr.survey = nuova_persona
            update_usr.save()
            old_survey.delete()


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

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        result = {}
        result['citta'] = Citta.objects.all()

        # per creare copie uso url GET
        copy = {}
        copy['id'] = ""
        copy['email'] = ""
        copy['citta'] = ""
        copy['altra_sede'] = ""
        copy['note'] = ""
        copy['nome_referente'] = ""

        if 'id' in kwargs:
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

        return render(request, "aziende.html", result)

    @method_decorator(login_required(login_url='log_in'))
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

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        result = {}
        result['lingua'] = Lingua.objects.all()
        result['campo_studi'] = CampoStudi.objects.all()
        result['esame'] = Esame.objects.all()
        result['livello_cariera'] = LivelloCariera.objects.all()
        result['area_operativa'] = AreaOperativa.objects.all()
        result['tipo_contratto'] = TipoContratto.objects.all()
        result['citta'] = Citta.objects.all()

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


class RisultatiAziende(View):

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):

        result={}
        # aziende
        list_aziende = Azienda.objects.all().select_related()

        # altra sede
        list_altra_sede = AltraSede.objects.all().select_related()

        for a in list_aziende:
            if a.citta_sede != None:
                citta_sede= a.citta_sede.valore
            else:
                citta_sede = "None"
            result[a.id] = {'id': a.id, 'note': a.note, 'citta_sede': citta_sede, 'email': a.email,
                            "nome_referente":  a.nome_referente, 'altra_sede': "", 'data': a.pub_date}

        for las in list_altra_sede:
            if las.citta != None:
                if result[las.azienda.id]['altra_sede'] != "":
                    result[las.azienda.id]['altra_sede'] += ","+las.citta.valore
                else:
                    result[las.azienda.id]['altra_sede'] += las.citta.valore
            else:
                result[las.azienda.id]['altra_sede'] += "None"

        return render(request, "risultati.html", {"result": result, "type": 1})

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
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

class RisultatiOffertaLavoro(View):
    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):

        result={}
        # lavori
        list_lavori = Lavoro.objects.all().select_related()

        for l in list_lavori:

            result[l.id] = {"id": l.id, 'id_azienda': l.azienda_id,
                            'note_azienda': l.azienda.note,"email_riferimento_azienda": l.azienda.email ,
                            'email_riferimento_lavoro': l.email_referente, "citta_lavoro":  "", 'lingua': "",
                            'campo_studi': "", 'esami': "", 'area_operativa': "", 'livello_cariera': "",
                            'tipo_contratto': "", 'distanza': l.distanza_massima, 'note': l.note_lavoro,
                            'data': l.pub_date}

        # citta lavoro
        list_citta_lavoro = CercaCitta.objects.all().select_related()
        for lcs in list_citta_lavoro:
            if lcs.citta != None:
                if result[lcs.lavoro.id]['citta_lavoro'] != "":
                    result[lcs.lavoro.id]['citta_lavoro'] += ","+lcs.citta.valore
                else:
                    result[lcs.lavoro.id]['citta_lavoro'] += lcs.citta.valore
            else:
                result[lcs.lavoro.id]['citta_lavoro'] += "None"

        # lingua cerca lavoro
        list_lingua = CercaLingua.objects.all().select_related()
        for ll in list_lingua:
            if ll.lingua != None:
                if result[ll.lavoro.id]['lingua'] != "":
                    result[ll.lavoro.id]['lingua'] += ","+ll.lingua.valore
                else:
                    result[ll.lavoro.id]['lingua'] += ll.lingua.valore
            else:
                result[ll.lavoro.id]['lingua'] += "None"

        # campo studi cerca lavoro
        list_campo_studi = CercaCampoStudio.objects.all().select_related()
        for lcs in list_campo_studi:
            if lcs.campo_studio != None:
                if result[lcs.lavoro.id]['campo_studi'] != "":
                    result[lcs.lavoro.id]['campo_studi'] += ","+lcs.campo_studio.valore
                else:
                    result[lcs.lavoro.id]['campo_studi'] += lcs.campo_studio.valore
            else:
                result[lcs.lavoro.id]['campo_studi'] += "None"

        # esami cerca lavoro
        list_esami = CercaEsami.objects.all().select_related()
        for le in list_esami:
            if le.esame != None:
                if result[le.lavoro.id]['esami'] != "":
                    result[le.lavoro.id]['esami'] += ","+le.esame.valore
                else:
                    result[le.lavoro.id]['esami'] += le.esame.valore
            else:
                result[le.lavoro.id]['esami'] += "None"

        # area_operativa cerca lavoro
        list_area_operativa = CercaAreaOperativa.objects.all().select_related()
        for lao in list_area_operativa:
            if lao.area_operativa != None:
                if result[lao.lavoro.id]['area_operativa'] != "":
                    result[lao.lavoro.id]['area_operativa'] += ","+lao.area_operativa.valore
                else:
                    result[lao.lavoro.id]['area_operativa'] += lao.area_operativa.valore
            else:
                result[lao.lavoro.id]['area_operativa'] += "None"

        # livello_cariera cerca lavoro
        list_livello_cariera = CercaLivelloCariera.objects.all().select_related()
        for llc in list_livello_cariera:
            if llc.livello_cariera != None:
                if result[llc.lavoro.id]['livello_cariera'] != "":
                    result[llc.lavoro.id]['livello_cariera'] += ","+llc.livello_cariera.valore
                else:
                    result[llc.lavoro.id]['livello_cariera'] += llc.livello_cariera.valore
            else:
                result[llc.lavoro.id]['livello_cariera'] += "None"

        # tipo_contratto cerca lavoro
        list_tipo_contratto = CercaTipoContratto.objects.all().select_related()
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


class RisultatiStudenti(View):

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):

        result={}
        # studenti
        list_studenti = Persona.objects.all().select_related()

        # chiavi esterne
        # Zona
        list_zona = Zona.objects.all().select_related()
        # Zona
        list_conoscenza_pc = LivelloPC.objects.all().select_related()

        for s in list_studenti:

            zona_tmp="None"
            if s.zona != None:
                zona_tmp = s.zona.valore
            grado_studi_tmp="None"
            if s.grado_studi != None:
                grado_studi_tmp = s.grado_studi.valore
            livello_uso_computer_tmp="None"
            if s.livello_uso_computer != None:
                livello_uso_computer_tmp = s.livello_uso_computer.valore

            result[s.id] = {"id": s.id, 'cap': s.cap,
                            'email': s.email, "anno": s.anno_nascita, 'citta': s.citta, "zona":  zona_tmp,
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
                            'stipendio': s.stipendio_futuro, 'interesse': "",'possibilita_trasferirsi': s.possibilita_trasferirsi,
                            'data': s.pub_date}

        # esami
        list_esami = EsameAttuale.objects.all().select_related()
        for le in list_esami:
            if le.esame != None:
                if result[le.persona.id]['esami'] != "":
                    result[le.persona.id]['esami'] += ","+le.esame.valore
                else:
                    result[le.persona.id]['esami'] += le.esame.valore
            else:
                result[le.persona.id]['esami'] += "None"

       # lingua
        list_lingua = LinguaAttuale.objects.all().select_related()
        for ll in list_lingua:
            if ll.lingua != None:
                if result[ll.persona.id]['lingua'] != "":
                    result[ll.persona.id]['lingua'] += ","+ll.lingua.valore
                else:
                    result[ll.persona.id]['lingua'] += ll.lingua.valore
            else:
                result[ll.persona.id]['lingua'] += "None"

        # campo studi
        list_campo_studi = CampoStudiAttuale.objects.all().select_related()
        for lcs in list_campo_studi:
            if lcs.campo_studi != None:
                if result[lcs.persona.id]['campo_studi'] != "":
                    result[lcs.persona.id]['campo_studi'] += ","+lcs.campo_studi.valore
                else:
                    result[lcs.persona.id]['campo_studi'] += lcs.campo_studi.valore
            else:
                result[lcs.persona.id]['campo_studi'] += "None"

        # conoscenza_specifica
        list_conoscenza_specifica = ConoscenzaSpecificaAttuale.objects.all().select_related()
        for lcs in list_conoscenza_specifica:
            if lcs.conoscenza_specifica != None:
                if result[lcs.persona.id]['conoscenza_specifica'] != "":
                    result[lcs.persona.id]['conoscenza_specifica'] += ","+lcs.conoscenza_specifica.valore
                else:
                    result[lcs.persona.id]['conoscenza_specifica'] += lcs.conoscenza_specifica.valore
            else:
                result[lcs.persona.id]['conoscenza_specifica'] += "None"


        # stato
        list_stato = StatoAttuale.objects.all().select_related()
        for ls in list_stato:
            if ls.stato != None:
                if result[ls.persona.id]['stato'] != "":
                    result[ls.persona.id]['stato'] += ","+ls.stato.valore
                else:
                    result[ls.persona.id]['stato'] += ls.stato.valore
            else:
                result[ls.persona.id]['stato'] += "None"


        # mansione attuale
        list_mansione_attuale = MansioneAttuale.objects.all().select_related()
        for lma in list_mansione_attuale:
            if lma.mansione != None:
                if result[lma.persona.id]['mansione_attuale'] != "":
                    result[lma.persona.id]['mansione_attuale'] += ","+lma.mansione.valore
                else:
                    result[lma.persona.id]['mansione_attuale'] += lma.mansione.valore
            else:
                result[lma.persona.id]['mansione_attuale'] += "None"
        # mansione pregressa
        list_mansione_pregressa = MansionePregresso.objects.all().select_related()
        for lmp in list_mansione_pregressa:
            if lmp.mansione != None:
                if result[lmp.persona.id]['mansione_pregressa'] != "":
                    result[lmp.persona.id]['mansione_pregressa'] += ","+lmp.mansione.valore
                else:
                    result[lmp.persona.id]['mansione_pregressa'] += lmp.mansione.valore
            else:
                result[lmp.persona.id]['mansione_pregressa'] += "None"
        # mansione futura
        list_mansione_futura = MansioneFuturo.objects.all().select_related()
        for lmf in list_mansione_futura:
            if lmf.mansione != None:
                if result[lmf.persona.id]['mansione_futura'] != "":
                    result[lmf.persona.id]['mansione_futura'] += ","+lmf.mansione.valore
                else:
                    result[lmf.persona.id]['mansione_futura'] += lmf.mansione.valore
            else:
                result[lmf.persona.id]['mansione_futura'] += "None"


        # livello_cariera attuale
        list_livello_cariera_attuale = LivelloCarieraAttuale.objects.all().select_related()
        for llca in list_livello_cariera_attuale:
            if llca.livello_cariera != None:
                if result[llca.persona.id]['livello_cariera_attuale'] != "":
                    result[llca.persona.id]['livello_cariera_attuale'] += ","+llca.livello_cariera.valore
                else:
                    result[llca.persona.id]['livello_cariera_attuale'] += llca.livello_cariera.valore
            else:
                result[llca.persona.id]['livello_cariera_attuale'] += "None"

        # livello_cariera pregressa
        list_livello_cariera_pregressa = LivelloCarieraPregresso.objects.all().select_related()
        for llcp in list_livello_cariera_pregressa:
            if llcp.livello_cariera != None:
                if result[llcp.persona.id]['livello_cariera_pregressa'] != "":
                    result[llcp.persona.id]['livello_cariera_pregressa'] += ","+llcp.livello_cariera.valore
                else:
                    result[llcp.persona.id]['livello_cariera_pregressa'] += llcp.livello_cariera.valore
            else:
                result[llcp.persona.id]['livello_cariera_pregressa'] += "None"

        # livello_cariera futura
        list_livello_cariera_futura = LivelloCarieraFuturo.objects.all().select_related()
        for llcf in list_livello_cariera_futura:
            if llcf.livello_cariera != None:
                if result[llcf.persona.id]['livello_cariera_futura'] != "":
                    result[llcf.persona.id]['livello_cariera_futura'] += ","+llcf.livello_cariera.valore
                else:
                    result[llcf.persona.id]['livello_cariera_futura'] += llcf.livello_cariera.valore
            else:
                result[llcf.persona.id]['livello_cariera_futura'] += "None"

        # ruolo_attuale
        list_ruolo_attuale = RuoloAttuale.objects.all().select_related()
        for lra in list_ruolo_attuale:
            if lra.ruolo != None:
                if result[lra.persona.id]['ruolo_attuale'] != "":
                    result[lra.persona.id]['ruolo_attuale'] += ","+lra.ruolo.valore
                else:
                    result[lra.persona.id]['ruolo_attuale'] += lra.ruolo.valore
            else:
                result[lra.persona.id]['ruolo_attuale'] += "None"

        # ruolo pregressa
        list_ruolo_pregressa = RuoloPregresso.objects.all().select_related()
        for lrp in list_ruolo_pregressa:
            if lrp.ruolo != None:
                if result[lrp.persona.id]['ruolo_pregressa'] != "":
                    result[lrp.persona.id]['ruolo_pregressa'] += ","+lrp.ruolo.valore
                else:
                    result[lrp.persona.id]['ruolo_pregressa'] += lrp.ruolo.valore
            else:
                result[lrp.persona.id]['ruolo_pregressa'] += "None"

        # ruolo futura
        list_ruolo_futura = RuoloFuturo.objects.all().select_related()
        for lrf in list_ruolo_futura:
            if lrf.ruolo != None:
                if result[lrf.persona.id]['ruolo_futura'] != "":
                    result[lrf.persona.id]['ruolo_futura'] += ","+lrf.ruolo.valore
                else:
                    result[lrf.persona.id]['ruolo_futura'] += lrf.ruolo.valore
            else:
                result[lrf.persona.id]['ruolo_futura'] += "None"

        # area_operativa attuale
        list_area_operativa_attuale = AreaOperativaAttuale.objects.all().select_related()
        for laoa in list_area_operativa_attuale:
            if laoa.area_operativa != None:
                if result[laoa.persona.id]['area_operativa_attuale'] != "":
                    result[laoa.persona.id]['area_operativa_attuale'] += ","+laoa.area_operativa.valore
                else:
                    result[laoa.persona.id]['area_operativa_attuale'] += laoa.area_operativa.valore
            else:
                result[laoa.persona.id]['area_operativa_attuale'] += "None"

        # area_operativa pregressa
        list_area_operativa_pregressa = AreaOperativaPregresso.objects.all().select_related()
        for laop in list_area_operativa_pregressa:
            if laop.area_operativa != None:
                if result[laop.persona.id]['area_operativa_pregressa'] != "":
                    result[laop.persona.id]['area_operativa_pregressa'] += ","+laop.area_operativa.valore
                else:
                    result[laop.persona.id]['area_operativa_pregressa'] += laop.area_operativa.valore
            else:
                result[laop.persona.id]['area_operativa_pregressa'] += "None"

        # area_operativa futura
        list_area_operativa_futura = AreaOperativaFuturo.objects.all().select_related()
        for laof in list_area_operativa_futura:
            if laof.area_operativa != None:
                if result[laof.persona.id]['area_operativa_futura'] != "":
                    result[laof.persona.id]['area_operativa_futura'] += ","+laof.area_operativa.valore
                else:
                    result[laof.persona.id]['area_operativa_futura'] += laof.area_operativa.valore
            else:
                result[laof.persona.id]['area_operativa_futura'] += "None"

        # tipo_contratto attuale
        list_tipo_contratto_attuale = TipoContrattoAttuale.objects.all().select_related()
        for ltca in list_tipo_contratto_attuale:
            if ltca.tipo_contratto != None:
                if result[ltca.persona.id]['tipo_contratto_attuale'] != "":
                    result[ltca.persona.id]['tipo_contratto_attuale'] += ","+ltca.tipo_contratto.valore
                else:
                    result[ltca.persona.id]['tipo_contratto_attuale'] += ltca.tipo_contratto.valore
            else:
                result[ltca.persona.id]['tipo_contratto_attuale'] += "None"

        # tipo_contratto prgresso
        list_tipo_contratto_pregresso = TipoContrattoPregesso.objects.all().select_related()
        for ltcp in list_tipo_contratto_pregresso:
            if ltcp.tipo_contratto != None:
                if result[ltcp.persona.id]['tipo_contratto_pregressa'] != "":
                    result[ltcp.persona.id]['tipo_contratto_pregressa'] += ","+ltcp.tipo_contratto.valore
                else:
                    result[ltcp.persona.id]['tipo_contratto_pregressa'] += ltcp.tipo_contratto.valore
            else:
                result[ltcp.persona.id]['tipo_contratto_pregressa'] += "None"

        # tipo_contratto futura
        list_tipo_contratto_futura = TipoContrattoFuturo.objects.all().select_related()
        for ltcf in list_tipo_contratto_futura:
            if ltcf.tipo_contratto != None:
                if result[ltcf.persona.id]['tipo_contratto_futura'] != "":
                    result[ltcf.persona.id]['tipo_contratto_futura'] += ","+ltcf.tipo_contratto.valore
                else:
                    result[ltcf.persona.id]['tipo_contratto_futura'] += ltcf.tipo_contratto.valore
            else:
                result[ltcf.persona.id]['tipo_contratto_futura'] += "None"

        # benefit
        list_benefit = BenefitFuturo.objects.all().select_related()
        for lb in list_benefit:
            if lb.benefit != None:
                if result[lb.persona.id]['benefit'] != "":
                    result[lb.persona.id]['benefit'] += ","+lb.benefit.valore
                else:
                    result[lb.persona.id]['benefit'] += lb.benefit.valore
            else:
                result[lb.persona.id]['benefit'] += "None"

        # interesse
        list_interesse_futuro = InteresseFuturo.objects.all().select_related()
        for lif in list_interesse_futuro:
            if lif.interesse != None:
                if result[lif.persona.id]['interesse'] != "":
                    result[lif.persona.id]['interesse'] += ","+lif.interesse.valore
                else:
                    result[lif.persona.id]['interesse'] += lif.interesse.valore
            else:
                result[lif.persona.id]['interesse'] += "None"

        return render(request, "risultati.html", {"result": result, "type": 0})

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
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

