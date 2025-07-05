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

