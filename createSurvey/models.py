from django.db import models
from django.contrib.auth.models import User

# for database setting

# python manage.py makemigrations

# change 0001 every time####
# python manage.py sqlmigrate createSurvey 0001
# python manage.py migrate
# python manage.py runserver 0.0.0.0:8000

TYPE_CHOICES = ((0, 'Utente'), (1, 'Azienda'), (2, 'Admin'))


#id is by default
class Survey(models.Model):
    '''
    Sondaggio vecchio modo di fare, obsoleto
    '''
    name = models.CharField(max_length=256)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    note = models.CharField(max_length=512)

    #for string print
    def __str__(self):
        return self.name


class Column(models.Model):
    '''
    Attributi di un sondagggio vecchio modo di fare, obsoleto
    '''
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
    '''
    Intervista di un sondagggio vecchio modo di fare, obsoleto
    '''
    name_user = models.CharField(max_length=256, default="anonymous")
    type_user = models.CharField(max_length=256, default="people")

    def __str__(self):
        return self.id


class Result(models.Model):
    '''
    Risultato di un sondagggio vecchio modo di fare, obsoleto
    '''
    value = models.CharField(max_length=256, default="")
    type_value = models.CharField(max_length=256, default="single")  # for array/single/dict value
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
# ------------------------------------------------------------------------------------------------------------------


# valori sigoli ----------------------------------------------------------------------------------------------------
class Zona(models.Model):
    '''
    Rappresenta la tabella con tutte le possibili Zone
    '''
    valore = models.CharField(max_length=64)


class LivelloPC(models.Model):
    '''
    Rappresenta la tabella con tutte  i possibili Livelli di conoscenza nell'uso del Computer
    '''
    valore = models.CharField(max_length=64)


class GradoStudi(models.Model):
    '''
    Rappresenta la tabella con tutte i possibili Livelli di Istruzione
    '''
    valore = models.CharField(max_length=64)


# valori multipli------------------------------------------------------------------------------------------------------
class Stato(models.Model):
    '''
    Rappresenta la tabella con tutte i  possibili Stati occupazionali
    '''
    valore = models.CharField(max_length=64)


class Lingua(models.Model):
    '''
    La tabella con tutte le possibili lingue presenti nei sondaggi
    '''
    valore = models.CharField(max_length=64)


class ConoscenzaSpecifica(models.Model):
    '''
    Rappresenta la tabella con tutte le possibili conoscenza specifiche
    '''
    valore = models.CharField(max_length=64)


class Mansione(models.Model):
    '''
    Rappresenta la tabella con tutte le possibili mansioni
    '''
valore = models.CharField(max_length=64)


class LivelloCariera(models.Model):
    '''
    Rappresenta la tabella con tutte i possibili Livelli di Cariera
    '''
    valore = models.CharField(max_length=64)


class Ruolo(models.Model):
    '''
    Rappresenta la tabella con tutte i possibili Ruoli
    '''
    valore = models.CharField(max_length=64)


class AreaOperativa(models.Model):
    '''
    Rappresenta la tabella con tutte le possibili Aree Operative
    '''
    valore = models.CharField(max_length=64)


class TipoContratto(models.Model):
    '''
    Rappresenta la tabella con tutti i possibili Tipi Di Contratto
    '''
    valore = models.CharField(max_length=64)


class Benefit(models.Model):
    '''
    Rappresenta la tabella con tutti i possibili Benefit
    '''
    valore = models.CharField(max_length=64)


class Interesse(models.Model):
    '''
    Rappresenta la tabella con tutti i possibili Interessi
    '''
    valore = models.CharField(max_length=64)

class Esame(models.Model):
    '''
    Rappresenta la tabella con tutte i possibili esami
    '''
    valore = models.CharField(max_length=64)

class CampoStudi(models.Model):
    '''
    Rappresenta la tabella con tutte i possibili Campi di Studio
    '''
    valore = models.CharField(max_length=64)


class Persona(models.Model):
    '''
    Rappresenta la tabella Tutte le persone (Studenti) che hanno effettuato un sondaggio
    '''
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
    '''
    Rappresenta la tabella che associa una Persona con zero o piu stati occupazionali
    '''
    stato = models.ForeignKey(Stato, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class LinguaAttuale(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Lingue conosciute
    '''
    lingua = models.ForeignKey(Lingua, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class ConoscenzaSpecificaAttuale(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu conoscenze specifiche
    '''
    conoscenza_specifica = models.ForeignKey(ConoscenzaSpecifica, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class MansioneAttuale(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Mansioni Attuali
    '''
    mansione = models.ForeignKey(Mansione, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class MansionePregresso(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Mansioni Passate
    '''
    mansione = models.ForeignKey(Mansione, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class MansioneFuturo(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Mansioni Future
    '''
    mansione = models.ForeignKey(Mansione, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class LivelloCarieraAttuale(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Livelli di cariera Attuali
    '''
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True )


class LivelloCarieraPregresso(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Livelli di cariera Passati
    '''
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)


class LivelloCarieraFuturo(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Livelli di cariera Futuri
    '''
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)


class RuoloAttuale(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Ruoli Attuali
    '''
    ruolo = models.ForeignKey(Ruolo, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class RuoloPregresso(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Ruoli Passati
    '''
    ruolo = models.ForeignKey(Ruolo, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class RuoloFuturo(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Ruoli Futuri
    '''
    ruolo = models.ForeignKey(Ruolo, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class AreaOperativaAttuale(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Aree Operative Attuali
    '''
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class AreaOperativaPregresso(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Aree Operative Passate
    '''
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class AreaOperativaFuturo(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Aree Operative Future
    '''
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class TipoContrattoAttuale(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu tipi di Contratti Attuali
    '''
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class TipoContrattoPregesso(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu tipi di Contratti Passati
    '''
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class TipoContrattoFuturo(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu tipi di Contratti Futuri
    '''
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class BenefitFuturo(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Benefit Futuri
    '''
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class InteresseFuturo(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Interessi Futuri
    '''
    interesse = models.ForeignKey(Interesse, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class EsameAttuale(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Esami
    '''
    esame = models.ForeignKey(Esame, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

class CampoStudiAttuale(models.Model):
    '''
    Rappresenta la tabella che associa una Persona con zero o piu Campi di Studio
    '''
    campo_studi = models.ForeignKey(CampoStudi, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)



# -----------------------------------------------------------------------------------------------------------------
# Aziende

class Citta(models.Model):
    '''
    Rappresenta la tabella delle citta
    '''
    valore = models.CharField(max_length=64)


class Azienda(models.Model):
    '''
    Rappresenta la tabella delle Aziende che proponogno offerte di lavoro
    '''
    #anagrafica
    email = models.CharField(max_length=64, null=True)
    nome_referente = models.CharField(max_length=512, null=True)
    note = models.CharField(max_length=512, null=True)
    citta_sede = models.ForeignKey(Citta, on_delete=models.CASCADE, null=True)
    #data
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)


class AltraSede(models.Model):
    '''
    Rappresenta la tabella che associa un azienda a zero o piu sedi alternative
    '''
    citta = models.ForeignKey(Citta, on_delete=models.CASCADE, null=True)
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE)

# -----------------------------------------------------------------------------------------------------------------
# Lavoro


class Lavoro(models.Model):
    '''
    Rappresenta la tabella delle offerte di lavoro
    '''
    email_referente = models.CharField(max_length=64, null=True)
    note_lavoro = models.CharField(max_length=512, null=True)
    durata_lavoro = models.IntegerField(null=True)
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE)
    distanza_massima = models.CharField(max_length=64, null=True)
    #data
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)


class CercaLingua(models.Model):
    '''
    Rappresenta la tabella che associa una Offerta di Lavoro con zero o piu tipi Lingue
    '''
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    lingua= models.ForeignKey(Lingua, on_delete=models.CASCADE, null=True)


class CercaLivelloCariera(models.Model):
    '''
    Rappresenta la tabella che associa una Offerta di Lavoro con zero o piu livelli cariera
    '''
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    livello_cariera = models.ForeignKey(LivelloCariera, on_delete=models.CASCADE, null=True)


class CercaCitta(models.Model):
    '''
    Rappresenta la tabella che associa una Offerta di Lavoro con zero o piu Citta
    '''
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    citta = models.ForeignKey(Citta, on_delete=models.CASCADE, null=True)


class CercaTipoContratto(models.Model):
    '''
    Rappresenta la tabella che associa una Offerta di Lavoro con zero o piu Tipi di Contratto
    '''
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    tipo_contratto = models.ForeignKey(TipoContratto, on_delete=models.CASCADE, null=True)


class CercaEsami(models.Model):
    '''
    Rappresenta la tabella che associa una Offerta di Lavoro con zero o piu Esami
    '''
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    esame = models.ForeignKey(Esame, on_delete=models.CASCADE, null=True)

class CercaAreaOperativa(models.Model):
    '''
    Rappresenta la tabella che associa una Offerta di Lavoro con zero o piu Aree Operative
    '''
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.CASCADE, null=True)

class CercaCampoStudio(models.Model):
    '''
    Rappresenta la tabella che associa una Offerta di Lavoro con zero o piu Campi di Studio
    '''
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)
    campo_studio = models.ForeignKey(CampoStudi, on_delete=models.CASCADE, null=True)


# utente modificato
class Account(User):
    '''
    Account deriva dalla classe account e permette di aggiungere utleriori caratteristiche all'untente loggato
    '''
    type = models.IntegerField(choices=TYPE_CHOICES, default=0)
    # email gia nella classe base con   Optional. Email address.
    activationCode = models.CharField(max_length=32, default="", null=False)
    timeCode = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey(Persona, null=True, on_delete=models.CASCADE)
    azienda = models.ForeignKey(Azienda, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class MatricePunteggio(models.Model):
    '''
    Rappresente la Matrice dei punteggi tra Persone e Lavori
    '''
    persona = models.ForeignKey(Persona, null=True, on_delete=models.CASCADE)
    lavoro = models.ForeignKey(Lavoro, null=True, on_delete=models.CASCADE)
    punteggio_dato_da_persona = models.IntegerField(null=True)
    punteggio_dato_da_lavoro = models.IntegerField(null=True)
    note_da_persona = models.CharField(max_length=512, null=True)
    note_da_lavoro = models.CharField(max_length=512, null=True)

# fine Lavoro