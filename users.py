import getpass
import hashlib

def hash_password(password) :
    return hashlib.sha256(password.encode()).hexdigest()

def login(users_db) :
    username = input("Gebruikersnaam: ")
    password = getpass.getpass("Wachtwoord: ")
    hashed = hash_password(password)
    if username in users_db and users_db[username]['password'] == hashed:
        print("Succesvol ingelogd!")
        return users_db[username]['role']
    else:
        print("Ongeldige inloggegevens.")
        return None
