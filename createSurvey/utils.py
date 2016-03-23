from .models import Column, Survey

# for Json format
import json

# import the logging library #per debug scrive nella Console
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def json_form_in_html(survey):
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

