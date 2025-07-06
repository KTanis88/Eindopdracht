role_permissions = {"admin": {"modules":["gebruikersbeheer", "rapportages", "trainingsschema", "spelersgegevens",
                                         "materiaalbeheer", "scoutingsverslag"], "rapport_types":["trainer",
                                         "scout", "hjo-breedte", "hjo-selectie", "tc_bovenbouw", "tc_middenbouw", "tc-onderbouw",
                                        "sectiehoofd_bovenbouw", "sectiehoofd_middenbouw", "sectiehoofd_onderbouw" ]},
                            "hjo-selectie": {"modules": ["rapportages", "trainingsschema", "spelersgegevens", "materiaalbeheer", "scoutingsverslag"],
                                             "rapport_types": ["trainer", "scout", "tc_bovenbouw", "tc_middenbouw", "tc_onderbouw",
                                                               "sectiehoofd_middenbouw", "sectiehoofd_bovenbouw", "sectiehoofd_onderbouw",
                                                               "hjo_selectie", "hjo_breedte"]},
"hjo-breedte": {"modules": ["rapportages", "trainingsschema", "spelersgegevens", "materiaalbeheer", "scoutingsverslag"],
                                             "rapport_types": ["trainer", "scout", "tc_bovenbouw", "tc_middenbouw", "tc_onderbouw",
                                                               "sectiehoofd_middenbouw", "sectiehoofd_bovenbouw", "sectiehoofd_onderbouw",
                                                               "hjo_selectie", "hjo_breedte"]},
                            "tc_bovenbouw": {"modules": ["rapportages", "trainingsschema", "spelersgegevens", "materiaalbeheer",
                                                "scoutingsverslag"], "rapport_types": ["trainer", "scout", "tc_bovenbouw", "sectiehoofd_bovenbouw"]},
                            "tc_middenbouw": {"modules": ["rapportages", "trainingsschema", "spelersgegevens", "materiaalbeheer"],
                             "rapport_types": ["trainer", "scout","tc_middenbouw", "sectiehoofd_middenbouw"]},
                    "tc_onderbouw": {
                        "modules": ["rapportages", "trainingsschema", "spelersgegevens", "materiaalbeheer"],
                        "rapport_types": ["trainer", "scout", "tc_onderbouw", "sectiehoofd_onderbouw"]},
                    "sectiehoofd_bovenbouw": {"modules": ["rapportages", "trainingsschema", "spelersgegevens", "materiaalbeheer", "scoutingsverslag"],
                                             "rapport_types": ["trainer", "scout", "tc_bovenbouw", "sectiehoofd_bovenbouw"]},
"sectiehoofd_middenbouw": {"modules": ["rapportages", "trainingsschema", "spelersgegevens", "materiaalbeheer", "scoutingsverslag"],
                                             "rapport_types": ["trainer", "scout", "tc_middenbouw", "sectiehoofd_middenbouw"]},
"sectiehoofd_onderbouw": {"modules": ["rapportages", "trainingsschema", "spelersgegevens", "materiaalbeheer", "scoutingsverslag"],
                                             "rapport_types": ["trainer", "scout", "tc_onderbouw", "sectiehoofd_onderbouw"]},
                    "scouts":{"modules": ["rapportages", "trainingsschema", "spelersgegevens", "materiaalbeheer", "scoutingsverslag"],
                                             "rapport_types": ["trainer", "scout", "tc_onderbouw"]},
                    "trainer":{"modules": ["rapportages", "trainingsschema", "spelersgegevens", "materiaalbeheer", "scoutingsverslag"],
                                             "rapport_types": ["trainer"]},
}

def mag_toegang(gebruiker, module, rapport_type=None) :
    role = gebruiker['role']
    permissions = role_permissions.get(role, {})
    if module in permissions.get("modules", []):
        if rapport_type is None:
            return True
        return rapport_type in permissions.get("rapport_types", [])
    return False