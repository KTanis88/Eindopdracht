import csv

def add_training_schedule(schedules_db) :
    datum = input("Datum training: ")
    onderwerp = input("Onderwerp: ")
    if datum not in schedules_db :
        schedules_db[datum] = []
    schedules_db[datum].append(onderwerp)
    print("Trainingsschema toegevoegd.")

def register_attendance(schedules_db) :
    datum = input("Datum training (dd-mm-jjjj): ")
    speler = input("Naam speler: ")
    aanwezig = input("Aanwezig? (ja/nee):").lower() == "ja"
    if datum not in schedules_db :
        schedules_db[datum] = {}
    if "aanwezigheid" not in schedules_db[datum] :
        schedules_db[datum]['aanwezigheid'] = {}
    schedules_db[datum]['aanwezigheid'] [speler] = aanwezig
    print(f"Aanwezigheid voor {speler} op {datum} geregistreerd a;s {'aanwezig' if aanwezig else 'afwezig'}.")

def register_perfomance(schedules_db):
    datum = input("Datum (dd-mm-jjjj):")
    type_sessie = input("Type (training/wedstrijd):").lower()
    speler = input("Naam speler:")
    prestatie = input("Prestatie (bijv. cijfer of korte beoordeling):")

    if datum not in schedules_db:
        schedules_db[datum] = {}
    if type_sessie not in schedules_db[datum]:
        schedules_db[datum][type_sessie] = {"prestaties": {}}
    if "prestaties" not in schedules_db[datum][type_sessie]:
        schedules_db[datum][type_sessie]["prestaties"] = {}

    schedules_db[datum][type_sessie]["prestaties"][speler] = prestatie
    print(f"Prestatie voor {speler} op {datum} ({type_sessie}) geregistreerd als: {prestatie}")


def export_reports_to_csv(report_db, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["speler", "mentaliteit", "techniek", "beoordeling", "rapport"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for speler, rapporten in report_db.items():
            for rapport in rapporten:
                row = {"speler": speler}
                row.update(rapport)
                writer.writerow(row)

    print(f"Rapporten geexporteerd naar {filename}")