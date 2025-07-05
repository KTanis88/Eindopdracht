def add_scouting_report(report_db) :
    speler = input("Naam speler:").strip()
    if not speler:
        print("Naam mag niet leeg zijn.")
        return
    beoordeling = input("Beoordeling:").strip()
    if not beoordeling:
        print("Beoordeling mag niet leeg zijn.")
        return
    rapport = input("Observaties:").strip()
    if not rapport:
        print("Observaties mogen niet leeg zijn.")
        return

    rapport_dict = {"beoordeling": beoordeling, "rapport": rapport}
    if speler not in report_db:
       report_db[speler] = []
    report_db[speler].append(rapport_dict)
    print("Scoutingsrapport toegevoegd.")

def view_scouting_reports(report_db) :
    speler = input("Naam speler waarvan je rapporten wilt zien: ")
    if speler in report_db and report_db[speler]:
        print(f"Rapporten voor {speler}:")
        for idx, rapport in enumerate(report_db[speler], 1) :
            print(f"\nRapport {idx}:")
            print(f"Beoordeling: {rapport['beoordeling' ]}")
            print(f"Observaties: {rapport['rapport']}")
    else:
        print("Geen rapporten gevonden voor deze speler.")



