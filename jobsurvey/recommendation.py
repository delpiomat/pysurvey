from createSurvey.models import *


def stud_prodotto_scalare(st1_id, st2_id):
    '''
    Prodotto scalare tra due utenti per la distanza (cardinalita intersezione 2 insiemi)
    se un termine Nullo il punteggio per quel dato vale ZERO (parte di And negli if)
    :param st1_id: id primo studente
    :param st2_id: id secondo stundente
    :return: ritorna un punteggio di similarità
    '''
    score = 0
    s1 = Persona.objects.get(pk=st1_id)
    s2 = Persona.objects.get(pk=st2_id)
    if (s1.anno_nascita == s2.anno_nascita) and s1.anno_nascita and s2.anno_nascita:
        score += 1
    if (s1.cap == s2.cap) and s1.cap and s2.cap:
        score += 1
    # per 5 voti sono uguali
    if s1.voto_finale and s2.voto_finale:
        if abs(s1.voto_finale - s2.voto_finale) <= 5:
            score += 1
    if (s1.esperienze_pregresse == s2.esperienze_pregresse) and s1.esperienze_pregresse and s2.esperienze_pregresse:
        score += 1
    if (s1.numero_attivita_svolte == s2.numero_attivita_svolte) and s1.numero_attivita_svolte and s2.numero_attivita_svolte:
        score += 1
    if (s1.numero_mesi_attivita_svolte == s2.numero_mesi_attivita_svolte) and s1.numero_mesi_attivita_svolte and s2.numero_mesi_attivita_svolte:
        score += 1
    if (s1.possibilita_trasferirsi == s2.possibilita_trasferirsi) and s1.possibilita_trasferirsi == s2.possibilita_trasferirsi:
        score += 1
    # per 200 euro gli stipendi sono simili
    if s1.stipendio_futuro and s2.stipendio_futuro:
        if abs(s1.stipendio_futuro - s2.stipendio_futuro) <= 200:
            score += 1
    if (s1.grado_studi_id == s2.grado_studi_id) and s1.grado_studi_id and s2.grado_studi_id:
        score += 1
    if (s1.livello_uso_computer_id == s2.livello_uso_computer_id) and s1.livello_uso_computer_id and s2.livello_uso_computer_id:
        score += 1
    if (s1.zona_id == s2.zona_id) and s1.zona_id and s2.zona_id:
        score += 1

    # Mansione
    s1_att= MansionePregresso.objects.filter(persona=s1).select_related()
    s2_att = MansionePregresso.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.mansione_id == m2.mansione_id and m1.mansione_id and m2.mansione_id:
                score += 1

    s1_att = MansioneAttuale.objects.filter(persona=s1).select_related()
    s2_att = MansioneAttuale.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.mansione_id == m2.mansione_id and m1.mansione_id and m2.mansione_id:
                score += 1

    s1_att = MansioneFuturo.objects.filter(persona=s1).select_related()
    s2_att = MansioneFuturo.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.mansione_id == m2.mansione_id and m1.mansione_id and m2.mansione_id:
                score += 1

    # Ruolo
    s1_att = RuoloPregresso.objects.filter(persona=s1).select_related()
    s2_att = RuoloPregresso.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.ruolo_id == m2.ruolo_id and m1.ruolo_id and m2.ruolo_id:
                score += 1

    s1_att = RuoloAttuale.objects.filter(persona=s1).select_related()
    s2_att = RuoloAttuale.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.ruolo_id == m2.ruolo_id and m1.ruolo_id and m2.ruolo_id:
                score += 1

    s1_att = RuoloFuturo.objects.filter(persona=s1).select_related()
    s2_att = RuoloFuturo.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.ruolo_id == m2.ruolo_id and m1.ruolo_id and m2.ruolo_id:
                score += 1

    # Area Operativa
    s1_att = AreaOperativaPregresso.objects.filter(persona=s1).select_related()
    s2_att = AreaOperativaPregresso.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.area_operativa_id == m2.area_operativa_id and m1.area_operativa_id and m2.area_operativa_id:
                score += 1

    s1_att = AreaOperativaAttuale.objects.filter(persona=s1).select_related()
    s2_att = AreaOperativaAttuale.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.area_operativa_id == m2.area_operativa_id and m1.area_operativa_id and m2.area_operativa_id:
                score += 1

    s1_att = AreaOperativaFuturo.objects.filter(persona=s1).select_related()
    s2_att = AreaOperativaFuturo.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.area_operativa_id == m2.area_operativa_id and m1.area_operativa_id and m2.area_operativa_id:
                score += 1

    # Livello Cariera
    s1_att = LivelloCarieraPregresso.objects.filter(persona=s1).select_related()
    s2_att = LivelloCarieraPregresso.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.livello_cariera_id == m2.livello_cariera_id and m1.livello_cariera_id and m2.livello_cariera_id:
                score += 1

    s1_att = LivelloCarieraAttuale.objects.filter(persona=s1).select_related()
    s2_att = LivelloCarieraAttuale.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.livello_cariera_id == m2.livello_cariera_id and m1.livello_cariera_id and m2.livello_cariera_id:
                score += 1

    s1_att = LivelloCarieraFuturo.objects.filter(persona=s1).select_related()
    s2_att = LivelloCarieraFuturo.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.livello_cariera_id == m2.livello_cariera_id and m1.livello_cariera_id and m2.livello_cariera_id:
                score += 1

    # Tipo Contratto
    s1_att = TipoContrattoPregesso.objects.filter(persona=s1).select_related()
    s2_att = TipoContrattoPregesso.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.tipo_contratto_id == m2.tipo_contratto_id and m1.tipo_contratto_id and m2.tipo_contratto_id:
                score += 1

    s1_att = TipoContrattoAttuale.objects.filter(persona=s1).select_related()
    s2_att = TipoContrattoAttuale.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.tipo_contratto_id == m2.tipo_contratto_id and m1.tipo_contratto_id and m2.tipo_contratto_id:
                score += 1

    s1_att = TipoContrattoFuturo.objects.filter(persona=s1).select_related()
    s2_att = TipoContrattoFuturo.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.tipo_contratto_id == m2.tipo_contratto_id and m1.tipo_contratto_id and m2.tipo_contratto_id:
                score += 1

    # Esame
    s1_att = EsameAttuale.objects.filter(persona=s1).select_related()
    s2_att = EsameAttuale.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.esame_id == m2.esame_id and m1.esame_id and m2.esame_id:
                score += 1

    # Conoscenza
    s1_att = ConoscenzaSpecificaAttuale.objects.filter(persona=s1).select_related()
    s2_att = ConoscenzaSpecificaAttuale.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.conoscenza_specifica_id == m2.conoscenza_specifica_id and m1.conoscenza_specifica_id and m2.conoscenza_specifica_id:
                score += 1

    # Interesse
    s1_att = InteresseFuturo.objects.filter(persona=s1).select_related()
    s2_att = InteresseFuturo.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.interesse_id == m2.interesse_id and m1.interesse_id and m2.interesse_id:
                score += 1

    # Benefit
    s1_att = BenefitFuturo.objects.filter(persona=s1).select_related()
    s2_att = BenefitFuturo.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.benefit_id == m2.benefit_id and m1.benefit_id and m2.benefit_id:
                score += 1

    # Campo di Studi
    s1_att = CampoStudiAttuale.objects.filter(persona=s1).select_related()
    s2_att = CampoStudiAttuale.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.campo_studi_id == m2.campo_studi_id and m1.campo_studi_id and m2.campo_studi_id:
                score += 1

    # Lingua
    s1_att = LinguaAttuale.objects.filter(persona=s1).select_related()
    s2_att = LinguaAttuale.objects.filter(persona=s2).select_related()
    for m1 in s1_att:
        for m2 in s2_att:
            if m1.lingua_id == m2.lingua_id and m1.lingua_id and m2.lingua_id:
                score += 1

    return score

def stud_cardinality (st_id):
    '''
    Conta quanti elementi possiede uno studente in totale tra tutte le sue feature
    :param st_id: id di uno studente
    :return: la cardinalita
    '''
    dim = 0
    s = Persona.objects.get(pk=st_id)
    #cardinalita di A
    if s.anno_nascita:
        dim += 1
    if s.cap:
        dim += 1
    # per 5 voti sono uguali
    if s.voto_finale:
        dim += 1
    if s.esperienze_pregresse:
        dim += 1
    if s.numero_attivita_svolte:
        dim += 1
    if s.numero_mesi_attivita_svolte:
        dim += 1
    if s.possibilita_trasferirsi:
        dim += 1
    if s.stipendio_futuro:
        dim += 1
    if s.grado_studi_id :
        dim += 1
    if s.livello_uso_computer_id:
        dim += 1
    if s.zona_id:
        dim += 1

    # Mansione
    s_att= MansionePregresso.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.mansione_id:
            dim += 1

    s_att = MansioneAttuale.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.mansione_id:
            dim += 1

    s_att = MansioneFuturo.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.mansione_id:
            dim += 1

    # Ruolo
    s_att = RuoloPregresso.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.ruolo_id:
            dim += 1

    s_att = RuoloAttuale.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.ruolo_id == m.ruolo_id and m.ruolo_id and m.ruolo_id:
            dim += 1

    s1_att = RuoloFuturo.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.ruolo_id == m.ruolo_id and m.ruolo_id and m.ruolo_id:
            dim += 1

    # Area Operativa
    s_att = AreaOperativaPregresso.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.area_operativa_id:
            dim += 1

    s_att = AreaOperativaAttuale.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.area_operativa_id:
            dim += 1

    s_att = AreaOperativaFuturo.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.area_operativa_id:
            dim += 1

    # Livello Cariera
    s_att = LivelloCarieraPregresso.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.livello_cariera_id:
            dim += 1

    s_att = LivelloCarieraAttuale.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.livello_cariera_id:
            dim += 1

    s_att = LivelloCarieraFuturo.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.livello_cariera_id:
            dim += 1

    # Tipo Contratto
    s_att = TipoContrattoPregesso.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.tipo_contratto_id:
            dim += 1

    s_att = TipoContrattoAttuale.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.tipo_contratto_id:
            dim += 1

    s_att = TipoContrattoFuturo.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.tipo_contratto_id:
            dim += 1

    # Esame
    s_att = EsameAttuale.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.esame_id:
            dim += 1

    # Conoscenza
    s_att = ConoscenzaSpecificaAttuale.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.conoscenza_specifica_id:
            dim += 1

    # Interesse
    s_att = InteresseFuturo.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.interesse_id:
            dim += 1

    # Benefit
    s_att = BenefitFuturo.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.benefit_id:
            dim += 1

    # Campo di Studi
    s_att = CampoStudiAttuale.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.campo_studi_id:
            dim += 1

    # Lingua
    s_att = LinguaAttuale.objects.filter(persona=s).select_related()
    for m in s_att:
        if m.lingua_id:
            dim += 1

    return dim


# Misura Dice
# 2*|A intersezione B| / |A|+|B|
def stud_dice(st1_id, st2_id):
    '''
    Calcola una forma leggermente imprecisa di Misura DICE 2*|A intersezione B| / |A|+|B|
    :param st1_id: id primo studente
    :param st2_id: id secondo studente
    :return: il punteggio
    '''
    intersection = stud_prodotto_scalare(st1_id, st2_id)
    union = stud_cardinality(st1_id) + stud_cardinality(st2_id)
    return (2*intersection)/union


# Misura dice Jaccard  ( |A intersecato B| / |A unione B| )
# Jaccard = Dice/(2-Dice) e Dice = 2Jaccard / (1+Jaccard)
def stud_jaccard(st1_id, st2_id):
    '''
    Calcola la misura di Jaccard in Maniera un po im precisa, Misura dice Jaccard  ( |A intersecato B| / |A unione B| )
    quindi Jaccard = Dice/(2-Dice) e Dice = 2Jaccard / (1+Jaccard)
    :param st1_id: id primo studente
    :param st2_id: id secodno studente
    :return: ritorna il punteggio di jaccard
    '''
    score_dice = stud_dice(st1_id, st2_id)
    return score_dice/(2-score_dice)


#-------------------------------Aziende--------------------------------------------------------------------------------
# prodotto scalare tra due utenti Azienda per la distanza (cardinalita intersezione 2 insiemi)
# se un termine Nullo il punteggio per quel dato vale ZERO (parte di And negli if)

def azieda_scalare(az1_id, az2_id):
    '''
    Da Completare produce il Prodotto scalare tra due Aziende
    :param az1_id: id prima Azienda
    :param az2_id: id Seconda Azienda
    :return: Lo score
    '''
    score=0
    return score