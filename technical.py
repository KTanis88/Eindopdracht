def add_material(materials_db) :
    item = input("Materiaal: ")
    aantal = input("Aantal: ")
    if item in materials_db :
        materials_db[item] += aantal
    else:
        materials_db[item] = aantal
    print(f"{aantal} stuks {item} toegevoegd. Totaal nu: {materials_db[item]}")