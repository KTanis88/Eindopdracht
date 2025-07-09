def add_scouting_report_full(report_db):
    print("Vul het scoutingsformulier in volgens het boekje.")

    #Algemene gegevens
    datum = input("Datum (dd-mm-jjjj): ").strip()
    westrijd = input("Wedstrijd: ").strip()
    weerstand = input("Weerstand (hoog/gemiddeld/laag):").strip()
    speler = input("Naam speler: ").strip()
    geboortedatum = input("Geboortedatum (dd-mm-jjjj): ").strip()
    club_team = input("Club/Team: ").strip()
    positie = input("Positie: ")
    bouw = input("Lichamelijk bouw: ").strip()

    # Beoordelingscriteria per categorie (voorbeeld met afkortingen)
    print("\n--- Handelingssnelheid ---")
    ASB = input("Aanspeelbaar (ASB): ")
    AN = input("Aanname (AN): ")
    SCA = input("Scannen (SCA): ")
    OZ = input("Overzicht (OZ): ")
    OS = input("Open staan (OS): ")

    print("\n--- Tactisch ---")
    BSH = input("Balsnelheid (BSH): ")
    ZCOM = input("Zoekt combinatie (ZCOM): ")
    POS = input("Positiespel (POS): ")
    LEZ = input("Spel lezen (LEZ): ")
    tweedeB = input("Pakt 2e bal (2eB): ")
    DRZ = input("Drukzetten (DRZ): ")
    Bplusmin = input("Omschakeling Balverlies (B+/B-): ")
    Bminplus = input("Omschakeling Balverovering (B-/B+): ")

    print("\n--- Extra ---")
    TG = input("Taakgericht (TG): ")
    SWL = input("Samenwerking Linie (SWL): ")
    SWAF = input("Samenwerking As/Flank (SWAF): ")
    JB = input("Juiste been (JB): ")
    JT = input("Juiste Tempo (JT): ")
    TT = input("Traptechniek (TT): ")

    print("\n--- Motoriek ---")
    SMS = input("Snelheid/Motoriek/Souplese (SMS): ")
    KWD = input("Kort wegdraaien (KWD): ")
    SH = input("Snelheid (SH): ")
    SSH = input("Startsnelheid (SSH): ")

    print("\n--- Technisch ---")
    BC = input("Balcontrole (BC): ")
    Pl = input("Passing lang (PL): ")
    PK = input("Passing kort (PK): ")
    SCH = input("Schieten (SCH): ")
    VZET = input("Voorzet (VZET): ")

    print("\n--- Voetbalhandeling ---")
    eeneenA = input("1 op 1 Aanvallend (1-1A): ")
    eeneenV = input("1 op 1 Verdedigend (1-1V): ")
    DBEW = input("Doorbewegen (DBEW): ")
    KOPA = input("Koppen Aanvallend (KOPA): ")
    KOPV = input("Koppen Verdedigend (KOPV): ")
    DK= input("Duelkracht (DK): ")
    ZDIEP = input("Zoekt Diepte (ZDIEP): ")
    VSB = input("Voorspelbaar (VSB): ")
    SVM = input("Scorend vermogen (SVM): ")
    BAL_AF = input("Pakt de bal af (BAL AF): ")

    print("\n--- Overige eigenschappen ---")
    coachbaarheid = input("Coachbaarheid: ")
    inzet = input("Inzet & Motivatie: ")
    persoonlijkheid = input("Persoonlijkheid: ")
    houding = input("Houding: ")
    zelfvertrouwen = input("Zelfvertrouwen: ")
    uithoudingsvermogen = input("Uithoudingsvermogen: ")
    sprongkracht = input("Sprongkracht: ")
    gebruikt_lichaam = input("Gebruikt Lichaam: ")

    print("\n--- Type speler ---")
    teamspeler = input("Teamspeler (ja/nee): ")
    leider = input("Leider (ja/nee): ")
    creatief = input("Creatief (ja/nee): ")
    dienend = input("Dienend (ja/nee): ")
    technisch = input("Technisch (ja/nee): ")
    individueel = input("Individueel (ja/nee): ")
    karakter = input("Karakter (ja/nee): ")

    opmerkingen = input("Opmerkingen: ")

    rapport_dict = {"datum": datum, "wedstrijd": westrijd, "weerstand": weerstand, "speler": speler,
                "geboortedatum": geboortedatum, "club_team": club_team, "positie": positie, "bouw": bouw,
                    "handelingssnelheid": {"ASB": ASB, "AN": AN, "SCA": SCA, "OZ": OZ, "OS": OS,},
                    "tactisch": {"BSH": BSH, "ZCOM": ZCOM, "POS": POS, "LEZ": LEZ, "2eB": tweedeB,
                    "DRZ": DRZ, "B+/B-": Bplusmin, "B-/B+": Bminplus}, "extra": {"TG": TG, "SWL": SWL, "SWA/F": SWAF,
                    "JB": JB, "JT": JT, "TT": TT}, "motoriek": {"SMS": SMS, "KWD": KWD, "SH": SH, "SSH": SSH},
                "technisch": {"BC": BC, "PL": Pl, "PK": PK, "SCH": SCH, "VZET": VZET},
                    "voetbalhandeling": {"1-1A": eeneenA, "1-1V": eeneenV, "DBEW": DBEW, "KOPA": KOPA, "KOPV": KOPV,
                                         "DK": DK, "ZDIEP": ZDIEP, "VSB": VSB, "SVM": SVM, "BAL AF": BAL_AF},
                    "coachbaarheid": coachbaarheid, "inzet": inzet, "persoonlijkheid": persoonlijkheid, "houding": houding,
                    "zelfvertrouwen": zelfvertrouwen, "uithoudingsvermogen": uithoudingsvermogen, "sprongkracht": sprongkracht,
                    "gebruikt_lichaam": gebruikt_lichaam, "type_speler": {"teamspeler": teamspeler, "leider": leider,
                    "creatief": creatief, "dienend": dienend, "technisch": technisch, "individueel": individueel, "karakter": karakter},
                                                                          "opmerkingen": opmerkingen}

    if speler not in report_db:
        report_db[speler] = []
        report_db[speler].append(rapport_dict)
        print("Scoutingsrapport (volledig) toegevoegd.")

