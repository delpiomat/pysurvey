from django.db import models

# for database setting

# python manage.py makemigrations

# change 0001 every time####
# python manage.py sqlmigrate pysurvey 0001
# python manage.py migrate
# python manage.py runserver 0.0.0.0:8000


#id is by default
class Survey(models.Model):
    name = models.CharField(max_length=256)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    note = models.CharField(max_length=512)

    #for string print
    def __str__(self):
        return self.name


class Column(models.Model):
    label = models.CharField(max_length=256, default="")
    type = models.CharField(max_length=256, default="")
    required = models.BooleanField(default=True)
    option = models.CharField(max_length=2048, default="")
    description = models.CharField(max_length=2048, default="")
    jsonCode = models.CharField(max_length=4096, default="")
    num_order = models.IntegerField()
    cid = models.CharField(max_length=32, default="")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.label


class Interview(models.Model):
    name_user = models.CharField(max_length=256, default="anonymous")
    type_user = models.CharField(max_length=256, default="people")

    def __str__(self):
        return self.id


class Result(models.Model):
    value = models.CharField(max_length=256, default="")
    type_value = models.CharField(max_length=256, default="single")  # for array/single/dict value
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
