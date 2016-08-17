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


# login
class AuthLogin(View):
    method_decorator(csrf_protect)
    def get(self, request):
        c = {}
       #c.update(csrf(request)) #deprecato
        return render(request, 'log_in.html', c)

    def post(self, request):
        logger.error("username! ")
        logger.error(request.POST['usr'])
        if 'usr' in request.POST:
            user = authenticate(username=request.POST['usr'], password=request.POST['password'])
        else:
            return JsonResponse({'success': False})

        if user:
            login(request, user)
            # return redirect('index')
            return JsonResponse({'success': True})
        else:
            # return redirect('login')
            return JsonResponse({'success': False})

# signup
class SignUp(View):
    method_decorator(csrf_protect)
    def get(self, request):
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


# log out
def log_out(request):
    logout(request)
    return redirect('index')

# attivazione account
def verification(request, id, str):
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

# Index Page.
class Index(View):

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
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
        return render(request, 'index.html')


# Create New Survey
class NewSurvey(View):

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        return render(request, 'new_survey.html')

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):

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


# Preview Survey
class PreviewSurvey(View):

    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
        id_survey = None
        if 'id' in kwargs:
            id_survey = kwargs['id']
        survey = Column.objects.filter(survey=id_survey)
        return render(request, 'preview_survey.html', {"survey": json_form_in_html(survey)})

    @method_decorator(login_required(login_url='log_in'))
    def post(self, request, *args, **kwargs):
        return render(request, 'preview_survey.html')


# Make Survey
# after survey its important to log out for secure issues
class MakeSurvey(View):

    def get(self, request, *args, **kwargs):
        id_survey = None
        if 'id' in kwargs:
            id_survey = kwargs['id']
        survey = Column.objects.filter(survey=id_survey)
        return render(request, 'make_survey.html', {"survey": json_form_in_html(survey), "id": kwargs['id'], "thank": 0})

    def post(self, request, *args, **kwargs):
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


# Result of Survey
class ResultSurvey(View):
    @method_decorator(login_required(login_url='log_in'))
    def get(self, request, *args, **kwargs):
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
        return render(request, 'result.html')


def result_download(request, type, survey_id):
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
