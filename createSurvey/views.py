from django.http import HttpResponse

#from django.core.context_processors import csrf #deprecato...
from django.views.decorators.csrf import csrf_protect

# from django.shortcuts import render, redirect, render_to_response, RequestContext # da errore Request Context
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View
from .models import Column, Survey, Interview, Result, Account

# for login
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User

# check if login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

# for list of items in a page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# for timezone ed il resto
from datetime import date
import datetime
import time
from django.utils import timezone, dateparse


# for Json format
import json

# for utility
from createSurvey.utils import *

# import the logging library #per debug scrive nella Console
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# server per lo sleep
import time



class AuthLogin(View):
    '''
    Classe per permettere autenticazione dell'utente
    Utilizzare per gestire login
    '''
    method_decorator(csrf_protect)

    def get(self, request):
        '''
        Funzione per gestire le richieste GET sul template log_in.html
        '''
        c = {}
       #c.update(csrf(request)) #deprecato
        return render(request, 'log_in.html', c)

    def post(self, request):
        '''
        Funzione per gestire le richieste POST sul template log_in.html
        '''
        logger.error("username! ")
        logger.error(request.POST['usr'])
        logger.error(request.POST['password'])
        if 'usr' in request.POST:
            user = authenticate(username=request.POST['usr'], password=request.POST['password'])
        else:
            logger.error("errore login 1 ")
            return JsonResponse({'success': False})

        if user:
            login(request, user)
            # return redirect('index')
            return JsonResponse({'success': True})
        else:
            # return redirect('login')
            logger.error("errore login 2 ")
            return JsonResponse({'success': False})


class SignUp(View):
    '''
    Classe per gestire la registrazione di nuovi utenti
    '''
    method_decorator(csrf_protect)

    def get(self, request):
        '''
        Funzione per gestire le richieste GET sul template sign_up.html
        '''
        error = None
        if 'error' in request.GET:
            error = request.GET['error']
        result = None
        if 'result' in request.GET:
            result = request.GET['result']
        c = {'error': error, 'result': result}
        #c.update(csrf(request)) #deprecato
        return render(request, 'sign_up.html', c)

    def post(self, request):
        '''
        Funzione per gestire le richieste POST sul template sign_up.html
        '''
        post = request.POST
        username = None
        password = None
        name = None

        name = post['name']
        username = post['username']
        password = post["password"]
        user_count = User.objects.filter(username=username).count()
        if user_count != 0:
            return redirect('sign_up', error='email esistente')
        if post["password"].strip() == "" or post["password"] != post["password2"]:
            return redirect('sign_up', error='password non adatta')
        user = User(is_active=True, first_name=name, username=post['username'])
        user.set_password(post['password'])
        user.save()
        auth = authenticate(username=username, password=password)
        login(request, auth)
        return redirect('index')



def log_out(request):
    '''
    Funzione per deautenticare un utente dal portale
    '''
    logout(request)
    return redirect('index')



def verification(request, id, str):
    '''
    Funzione per gestire il codice di attivazione di un Accounnt
    '''
    user = None
    try:
        user = Account.objects.get(user_ptr_id=id)
    except:
        pass
    if user and user.activationCode == str:
        user.is_active = True
        user.save()
        return render(request, 'verification.html', {'msg': 'activated'})

    time.sleep(2)
    return render(request, 'verification.html', {'msg': 'Errore'})


class Index(View):
    '''
    Classe per la gestione della pagina principale dove è presente un menu di navigazione
    '''

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        '''
        Funzione per gestire le richieste GET sul template index.html
        Prima versione del portale vnivano gestiti sondaggi di qualsiasi tipo
        Dovra essere rimossa o modificata
        '''
        survey_list = Survey.objects.all()
        paginator = Paginator(survey_list, 15)
        page = request.GET.get('page')
        try:
             surveys = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
             surveys = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
             surveys = paginator.page(paginator.num_pages)

        return render(request, "index.html", {"surveys":  surveys})


    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
        '''
        Funzione per gestire le richieste POST sul template index.html
        '''
        return render(request, 'index.html')



class NewSurvey(View):
    '''
    Classe per la gestione della generazioen di nuovi sondaggi
    '''

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        '''
        Funzione per la gestione delle richieste GET su creazione nuovi sondaggi
        '''
        return render(request, 'new_survey.html')


    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
        '''
        Funzione per la gestione delle richieste POST su creazione nuovi sondaggi
        Questo modo di fare è superato e deve essere rimosso o modificato
        Non è piu necessario creare nuovi sondaggi
        '''
        # recupero le informazioni arrivate tramite POST
        title_survey = request.POST["title_survey"]
        desc_survey = request.POST["desc_survey"]
        data = json.loads(request.POST["data"])

        new_survey = Survey(name=title_survey, note=desc_survey)
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



class PreviewSurvey(View):
    '''
    Classe per la gestione la visulaizzazione dei sondaggi, vecchio modo di gestire il portale
    Deve essere rimosso o modificato
    '''

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        '''
        Funzione per gestire le richieste GET per visualizzare i risultati dei sondaggi
        '''
        id_survey = None
        if 'id' in kwargs:
            id_survey = kwargs['id']
        survey = Column.objects.filter(survey=id_survey)
        return render(request, 'preview_survey.html', {"survey": json_form_in_html(survey)})

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
        '''
        Funzione per gestire le richieste POST per visualizzare i risultati dei sondaggi
        '''
        return render(request, 'preview_survey.html')



class MakeSurvey(View):
    '''
    Classe per fare un sondaggio, attenzione importante effettuare il log out da amministratore prima di svolgere un sondaggio
    per motivi di sicurezza
    Deve essere rimosso o modificato, vecchio modo di fare sondaggi
    '''

    def get(self, request, *args, **kwargs):
        '''
        Funzione per gestire le richieste GET per effettuare un sondaggio
        '''
        id_survey = None
        if 'id' in kwargs:
            id_survey = kwargs['id']
        survey = Column.objects.filter(survey=id_survey)
        return render(request, 'make_survey.html', {"survey": json_form_in_html(survey), "id": kwargs['id'], "thank": 0})

    def post(self, request, *args, **kwargs):
        '''
        Funzione per gestire le richieste POST per effettuare un sondaggio
        '''
        new_interview = Interview(name_user="anonymous", type_user="people")
        new_interview.save()
        for key in request.POST:
            if key != "csrfmiddlewaretoken":
                the_col = Column.objects.filter(id=int(key))
                if len(the_col) == 1:
                    list_value = request.POST.getlist(key)[0]
                    if len(request.POST.getlist(key)) > 1:
                        for i, val in enumerate(request.POST.getlist(key)):
                            if i != 0:
                                list_value += ","+val
                        new_result = Result(value=list_value, interview=new_interview, column=the_col[0])
                        new_result.type_value = "list"
                    else:
                        new_result = Result(value=list_value, interview=new_interview, column=the_col[0])
                        new_result.type_value = "single"
                    new_result.save()
                else:
                    return render(request, 'make_survey.html', {'errore':"dati inseriti non validi"})
        return render(request, 'make_survey.html', {"id": kwargs['id'], "thank": 1})



class ResultSurvey(View):
    '''
    Classe per vedere i risultati di un sondaggio
    Deve essere rimosso o modificato, vecchio modo di fare sondaggi
    '''

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        '''
        Funzione per gestire le richieste GET per leggere risultati di un sondaggio
        '''
        id_survey = None
        if 'id' in kwargs:
            id_survey = kwargs['id']
        col_list = Column.objects.filter(survey_id=id_survey)
        result_list = []
        final_list = []
        for col in col_list:
            result_list.append(Result.objects.filter(column=col))
        for i in range(0, len(result_list[0])):
            final_list.append([])
        for val in result_list:
            for i in range(0, len(result_list[0])):
                final_list[i].append(val[i])
        return render(request, 'result.html', {"columns": col_list, "results":  final_list})

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
        '''
        Funzione per gestire le richieste POST per leggere risultati di un sondaggio
        '''
        return render(request, 'result.html')



def result_download(request, type, survey_id):
    '''
    Funzione i download con i risultati di un sondaggio
    Vecchio modo di fare va tolto o modificato
    '''
    try:
        survey = Survey.objects.get(id=survey_id)
        col_list = Column.objects.filter(survey_id=survey_id)
        result_list = []
        final_list = []
        for col in col_list:
            result_list.append(Result.objects.filter(column=col))
        for i in range(0, len(result_list[0])):
            final_list.append([])
        for val in result_list:
            for i in range(0, len(result_list[0])):
                final_list[i].append(val[i])
    except:
        return redirect('index')

    filename = survey.name
    filename = filename.replace(" ", "_")
    return export_csv(survey, col_list, final_list, filename + ".csv")




class Lost_password(View):
    '''
    Classe per gestire la richiesta di una nuova password dopo aver smarrito la precedetne
    '''

    def get(self, request, *args, **kwargs):
        '''
        Per gestire le richieste di GET sulla pagina della richiesta password smarrita
        '''
        error = None
        if 'error' in request.GET:
            error = request.GET['error']
        result = None
        if 'result' in request.GET:
            result = request.GET['result']

        return render(request, 'lost_password.html', {'error': error, 'result': result})

    def post(self, request, *args, **kwargs):
        '''
        Per gestire le richieste di POST sulla pagina della richiesta password smarrita
        '''
        if 'mailReset' in request.POST:
            account = None
            try:
                account = Account.objects.get(email=request.POST["mailReset"])
            except:
                return custom_redirect('lost_password', error='mail non valida')
            if account:
                account.activationCode = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
                account.timeCode = datetime.datetime.now(tz=timezone.get_default_timezone()) + datetime.timedelta(hours=1)
                account.save()
                # send verification email
                send_reset_pass_email(request, account)
                return custom_redirect('lost_password', result='Reset inviato sulla mail hai tempo una sola ora per cambiare')
        return custom_redirect('lost_password', error='mail non valida')



class Reset_password(View):
    '''
    Classe che permette di resettare la password di un account dopo aver controllato un link con codice di verifica
    '''
    def get(self, request, *args, **kwargs):
        '''
        Per gestire le richieste di GET sulla di reset dela password
        '''
        return render(request, 'reset_password.html', {"code": kwargs['str'], "id": kwargs['id']})



    def post(self, request, *args, **kwargs):
        '''
        Per gestire le richieste di POST sulla di reset dela password
        '''
        if 'id' in request.POST:
            u = User.objects.get(id=request.POST['id'])
            account = Account.objects.get(user_ptr_id=request.POST['id'])
            if account.timeCode > datetime.datetime.now(tz=timezone.get_default_timezone()):
                if 'newPassword' in request.POST:
                    account.timeCode = datetime.datetime.now(tz=timezone.get_default_timezone())
                    u.set_password(request.POST['newPassword'])
                    u.save()
                else:
                    return custom_redirect('reset_password', error='Nuova password non valida')
            else:
                 return custom_redirect('reset_password', error='Tempo Scaduto')
        else:
            return custom_redirect('change_password', error='Id non valido')
        user = authenticate(username=u, password=request.POST['newPassword'])
        if user:
            login(request, user)
            return custom_redirect('change_password', result='Password cambiata')
        else:
            return redirect('index')
        return redirect('reset_password')



class Change_password(View):
    '''
    Classe che permette di il cambio della password di un utente
    '''

    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):
        '''
        Per gestire le richieste di GET sulla pagina di cambio della password
        '''
        error = None
        if 'error' in request.GET:
            error = request.GET['error']
        result = None
        if 'result' in request.GET:
            result = request.GET['result']
        code = None
        if 'code' in request.GET:
            code = request.GET['code']
        return render(request, 'change_password.html', {'code': code, 'error': error, 'result': result})

    @method_decorator(login_required(login_url='login'))
    def post(self, request, *args, **kwargs):
        '''
        Per gestire le richieste di POST sulla pagina di cambio della password
        '''
        if 'oldPassword' in request.POST:
            u = User.objects.get(id=request.user.id)
            email = request.user.email
            if u.check_password(request.POST['oldPassword']):
                if 'newPassword' in request.POST:
                    u.set_password(request.POST['newPassword'])
                    u.save()
                else:
                    return custom_redirect('change_password', error='Nuova password non valida')
            else:
                return custom_redirect('change_password', error='Vecchia password errata')
        else:
            return custom_redirect('change_password', error='Vecchia password non presente')

        user = authenticate(username=email, password=request.POST['newPassword'])
        if user:
            login(request, user)
            return custom_redirect('change_password', result='Password cambiata')
        else:
            return redirect('index')
