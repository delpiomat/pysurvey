from django.db import models
from django.contrib.auth.models import User

# for database setting

# python manage.py makemigrations

# change 0001 every time####
# python manage.py sqlmigrate pysurvey 0001
# python manage.py migrate
# python manage.py runserver 0.0.0.0:8000

TYPE_CHOICES = ((0, 'Utente'), (1, 'Azienda'), (2, 'Admin'))


# utente modificato
class Account(User):
    type = models.IntegerField(choices=TYPE_CHOICES, default=0)
    # email gia nella classe base con   Optional. Email address.
    activationCode = models.CharField(max_length=32, default="", null=False)
    timeCode = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username



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

class Esame(models.Model):
    valore = models.CharField(max_length=64)

class CampoStudi(models.Model):
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

    #data
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)

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
    ruolo = models.ForeignKey(Ruolo, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class RuoloPregresso(models.Model):
    ruolo = models.ForeignKey(Ruolo, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class RuoloFuturo(models.Model):
    ruolo = models.ForeignKey(Ruolo, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


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


class EsameAttuale(models.Model):
    esame = models.ForeignKey(Esame, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

class CampoStudiAttuale(models.Model):
    campo_studi = models.ForeignKey(CampoStudi, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)



# -----------------------------------------------------------------------------------------------------------------
# Aziende

class Citta(models.Model):
    valore = models.CharField(max_length=64)


class Azienda(models.Model):
    #anagrafica
    email = models.CharField(max_length=64, null=True)
    nome_referente = models.CharField(max_length=512, null=True)
    note = models.CharField(max_length=512, null=True)
    citta_sede = models.ForeignKey(Citta, on_delete=models.CASCADE, null=True)
    #data
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)


class AltraSede(models.Model):
    citta = models.ForeignKey(Citta, on_delete=models.CASCADE, null=True)
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE)

# -----------------------------------------------------------------------------------------------------------------
# Lavoro


class Lavoro(models.Model):
    email_referente = models.CharField(max_length=64, null=True)
    note_lavoro = models.CharField(max_length=512, null=True)
    durata_lavoro = models.IntegerField(null=True)
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE)
    distanza_massima = models.CharField(max_length=64, null=True)
    #data
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)


class CercaLingua(models.Model):
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    lingua= models.ForeignKey(Lingua, on_delete=models.CASCADE, null=True)


class CercaLivelloCariera(models.Model):
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)


class CercaCitta(models.Model):
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    citta = models.ForeignKey(Citta, on_delete=models.CASCADE, null=True)


class CercaTipoContratto(models.Model):
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)


class CercaEsami(models.Model):
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    esame = models.ForeignKey(Esame, on_delete=models.CASCADE, null=True)

class CercaAreaOperativa(models.Model):
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)

class CercaCampoStudio(models.Model):
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    campo_studio = models.ForeignKey(CampoStudi, on_delete=models.CASCADE, null=True)




# fine Lavoro