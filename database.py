import requests

sportslink_api_url = "https://api.sportslink.com/v1/teams"
api_key = "jouw_api_sleutel"

def fetch_teams():
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(sportslink_api_url, headers=headers)
    if response.status_code== 200:
        return response.json()
    else:
        print("Fout bij ophalen", response.status_code)
        return []

def import_teams_to_db(teams, teams_db):
    for team in teams:
        team_id = team["id"]
        if team_id not in teams_db:
            teams_db[team_id] = team
    print(f"{len(teams)} teams geimporteerd of bijgewerkt.")

def sync_teams_with_db(sportslink_teams, local_db, save_func, filename):
    sportslink_dict = {team["id"]: team for team in sportslink_teams}
    wijzigingen = []

    for team_id, team_data in sportslink_dict.items():
        if team_id not in local_db:
            print(f"Nieuw team toegevoegd: {team_data['name']}")
        elif local_db[team_id] != team_data:
            print(f"Team bijgewerkt: {team_data['name']}")
        local_db[team_id] = team_data

    to_remove = [team_id for team_id in local_db if team_id not in sportslink_dict]
    for team_id in to_remove:
        print(f"Team verwijderd: {local_db[team_id]['name']}")
        del local_db[team_id]

    save_func(local_db, filename)

    if wijzigingen:
        print("Wijzigingen tijdens synchronisatie:")
        for w in wijzigingen:
            print("-", w)
    else:
        print("Geen wijzigingen tijdens synchronisatie.")

    return wijzigingen

def fetch_players_from_sportslink(team_id):
    url = f"https://api.sportslink.com/v1/teams/{team_id}/players"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Fout bij het ophalen van spelers:", response.status_code)
        return []

def sync_players_with_db(sportslink_players, local_db, save_func, filename):
    sportslink_dict = {player["id"]: player for player in sportslink_players}
    wijzigingen = []

    for player_id, player_data in sportslink_dict.items():
        if player_id not in local_db:
            print(f"Nieuwe speler toegevoegd: {player_data['name']}")
        elif local_db[player_id] != player_data:
            print(f"Speler bijgewerkt: {player_data['name']}")
        local_db[player_id] = player_data
    to_remove = [player_id for player_id in local_db if player_id not in sportslink_dict]
    for player_id in to_remove:
        print(f"Speler verwijderd: {local_db[player_id]['name']}")
        del local_db[player_id]

    save_func(local_db, filename)

    if wijzigingen:
        print("Wijzigingen tijdens synchronisatie:")
        for w in wijzigingen:
            print("-", w)
    else:
        print("Geen wijzigingen tijdens synchronisatie.")

    return wijzigingen

def log_wijzigingen(wijzigingen, logbestand):
    with open(logbestand, "a") as f:
        for w in wijzigingen:
            f.write(w + "\n")



