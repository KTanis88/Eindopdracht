def add_player(players_db) :
    naam = input("Naam speler: ")
    geboortedatum = input("Geboortedatum (dd-mm-jjjj): ")
    positie = input("Positie: ")
    players_db[naam] = {"geboortedatum": geboortedatum,
                        "positie": positie}
    print(f"Speler {naam} toegevoegd.")

def search_player(players_db) :
    naam = input("Naam speler: ")
    if naam in players_db :
        print(players_db[naam])
    else:
        print("Speler niet gevonden.")