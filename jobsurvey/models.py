from django.db import models

# for database setting

# python manage.py makemigrations

# change 0001 every time####
# python manage.py sqlmigrate pysurvey 0001
# python manage.py migrate
# python manage.py runserver 0.0.0.0:8000

#scrivo tutto in ita perche non ho tempo sorry
class Persona(models.Model):
    #anagrafica
    email = models.CharField(max_length=64, null=True)
    cap = models.CharField(max_length=64, null=True)
    citta = models.CharField(max_length=64, null=True)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, null=True)
    anno_nascita = models.IntegerField(null=True)
    note = models.CharField(max_length=512, null=True)
    #stato_attuale = models.ForeignKey(StatoAtuale, on_delete=models.CASCADE, null=True)  # multivalore
    grado_studi = models.ForeignKey(GradoStudi, on_delete=models.CASCADE, null=True)
    voto_finale = models.IntegerField(null=True)
    livello_uso_computer = models.ForeignKey(LivelloPC, on_delete=models.CASCADE, null=True)
    #lingue = models.ForeignKey(Lingue, on_delete=models.CASCADE, null=True)  # multivalore
    #conoscenze_specifiche = []  # multivalore

    #lavoro attuale
    #mansione_attuale=[]  # multivalore
    #livello_cariera_attuale=[]  # multivalore
    #ruolo_attuale=[]  # multivalore
    #area_operativa_attuale=[]  # multivalore
    #tipo_contratto_attuale=[]  # multivalore

    #esperienze pregresse
    esperienze_pregresse = models.BooleanField()  # si/no
    desc_esperienze_pregresse = models.CharField(max_length=512)
    #mansione_pregressa=[]  # multivalore
    #livello_cariera_pregressa=[]  # multivalore
    #ruolo_pregressa=[]  # multivalore
    #area_operativa_pregressa=[]  # multivalore
    #tipo_contratto_pregresso=[]  # multivalore
    numero_attivita_svolte = models.IntegerField()
    numero_mesi_attivita_svolte = models.IntegerField()

    #futuro
    #mansione_futuro=[]# multivalore
    #livello_cariera_futuro=[]  # multivalore
    #ruolo_futuro = []  # multivalore
    #area_operativa_ruolo_futuro = []  # multivalore
    #tipo_contratto_ruolo_futuro = []  # multivalore
    interessi_futuro = []  # cosa ti piacerebbe fare
    possibilita_trasferirsi = models.BooleanField()  # si/no/non so????
    stipendio_futuro = models.IntegerField()
    benefit_futuro = []  # multivalore


# valori sigoli--------------------------------------------------------------------------------------------------------
class Zona(models.Model):
    valore = models.CharField(max_length=64)


class LivelloPC(models.Model):
    valore = models.CharField(max_length=64)


class GradoStudi(models.Model):
    valore = models.CharField(max_length=64)


# valori multipli------------------------------------------------------------------------------------------------------
class Stato(models.Model):
    valore = models.CharField(max_length=64)

class StatoAttuale(models.Model):
    stato = models.ForeignKey(Stato, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)



class Lingua(models.Model):
    valore = models.CharField(max_length=64)

class LinguaAttuale(models.Model):
    lingua = models.ForeignKey(Lingua, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)



class ConoscenzaSpecifica(models.Model):
    valore = models.CharField(max_length=64)

class ConoscenzaSpecificaAttuale(models.Model):
    conoscenza_specifica = models.ForeignKey(ConoscenzaSpecifica, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)



class Mansione(models.Model):
    valore = models.CharField(max_length=64)

class MansioneAttuale(models.Model):
    mansione = models.ForeignKey(Mansione, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

class MansionePregresso(models.Model):
    mansione = models.ForeignKey(Mansione, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

class MansioneFuturo(models.Model):
    mansione = models.ForeignKey(Mansione, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class LivelloCariera(models.Model):
    valore = models.CharField(max_length=64)

class LivelloCarieraAttuale(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True )

class LivelloCarieraPregresso(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)

class LivelloCarieraFuturo(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)



class Ruolo(models.Model):
    valore = models.CharField(max_length=64)

class RuoloAttuale(models.Model):
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)
    Persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

class RuoloPregresso(models.Model):
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)
    livello_cariera = models.ForeignKey(Persona, on_delete=models.CASCADE)

class RuoloFuturo(models.Model):
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)
    livello_cariera = models.ForeignKey(Persona, on_delete=models.CASCADE)



class AreaOperativa(models.Model):
    valore = models.CharField(max_length=64)

class AreaOperativaAttuale(models.Model):
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

class AreaOperativaPregresso(models.Model):
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

class AreaOperativaFuturo(models.Model):
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)




class TipoContratto(models.Model):
    valore = models.CharField(max_length=64)

class TipoContrattoAttuale(models.Model):
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

class TipoContrattoPregesso(models.Model):
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

class TipoContrattoFuturo(models.Model):
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)