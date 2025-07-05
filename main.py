from storage import load_data, save_data
from users import login
from players import add_player
from scouting import add_scouting_report, view_scouting_reports
from trainers import add_training_schedule, register_attendance
from technical import add_material

report_db = load_data('rapporten.json')
save_data(report_db, 'rapporten.json')

users_db = {"trainer1": {"password": "gehasht_wachtwoord", "role": "trainer"},
            "scout1": {"password": "gehasht_wachtwoord", "role": "scout"}}
players_db = {}
report_db = {}
schedules_db = {}
materials_db = {}


def main() :
    role = login(users_db)
    if not role:
        return
    while True:
        print("1. Speler toevoegen")
        print("2. Scoutingsrapport toevoegen")
        print("3. Rapporten bekijken")
        print("4. Trainingsschema toevoegen")
        print("5. Aanwezigheid registeren")
        print("6. Materiaal toevoegen")
        print("7. Stoppen")
        keuze = input("Maak een keuze: ")
        if keuze == "1":
            add_player(players_db)
        elif keuze == "2":
            add_scouting_report(report_db)
            pass
        elif keuze == "3":
            view_scouting_reports(report_db)
            pass
        elif keuze == "4":
            add_training_schedule(schedules_db)
            pass
        elif keuze == "5":
            register_attendance(schedules_db)
        elif keuze == "6":
            add_material(materials_db)
        elif keuze == "7":
            print("Programma gestopt.")
            break
        else:
            print("Ongeldige keuze, probeer opnieuw.")

if __name__ == "__main__":
    main()
