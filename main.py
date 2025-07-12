from database import (fetch_teams, fetch_players_from_sportslink, sync_teams_with_db, sync_players_with_db, log_wijzigingen)
from storage import load_data, save_data
from matches import (fetch_matches_from_sportslink, fetch_schedule_from_sportslink, sync_matches_with_db, sync_schedule_with_db)
from users import (load_users, save_users, login, create_user, change_password, delete_user, reset_password)
from roles import role_permissions, mag_toegang
from players import add_player
from scouting import add_scouting_report, view_scouting_reports
from trainers import add_training_schedule, register_attendance
from technical import add_material, create_team_indeling, view_team_indelingen, export_teamindelingen_to_csv
from trainingsschema.loader import get_schema_path, open_schema



report_db = load_data('rapporten.json')
save_data(report_db, 'rapporten.json')

teamindelingen_db = load_data('teamindelingen.json')
users_db = load_users()
players_db = load_data('players.json')
teams_db = load_data('teams.json')
schedules_db = load_data('schedules.json')
materials_db = {}
matches_db = load_data('matches.json')

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
        elif actie == "teamindeling":
            while True:
                print("/nTeamindelingen-menu: ")
                print("1. Nieuwe teamindeling aanmaken")
                print("2. Teamindelingen bekijken")
                print("3. Teamindelingen exporteren naar CSV")
                print("0. Terug")
                keuze = input("Maak een keuze: ")
                if keuze == "1":
                    create_team_indeling(teams_db, players_db, teamindelingen_db)
                    save_data(teamindelingen_db, 'teamindelingen.json')
                elif keuze == "2":
                    view_team_indelingen(teamindelingen_db)
                elif keuze == "3":
                    export_teamindelingen_to_csv(teamindelingen_db)
                elif keuze == "0":
                    break
                else:
                    print("Ongeldige keuze.")
        elif actie == "import_sportslink":
            print("Start Sportslink synchronisatie...")
            sportslink_teams = fetch_teams()
            wijzigingen_teams = sync_teams_with_db(sportslink_teams, teams_db, save_data, 'teams.json')
            if wijzigingen_teams:
                log_wijzigingen(wijzigingen_teams, "logs", prefix="teams")
            for team in sportslink_teams:
                team_id = team.get("id")
                if not team_id:
                    continue
                sportslink_players = fetch_players_from_sportslink(team_id)
                wijzigingen_spelers = sync_players_with_db(sportslink_players, players_db, save_data,'players.json')
                if wijzigingen_spelers:
                    log_wijzigingen(wijzigingen_spelers, "logs", prefix="spelers")
                sportslink_matches = fetch_matches_from_sportslink(team_id)
                wijzigingen_matches = sync_matches_with_db(sportslink_matches, matches_db, save_data, 'matches.json')
                if wijzigingen_matches:
                    log_wijzigingen(wijzigingen_matches, "logs", prefix="wedstrijden")
                sportslink_schedule = fetch_schedule_from_sportslink(team_id)
                wijzigingen_schedule = sync_schedule_from_sportslink(sportslink_schedule, schedules_db, save_data, "schedules.json")
                if wijzigingen_schedule:
                    log_wijzigingen(wijzigingen_schedule, "logs", prefix="schema's")
            print("Sportslink synchronisatie voltooid.")
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
    if "teamindeling" in permissions.get("modules", []):
        menu.append(f"{nummer}. Teamindelingen beheren")
        mapping[str(nummer)] = "teamindeling"
        nummer += 1

    menu.append(f"{nummer}. Importeer teams en spelers uit Sportslink")
    mapping[str(nummer)] = "import_sportslink"
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

