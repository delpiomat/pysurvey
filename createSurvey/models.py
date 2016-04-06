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
# ------------------------------------------------------------------------------------------------------------------


# valori sigoli ----------------------------------------------------------------------------------------------------
class Zona(models.Model):
    valore = models.CharField(max_length=64)


class LivelloPC(models.Model):
    valore = models.CharField(max_length=64)


class GradoStudi(models.Model):
    valore = models.CharField(max_length=64)


# valori multipli------------------------------------------------------------------------------------------------------
class Stato(models.Model):
    valore = models.CharField(max_length=64)


class Lingua(models.Model):
    valore = models.CharField(max_length=64)


class ConoscenzaSpecifica(models.Model):
    valore = models.CharField(max_length=64)


class Mansione(models.Model):
    valore = models.CharField(max_length=64)


class LivelloCariera(models.Model):
    valore = models.CharField(max_length=64)


class Ruolo(models.Model):
    valore = models.CharField(max_length=64)


class AreaOperativa(models.Model):
    valore = models.CharField(max_length=64)


class TipoContratto(models.Model):
    valore = models.CharField(max_length=64)


class Benefit(models.Model):
    valore = models.CharField(max_length=64)


class Interesse(models.Model):
    valore = models.CharField(max_length=64)


class Persona(models.Model):
    #anagrafica
    email = models.CharField(max_length=64, null=True)
    cap = models.CharField(max_length=64, null=True)
    citta = models.CharField(max_length=64, null=True)
    anno_nascita = models.IntegerField(null=True)
    note = models.CharField(max_length=512, null=True)
    voto_finale = models.IntegerField(null=True)

    #esperienze pregresse
    esperienze_pregresse = models.BooleanField(default=False)  # si/no
    desc_esperienze_pregresse = models.CharField(max_length=512, null=True)
    numero_attivita_svolte = models.IntegerField(default=0, null=True)
    numero_mesi_attivita_svolte = models.IntegerField(default=0, null=True)

    #futuro
    possibilita_trasferirsi = models.BooleanField(default=False)  # si/no/non so????
    stipendio_futuro = models.IntegerField(default=0, null=True)

    #esterne
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, null=True)
    grado_studi = models.ForeignKey(GradoStudi, on_delete=models.CASCADE, null=True)
    livello_uso_computer = models.ForeignKey(LivelloPC, on_delete=models.CASCADE, null=True)


class StatoAttuale(models.Model):
    stato = models.ForeignKey(Stato, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class LinguaAttuale(models.Model):
    lingua = models.ForeignKey(Lingua, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class ConoscenzaSpecificaAttuale(models.Model):
    conoscenza_specifica = models.ForeignKey(ConoscenzaSpecifica, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class MansioneAttuale(models.Model):
    mansione = models.ForeignKey(Mansione, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class MansionePregresso(models.Model):
    mansione = models.ForeignKey(Mansione, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class MansioneFuturo(models.Model):
    mansione = models.ForeignKey(Mansione, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class LivelloCarieraAttuale(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True )


class LivelloCarieraPregresso(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)


class LivelloCarieraFuturo(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)


class RuoloAttuale(models.Model):
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)
    Persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class RuoloPregresso(models.Model):
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)
    livello_cariera = models.ForeignKey(Persona, on_delete=models.CASCADE)


class RuoloFuturo(models.Model):
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)
    livello_cariera = models.ForeignKey(Persona, on_delete=models.CASCADE)


class AreaOperativaAttuale(models.Model):
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class AreaOperativaPregresso(models.Model):
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class AreaOperativaFuturo(models.Model):
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class TipoContrattoAttuale(models.Model):
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class TipoContrattoPregesso(models.Model):
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class TipoContrattoFuturo(models.Model):
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class BenefitFuturo(models.Model):
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class InteresseFuturo(models.Model):
    interesse = models.ForeignKey(Interesse, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)