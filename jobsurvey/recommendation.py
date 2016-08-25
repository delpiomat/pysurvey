from createSurvey.models import *

# prodotto scalare tra due utenti per la distanza (cardinalita intersezione 2 insiemi)
# se un termine Nullo il punteggio per quel dato vale ZERO (parte di And negli if)
def stud_prodotto_scalare(st1_id, st2_id):
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