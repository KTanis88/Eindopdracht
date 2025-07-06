from storage import load_data, save_data
from users import (load_users, save_users, login, create_user, change_password, delete_user, reset_password)
from roles import role_permissions, mag_toegang
from players import add_player
from scouting import add_scouting_report, view_scouting_reports
from trainers import add_training_schedule, register_attendance
from technical import add_material
from trainingsschema.loader import get_schema_path, open_schema

report_db = load_data('rapporten.json')
save_data(report_db, 'rapporten.json')

users_db = load_users()
players_db = {}
report_db = {}
schedules_db = {}
materials_db = {}


def main() :
    users_db = load_users()
    while True:
        print("\n1. Inloggen\n2. Stoppen")
        keuze = input("Maak een keuze: ")
        if keuze == "1":
            username, role = login(users_db)
            if not role:
                continue
            gebruiker = {"username": username, "role": role}
            gebruikersmenu(gebruiker, users_db)
        elif keuze == "2":
            print("App gestopt.")
            break
        else:
            print("Ongeldige keuze.")

def gebruikersmenu(gebruiker, users_db) :
    while True:
        mapping = toon_menu(gebruiker)
        keuze = input("Maak een keuze: ")
        actie = mapping.get(keuze)
        if actie == "create_user":
            create_user(users_db)
            save_users(users_db)
        elif actie == "rapportages":
            view_scouting_reports(report_db)
        elif actie == "trainingsschema":
            add_training_schedule(schedules_db)
        elif actie == "spelersgegevens":
            add_player(players_db)
        elif actie == "materiaalbeheer":
            add_material(materials_db)
        elif actie == "scoutingsverslagen":
           add_scouting_report(report_db)
        elif actie == "change_password":
            change_password(users_db, gebruiker["username"])
            save_users(users_db)
        elif actie == "delete_user":
            delete_user(users_db, current_user=gebruiker["username"])
            save_users(users_db)
        elif actie == "reset_password":
            reset_password(users_db)
            save_users(users_db)
        elif actie == 'logout':
            print("Uitgelogd.")
            break
        else:
            print("Ongeldige keuze of geen toegang.")
            save_users(users_db)

def toon_menu(gebruiker):
    role = gebruiker['role']
    permissions = role_permissions.get(role, {})
    menu = []
    mapping = {}
    nummer = 1

    if "gebruikersbeheer" in permissions.get("modules", []):
        menu.append(f"{nummer}. Gebruikersbeheer (nieuwe gebruiker aanmaken)")
        mapping[str(nummer)] = "create_user"
        nummer += 1
    if "rapportages" in permissions.get("modules", []):
        menu.append(f"{nummer}. Rapportages")
        mapping[str(nummer)] = "rapportages"
        nummer += 1
    if "trainingsschema" in permissions.get("modules", []):
        menu.append(f"{nummer}. Trainingsschema's")
        mapping[str(nummer)] = "trainingsschema"
        nummer += 1
    if "spelersgegevens" in permissions.get("modules", []):
        menu.append(f"{nummer}. Spelersgegevens")
        mapping[str(nummer)] = "spelersgegevens"
        nummer += 1
    if "materiaalbeheer" in permissions.get("modules", []):
        menu.append(f"{nummer}. Materiaalbeheer")
        mapping[str(nummer)] = "materiaalbeheer"
        nummer += 1
    if "scoutingsverslag" in permissions.get("modules", []):
        menu.append(f"{nummer}. Scoutingsverslagen")
        mapping[str(nummer)] = "scoutingsverslagen"
        nummer += 1

    menu.append(f"{nummer}. Wachtwoord wijzigen")
    mapping[str(nummer)] = "change_password"
    nummer += 1

    if "gebruikersbeheer" in permissions.get("modules", []):
        menu.append(f"{nummer}. Gebruiker verwijderen")
        mapping[str(nummer)] = "delete_user"
        nummer += 1
        menu.append(f"{nummer}. Wachtwoord resetten (andere gebruiker)")
        mapping[str(nummer)] = "reset_password"
        nummer += 1

    menu.append("0. Uitloggen")
    mapping["0"] = "logout"

    print("\nMenu voor rol:", role)
    for item in menu:
        print(item)
    return mapping

