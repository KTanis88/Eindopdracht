import csv
import requests
import os
import datetime

api_key = os.getenv("sportslink_api_key")
if not api_key:
    raise ValueError("Omgevingsvariabele 'sportslink_api_key' is niet gezet!")

def fetch_matches_from_sportslink(team_id):
    """
    Haalt alle wedstrijden van een specifiek team op via de Sportslink API.
    :param team_id (str): Het ID van het team waarvan de wedstrijden opgehaald moeten worden.
    :return: list: Een lijst met wedstrijdgegevens (dicts) of een lege lijst bij een fout.
    """
    url = f"https://api.sportslink.com/v1/teams/{team_id}/matches"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print("Fout bij ophalen", response.status_code, response.text)
            return []
    except requests.RequestException as e:
            print(f"Netwerkfout bij ophalen wedstrijden: {e}")
            return []

def fetch_schedule_from_sportslink(team_id):
    """
    Haalt het speelschema van een specifiek team op via de Sportslink API.
    :param team_id (str): Het ID van het team waarvan het speelschema opgehaald moet worden.
    :return: list: Een lijst met speelschema-gegevens (dicts) of een lege lijst bij een fout.
    """
    url = f"https://api.sportslink.com/v1/teams/{team_id}/schedule"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print("Fout bij ophalen", response.status_code, response.text)
            return []
    except requests.RequestException as e:
        print(f"Netwerkfout bij ophalen programma: {e}")
        return []

def sync_matches_with_db(sportslink_matches, local_db, save_func, filename):
    """
    Synchroniseert de opgehaalde Sportslink-wedstrijden met de lokale database.
    :param sportslink_matches (list): Lijst met wedstrijden van Sportslink
    :param local_db (dict): Lokale database van wedstrijden (id -> dict).
    :param save_func (callable): Functie om de lokale database op te slaan.
    :param filename (str): Naam van het bestand waarin de database wordt opgeslagen.
    :return: list: Een lijst van tuples met het type wijziging en de omschrijving.
    """
    sportslink_dict = {match.get('id'): match for match in sportslink_matches if match.get('id')}
    wijzigingen = []
    for match_id, match_data in sportslink_dict.items():
        if match_id not in local_db:
            wijzigingen.append(("toegevoegd", f"Nieuwe wedstrijd toegevoegd: {match_data.get('opponent', 'onbekend')}"))
        elif local_db[match_id] != match_data:
            wijzigingen.append(("bijgewerkt", f"Wedstrijd bijgewerkt: {match_data.get('opponent', 'onbekend')}"))
        local_db[match_id] = match_data
    to_remove = [match_id for match_id in local_db if match_id not in sportslink_dict]
    for match_id in to_remove:
        wijzigingen.append(("verwijderd", f"Wedstrijd verwijderd: {local_db[match_id].get('opponent', 'onbekend')}"))
        del local_db[match_id]
    save_func(local_db, filename)
    if wijzigingen:
        print("Wijzigingen tijdens synchronisatie (wedstrijden):")
        for typ, w in wijzigingen:
            print(f"- [{typ}] {w}")
    else:
        print("Geen wijzigingen tijdens synchronisatie (wedstrijden)")
    return wijzigingen


def sync_schedule_with_db(sportslink_schedule, local_db, save_func, filename):
    """
    Synchroniseert het speelschema van Sportslink met de lokale database.

    :param sportslink_schedule (list): Lijst met schema-items van Sportslink.
    :param local_db (dict): Lokale database van schema's (id -> dict).
    :param save_func (callable): Functie om de lokale database op te slaan.
    :param filename (str): Naam van het bestand waarin de database wordt opgeslagen.

    :return: list: Een lijst van tuples met het type wijziging en de omschrijving
    """
    sportslink_dict = {item.get("id"): item for item in sportslink_schedule if item.get("id")}
    wijzigingen = []
    for item_id, item_data in sportslink_dict.items():
        if item_id not in local_db:
            wijzigingen.append(("toegevoegd", f"Nieuw schema-item toegevoegd: {item_data.get('omschrijving', item_data.get('opponent', 'onbekend'))}"))
        elif local_db[item_id] != item_data:
            wijzigingen.append(("bijgewerkt", f"Schema-item bijgewerkt: {item_data.get('omschrijving', item_data.get('opponent', 'onbekend'))}"))
        local_db[item_id] = item_data
    to_remove = [item_id for item_id in local_db if item_id not in sportslink_dict]
    for item_id in to_remove:
         omschrijving = local_db[item_id].get('omschrijving', local_db[item_id].get('opponent', 'onbekend'))
         wijzigingen.append(("verwijderd", f"Schema-item verwijderd: {omschrijving}"))
         del local_db[item_id]
    save_func(local_db, filename)
    if wijzigingen:
        print("Wijzigingen tijdens synchronisatie (schema):")
        for typ, w in wijzigingen:
                print(f"- [{typ}] {w}")
    else:
            print("Geen wijzingen tijdens synchronisatie (schema)")
    return wijzigingen


def log_wijzigingen(wijzigingen, logmap):
    """
    Logt alle wijzigingen naar een CSV-bestand in de opgegeven map met tijdstempel.
    :param wijzigingen (list): Lijst van tuples met (type, omschrijving) van de wijziging.
    :param logmap (str): Map waarin het logbestand wordt opgeslagen.
    :return: None
    """
    os.makedirs(logmap, exist_ok=True)
    datum = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    logbestand = os.path.join(logmap, f"wijzigingen_{datum}.csv")
    with open(logbestand, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Tijd", "Type", "Omschrijving"])
        for typ, w in wijzigingen:
            writer.writerow([datetime.datetime.now().isoformat(), typ, w])
