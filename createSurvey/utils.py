from .models import Column, Survey

# per custom redirect
import urllib
import requests
from django.http import HttpResponseRedirect


# for Json format
import json

# For export .SCV
import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str

# per prendere il path
from django.conf import settings

# import the logging library #per debug scrive nella Console
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# per la mail di verifica
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

def json_form_in_html(survey):
    '''
    trasforma un Json in una form HTML srve nella prima versione del programma, ora obsoleta
    :param survey: passare un oggetto contenente il risultato di un sondaggio
    :return: ritorna una forma HTML con i risultati
    '''

    form = dict()
    for col in survey:
        min = ""
        max = ""
        desc = ""
        required = ""
        #logger.error(col.option)
        #logger.error("col option= "+str(type(col.option)))

        #funziona
        json_acceptable_string = col.option.replace("True", "'True'")
        json_acceptable_string = json_acceptable_string.replace("False", "'False'")
        json_acceptable_string = json_acceptable_string.replace("'", "\"")
        options = json.loads(json_acceptable_string)
        html = '<label class="" for="'+str(col.id)+'">'+col.label+'</label>'
        if col.required:
            required = " required "
        if col.type == "text" or col.type == "number":
            if "minlength" in options:
                min = 'min="'+options["minlength"]+'" '
            elif "min" in options:
                min = 'min="'+options["min"]+'" '
            if "maxlength" in options:
                max = 'max="'+options["maxlength"]+'" '
            elif "max" in options:
                max = 'max="'+options["max"]+'" '
            if "description" in options:
                desc = '<span class="help-block">'+options["description"]+'</span>'
            html += '<input type="'+col.type+'" id="'+str(col.id)+'" name="'+str(col.id)+'" class="form-control" '+min+max+' '+required+' ></input>'+desc
        elif col.type == "checkboxes":
            for box in options["options"]:
                html +='<div class="checkbox"><label><input type="checkbox" value="'+box["label"]+'" id="'+str(col.id)+'" name="'+str(col.id)+'">'+box["label"]+'</label></div>'
        elif col.type == "radio":
            for box in options["options"]:
                html +='<div class="radio"><label><input type="radio" value="'+box["label"]+'" id="'+str(col.id)+'" name="'+str(col.id)+'">'+box["label"]+'</label></div>'
        elif col.type == "dropdown":
            html = '<p class="" for="'+str(col.id)+'">'+col.label+'</p>'
            html += '<select data-live-search="true" name="'+str(col.id)+'" id="'+str(col.id)+'" class="selectpicker">'
            for box in options["options"]:
                html +='<option>'+box["label"]+'</option>'
            html += '</select>'
        else:
            return"<div>errore</div>"
        form[col.num_order] = '<div class="form-group">' + html + '</div>'
    return form


# Export data old method
def export_csv(survey, col_list, final_list, filename):
    '''
    Per esportare il programma i risultati in CSV prima versione del programma ora obsoleta
    :param survey:
    :param col_list:
    :param final_list:
    :param filename:
    :return:
    '''
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    labels = [c.label for c in col_list]
    numfields = len(col_list)

    writer.writerow(labels)
    row = []
    for col in final_list:
        for val in col:
            row.append(val.value)
        writer.writerow(row)
        row = []
    return response


# Export data for Student, Job and Aziende
def export_csv_SJA(survey, col_list, filename):
    '''
    Permette di esportare i risultati di sondaggi a
    :param survey:
    :param col_list:
    :param filename:
    :return:
    '''
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    numfields = len(col_list)
    writer.writerow(col_list)
    row = []
    for key in survey:
        for label in col_list:
            # controllo i nulli
            if(key == 44):
                logger.error(survey[key][label])
                logger.error(label)
                logger.error(type(survey[key][label]))
            if (survey[key][label] != '') and (survey[key][label] != ' ') and (survey[key][label] is not None):
                row.append(survey[key][label])
                #logger.error('tutto ok')
            else:
                row.append("None")
                #logger.error('Scrivo None')
        writer.writerow(row)
        row = []
    return response



import random
import string

# password generator
def gen_password():
    '''
    Genera una password a partire da un dizionario di parole
    :return:  la èassword generata
    '''
    # Legge un file.
    file = open(settings.STATICFILES_DIRS[0]+"/dict/words_italian.txt", "r")
    list_num = [line.strip() for line in file]
    file.close()

    password = "123456"
    while len(password) < 8:
        first = random.choice(list_num)+random.choice(list_num)+random.choice(string.digits)+random.choice(string.digits)
        second = random.choice(list_num)+random.choice(string.digits)+random.choice(list_num)+random.choice(string.digits)
        password = random.choice([first, second])
        password = random.choice([password.capitalize(), password])
    return password


# manda mail con codice attivazione
def send_verification_email(request, user, isAzienda,password):
    '''
    :param request:
    :param user: utente
    :param isAzienda: mail diversa per le aziende
    :param password: codice per la passoword
    :return:
    '''
    # se nel futuro vogliamo persoanlizzare messaggio azienda o stundete modificare qui
    if user.type == 1:
        link = request.build_absolute_uri(reverse('verification', args=[user.id, user.activationCode]))
    else:
        link = request.build_absolute_uri(reverse('verification', args=[user.id, user.activationCode]))
    text_content = "Benvenuto in UnipdJob\nApri il link per verificare l'account\n" + link
    html_content = "<h2>UnipdJOB</h2><br>Apri il link per verificare l'account\n<br><a href='" + link + "'>link</a> <br> <p>La tua password: "+password+"</p>"
    mittenti = [user.email]
    logger.error("il mittente "+ mittenti[0])
    logger.error("la password" + password)
    logger.error(" ")
    return send_mail('Verifica account', text_content, "jobunipd@gmail.com", mittenti, fail_silently=False, html_message=html_content)


# per un redirect customizzato lo uso su reset password
def custom_redirect(url_name, *args, **kwargs):
    '''
    Permette di effettuare dei redirect
    :param url_name: url per effettuare il redirect
    :param args: arogmenti
    :param kwargs: vettore arogmenti
    :return:
    '''
    if args:
        url = reverse(url_name, args=args)
    else:
        url = reverse(url_name)
    params = urllib.parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def send_reset_pass_email(request, user):
    '''
    Genera una mail con il codice per aggiornare la password
    :param request:
    :param user: utente
    :return:
    '''
    #link url server
    link = request.build_absolute_uri(reverse('reset_password', args=[user.id, user.account.activationCode]))
    text_content = "Job UNIPD\nApri il link per resettare la password dell'account\n" + link
    html_content = "<h2>JOB UNIPD</h2><br>Apri il link per resettare l'account\n<br><a href='" + link + "'>link</a>"
    return send_mail('Reset password', text_content, "jobunipd@gmail.com", [user.email], fail_silently=False, html_message=html_content)