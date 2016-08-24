from createSurvey.models import *

# prodotto scalare tra due utenti per la distanza (cardinalita intersezione 2 insiemi)
def stud_prodotto_scalare(st1_id, st2_id):
    dist = 0
    s1 = Persona.objects.get(pk=st1_id)
    s2 = Persona.objects.get(pk=st2_id)
    if s1.anno_nascita == s2.anno_nascita:
        dist += 1
    if s1.cap == s2.cap:
        dist += 1
    if s1.cap == s2.cap:
        dist += 1
    if s1.voto_finale == s2.voto_finale:
        dist += 1
    if s1.esperienze_pregresse == s2.esperienze_pregresse:
        dist += 1
    if s1.numero_attivita_svolte == s2.numero_attivita_svolte:
        dist += 1
    if s1.numero_mesi_attivita_svolte == s2.numero_mesi_attivita_svolte:
        dist += 1
    if s1.possibilita_trasferirsi == s2.possibilita_trasferirsi:
        dist += 1
    if s1.stipendio_futuro == s2.stipendio_futuro:
        dist += 1
    if s1.grado_studi_id == s2.grado_studi_id:
        dist += 1
    if s1.livello_uso_computer_id == s2.livello_uso_computer_id:
        dist += 1
    if s1.zona_id == s2.zona_id:
        dist += 1
    return dist