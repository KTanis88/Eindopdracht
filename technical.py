import csv

def add_material(materials_db) :
    item = input("Materiaal: ")
    aantal = input("Aantal: ")
    if item in materials_db :
        materials_db[item] += aantal
    else:
        materials_db[item] = aantal
    print(f"{aantal} stuks {item} toegevoegd. Totaal nu: {materials_db[item]}")

def create_team_indeling(teams_db, players_db, teamindelingen_db):
    """
    Maakt een nieuwe teamindeling aan.
    :param teams_db:
    :param players_db:
    :param teamindelingen_db:
    :return:
    """
    teamnaam = input("Teamnaam: ").strip()
    if not teamnaam:
        print("Teamnaam mag niet leeg zijn.")
        return

    teamleden = []
    while True:
        speler = input("Voeg speler toe aan team (of druk Enter om te stoppen.").strip()
        if not speler:
            break
        if speler not in players_db:
            print("Speler niet gevonden in spelersdatabase.")
            continue
        teamleden.append(speler)

    if not teamleden:
        print("Geen spelers toegevoegd.")
        return

    teamindelingen_db[teamnaam] = teamleden
    print(f"Team '{teamnaam}' aangemaakt met {len(teamleden)} spelers.")

def view_team_indelingen(teamindelingen_db):
    """
    Toont alle teamindelingen.
    :param teamindelingen_db:
    :return:
    """
    if not teamindelingen_db:
        print("Geen teamindelingen gevonden.")
        return

    for team, spelers in teamindelingen_db.items():
        print(f"\nTeam: {team}")
        for speler in spelers:
            print(f"- {speler}")

def export_teamindelingen_to_csv(teamindelingen_db, filename="teamindelingen.csv"):
    """
    Exporteert alle teamindelingen naar een CSV-bestand.
    :param teamindelingen_db:
    :param filename:
    :return:
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Team", "Speler"])
        for team, spelers in teamindelingen_db.items():
            for speler in spelers:
                writer.writerow([team, speler])
    print(f"Teamindelingen geexporteerd naar {filename}")