import csv

from urllib3.filepost import writer


def add_perfomance_report(perfomance_db):
    speler = input("Naam speler: ").strip()
    wedstrijd = input("Wedstrijd/training: ").strip()
    beoordeling = input("Beoordeling:").strip()
    opmerking = input("Opmerking: ").strip()
    rapport = {"wedstrijd": wedstrijd, "beoordeling": beoordeling, "opmerking": opmerking}
    if speler not in perfomance_db:
        perfomance_db[speler] = []
    perfomance_db[speler].append(rapport)
    print("Prestatieformulier toegevoegd.")

def export_perfomance_to_csv(perfomance_db, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["datum", "type_sessie", "speler", "cijfer", "opmerking"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for datum, sessies in perfomance_db.items():
            for type_sessie, sessie_data in sessies.items():
                prestaties = sessie_data.get("prestaties", {})
                for speler, prestatie in prestaties.item():
                    row = {"datum": datum, "type_sessie": type_sessie, "speler": speler, "cijfer": prestatie.get("cijfer", "ww"), "opmerking": prestatie.get("opmerking", "")}
                    writer.writerow(row)
    print(f"Perfomance-rapporten geexporteerd naar {filename}")