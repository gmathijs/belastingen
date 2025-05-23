def get_user_input():
    """
    Collect user input for Box 3 tax calculation.
    """
    input_data = {
        "opslagnaam": "belasting",
        "db_path": "mijn_belastingen.db",   # Path to the database
        "year": 2024,                       # Tax year
        "aftrek_eigenwoning": 0,                   # Aftrek eigen woning

        "spaargeld": 100,                   # Savings
        "belegging": 0,                     # Investments
        "ontroerend": 0,                    # Real estate
        "WOZ_Waarde": 0,                     # WOZ value of real estate
        "schuld": 0,                        # Aftrekbare schulden Box 3
        "dividend": 0,                      # Ingehouden dividend belasting


        "primary": {
            "naam": "Mevrouw Nix",           # Identificatie voor de eerste persoon
            "aow_er": 0,                    # AOW status (0 = geen AOW, 1 = AOW na 1946, 2 = AOW voor 1946)
            "heeft_partner": False,          # Whether you have a fiscal partner
            "Inkomen": 0,                   # Inkomen uit artbeid
            "Pensioen": 4499,              # Pensioen of uitkering
            "deel_box1": 1,                 # Deel box1 wat persoon voor zijn rekening neemt
            "deel_box3": 1,                 # Deel box3 wat persoon voor zijn rekening neemt
            "deel_div": 1,                  # Deel dividendbelasting wat persoon voor zijn rekening neemt 
            "al_ingehouden": 0,             # Ingehouden loonheffing optelsom van jaaropgaven 
            "voorlopige_aanslag": 0      # Betaalde voorlopige aanslag (+) = betaald (-) is teruggekregem 

        },
        "partner": {
            "naam": "Persoon 2",          # Identificatie voor de partner
            "aow_er": 1,                    # AOW status (0 = geen AOW, 1 = AOW na 1946, 2 = AOW voor 1946)
            "heeft_partner": True,          # Whether you have a fiscal partner
            "Inkomen": 10000,               # Inkomen uit artbeid
            "Pensioen": 15000,              # Pensioen of uitkering
            "al_ingehouden": 3000,          # Ingehouden loonheffing optelsom van jaaropgaven 
            "voorlopige_aanslag": 0         # Betaalde voorlopige aanslag          
        },
        "programsetting": {
            "programsetting_mode": 2                       # 1: Normal 2: Vindt optimale verdeling
        }
    }
    return input_data

def check_input(data):
    """Validate and enforce dependencies in input data."""

    # Ensure that if primary has a partner, partner data is provided
    if data["primary"]["heeft_partner"]:
        # Primary heeft partner
        if "partner" not in data:
            raise ValueError("Partner data is required when 'heeft_partner' is True.")   
        
        # Enforce deel_box1 dependency
        if "deel_box1" in data["primary"]:
            data["partner"]["deel_box1"] = 1 - data["primary"]["deel_box1"]
        else:
            # Default to 1 for primary and 1 for partner
            data["primary"]["deel_box1"] = 1.0
            data["partner"]["deel_box1"] = 0.0

        # Enforce deel_box3 dependency
        if "deel_box3" in data["primary"]:
            data["partner"]["deel_box3"] = 1 - data["primary"]["deel_box3"]
        else:
            # Default to 1 for primary and 1 for partner
            data["primary"]["deel_box3"] = 1.0
            data["partner"]["deel_box3"] = 0.0

        # Enforce deel_box3 dividend dependency
        if "deel_div" in data["primary"]:
            data["partner"]["deel_div"] = 1 - data["primary"]["deel_div"]
        else:
            # Default to 1 for primary and 1 for partner
            data["primary"]["deel_div"] = 1.0
            data["partner"]["deel_div"] = 0.0
    else: 
        # Geen partner
        data["primary"]["deel_box1"] = 1.0
        data["primary"]["deel_box3"] = 1.0
        data["primary"]["deel_div"] = 1.0

    return data
