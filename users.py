import getpass
import bcrypt
import json
import re
from datetime import datetime

def hash_password(password) :
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login(users_db) :
    username = input("Gebruikersnaam: ")
    password = getpass.getpass("Wachtwoord: ")
    user = users_db.get(username)
    if user and check_password(password, user['password']):
        print("Succesvol ingelogd!")
        log_action("Succesvol ingelogd", username)
        return username, user['role']
    else:
        print("Ongeldige inloggegevens.")
        return None, None

def create_user(users_db) :
    username = input("Nieuwe gebruikersnaam:")
    if username in users_db:
        print("Gebruiker bestaat al.")
        return
    while True:
        password1 = getpass.getpass("Wachtwoord:")
        password2 = getpass.getpass("Herhaal wachtwoord:")
        if password1 != password2:
            print("Wachtwoorden komen niet overeen. Probeer opnieuw.")
            continue
        if not is_strong_password(password1):
            continue
        break
    role = input("Rol (bijv. trainer, scout):")
    users_db[username] = {"password": hash_password(password1), "role": role}
    print(f"Gebruiker {username} aangemaakt met rol {role}")
    log_action("Gebruiker aangemaakt", username)
    save_users(users_db)

def load_users(filename='users.json'):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users_db, filename='users.json'):
    with open(filename, 'w') as f:
        json.dump(users_db, f, indent=2)

def is_strong_password(password):
    if len(password) < 8 :
        print("Wachtwoord moet minimaal 8 tekens bevatten.")
        return False
    if not re.search(r"[A-Z]", password):
        print("Wachtwoord moet een hoofdletter bevatten.")
        return False
    if not re.search(r"[a-z]", password):
        print("Wachtwoord moet een kleine letter bevatten.")
        return False
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        print("Wachtwoord moet een speciaal teken bevatten.")
        return False
    return True

def change_password(users_db, username) :
    user = users_db.get(username)
    if not user:
        print("Gebruiker niet gevonden.")
        return
    old_password = getpass.getpass("Oud wachtwoord:")
    if not check_password(old_password, user['password']):
        print("Oud wachtwoord is onjuist.")
        return
    while True:
        new_password1 = getpass.getpass("Nieuw wachtwoord:")
        new_password2 = getpass.getpass("Herhaal nieuw wachtwoord:")
        if new_password1 != new_password2:
            print("Wachtwoorden komen niet overeen. Probeer opnieuw")
            continue
        if not is_strong_password(new_password1):
            continue
        break
    user['password'] = hash_password(new_password1)
    print("Wachtwoord succesvol gewijzigd.")
    log_action("Wachtwoord gewijzigd", username)
    save_users(users_db)

def delete_user(users_db, current_user=None) :
    username = input("Gebruikersnaam om te verwijderen:")
    if username == current_user:
        print('Je kunt jezelf niet verwijderen, terwijl je bent ingelogd.')
        return
    if username not in users_db:
        print("Gebruiker bestaat niet.")
        return
    bevestig = input(f"Weet je zeker dat je '{username}' wilt verwijderen? (ja/nee):").lower()
    if bevestig == "ja":
        del users_db[username]
        print(f"Gebruiker '{username}' is verwijderd.")
        save_users(users_db)
        log_action("Gebruiker verwijderd", username)
    else:
        print("Verwijderen geannuleerd.")

def reset_password(users_db) :
    username = input("Gebruikersnaam voor reset: ")
    if username not in users_db:
        print("Gebruiker bestaat niet.")
        return
    while True:
        new_password1 = getpass.getpass("Nieuw wachtwoord:")
        new_password2 = getpass.getpass("Herhaal nieuw wachtwoord:")
        if new_password1 != new_password2:
            print("Wachtwoorden komen niet overeen. Probeer opnieuw.")
            continue
        if not is_strong_password(new_password1):
            continue
        break
    users_db[username]['password'] = hash_password(new_password1)
    print(f"Wachtwoord voor '{username}' is gereset.")
    log_action("Wachtwoord gereset door beheerder.", username)
    save_users(users_db)

def log_action(action, username):
    tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("gebruikers_log.txt", "a") as f:
        f.write(f"[{tijd}] {username} : {action}\n")