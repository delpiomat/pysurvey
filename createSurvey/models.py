from django.db import models

#for database setting

#python manage.py makemigrations pysurvey

#change 0001 every time
#python manage.py sqlmigrate pysurvey 0001
#python manage.py migrate
#python manage.py runserver 0.0.0.0:8000


#id is by default
class Survey(models.Model):
    name = models.CharField(max_length=256)
    pub_date = models.DateTimeField('date published')
    note = models.CharField(max_length=512)

    #for string print
    def __str__(self):
        return self.name

class Domain(models.Model):
    value = models.CharField(max_length=1024, default="")
    type = models.CharField(max_length=256)

    def __str__(self):
        return self.id


class Column(models.Model):
    name = models.CharField(max_length=256)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


