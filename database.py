import csv
import requests
import os
import datetime

api_key = os.getenv("sportslink_api_key")
if not api_key:
    raise ValueError("Omgevingsvariabele 'sportslink_api_key' is niet gezet!")

def fetch_teams():
    """
    Haalt alle teams op via de Sportslink API.
    :return: list: Een lijst met teamgegevens (dicts) of een lege lijst bij een fout.
    """
    url = "https://api.sportslink.com/v1/teams"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code== 200:
            return response.json()
        else:
            print("Fout bij ophalen", response.status_code, response.text)
            return []
    except requests.RequestException as e:
        print(f"Netwerkfout bij ophalen teams: {e}")
        return []

def sync_teams_with_db(sportslink_teams, local_db, save_func, filename):
    """
    Synchroniseert Sportslink-teams met de lokale database.
    :param sportslink_teams (list): Lijst met teams van Sportslink.
    :param local_db (dict): Lokale database van teams (id -> dict).
    :param save_func (callable): Functie om de lokale database op te slaan.
    :param filename (str): Naam van het bestand waarin de database wordt opgeslagen.

    :return: list: Een lijst van tuples met het type wijziging en de omschrijving.
    """
    sportslink_dict = {team.get("id"): team for team in sportslink_teams if team.get('id')}
    wijzigingen = []
    for team_id, team_data in sportslink_dict.items():
        if team_id not in local_db:
            wijzigingen.append(("toegevoegd", f"Nieuw team toegevoegd: {team_data.get('name', 'onbekend')}"))
        elif local_db[team_id] != team_data:
            wijzigingen.append(("bijgewerkt",f"Team bijgewerkt: {team_data.get('name', 'onbekend')}"))
        local_db[team_id] = team_data
    to_remove = [team_id for team_id in local_db if team_id not in sportslink_dict]
    for team_id in to_remove:
        wijzigingen.append(("verwijderd", f"Team verwijderd: {local_db[team_id].get('name', 'onbekend')}"))
        del local_db[team_id]
    save_func(local_db, filename)
    if wijzigingen:
        print("Wijzigingen tijdens synchronisatie (teams):")
        for typ, w in wijzigingen:
            print(f"- [{typ}] {w}")
    else:
        print("Geen wijzigingen tijdens synchronisatie (teams).")
    return wijzigingen

def fetch_players_from_sportslink(team_id):
    """
    Haalt alle spelers van een team op via de Sportslink API.

    :param team_id (str): Het ID van het team waarvan de spelers opgehaald moeten worden.

    :return: list: Een lijst met spelersgegevens (dicts) of een lege lijst bij een fout.
    """
    url = f"https://api.sportslink.com/v1/teams/{team_id}/players"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print("Fout bij het ophalen van spelers:", response.status_code, response.text)
            return []
    except requests.RequestException as e:
        print(f"Netwerkfout bij ophalen spelers: {e}")
        return []

def sync_players_with_db(sportslink_players, local_db, save_func, filename):
    """
    Synchroniseert Sportslink-spelers met de lokale database.

    :param sportslink_players (list): Lijst met spelers van Sportslink.
    :param local_db (dict): Lokale database van spelers (id -> dict).
    :param save_func (callable): Functie om de lokale database op te slaan.
    :param filename (str): Naam van het bestand waarin de database wordt opgeslagen.

    :return: list: Een lijst van tuples met het type wijziging en de omschrijving.
    """
    sportslink_dict = {player.get("id"): player for player in sportslink_players if player.get('id')}
    wijzigingen = []
    for player_id, player_data in sportslink_dict.items():
        if player_id not in local_db:
            wijzigingen.append(("toegevoegd", f"Nieuwe speler toegevoegd: {player_data.get('name', 'onbekend')}"))
        elif local_db[player_id] != player_data:
            wijzigingen.append(("bijgewerkt", f"Speler bijgewerkt: {player_data.get('name', 'onbekend')}"))
        local_db[player_id] = player_data
    to_remove = [player_id for player_id in local_db if player_id not in sportslink_dict]
    for player_id in to_remove:
        wijzigingen.append(("verwijderd", f"Speler verwijderd: {local_db[player_id].get('name', 'onbekend')}"))
        del local_db[player_id]
    save_func(local_db, filename)
    if wijzigingen:
        print("Wijzigingen tijdens synchronisatie (spelers):")
        for typ, w in wijzigingen:
            print(f"- [{typ}] {w}")
    else:
        print("Geen wijzigingen tijdens synchronisatie (spelers).")
    return wijzigingen

def log_wijzigingen(wijzigingen, logmap, prefix="wijzigingen"):
    """
    Logt alle wijzigingen naar een CSV-bestand in de opgegeven map met tijdstempel.

    :param wijzigingen (list): Lijst van tuples met (type, omschrijving) van de wijziging.
    :param logmap (str): Map waarin het logbestand wordt opgeslagen.
    :param prefix (str): Optioneel, prefix voor de bestandsnaam.

    :return: None
    """

    os.makedirs(logmap, exist_ok=True)
    datum = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    logbestand= os.path.join(logmap, f"{prefix}_{datum}.csv")
    with open(logbestand, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Tijd", "Type", "Omschrijving"])
        for typ, w in wijzigingen:
            writer.writerow([datetime.datetime.now().isoformat(), typ, w])




