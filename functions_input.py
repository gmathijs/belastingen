def get_user_input():
    """
    Collect user input for Box 3 tax calculation.
    """
    input_data = {
        "db_path": "mijn_belastingen.db",   # Path to the database
        "year": 2024,                       # Tax year
        "aow_er": 1,                        # AOW status (0 = geen AOW, 1 = AOW na 1946, 2 = AOW voor 1946)
        "heeft_partner": True,              # Whether you have a fiscal partner
        "Inkomen": 50000,                   # Gross income
        "Pensioen": 0,                      # Pensioen of uitkering
        "spaargeld": 109929,                # Savings
        "belegging": 69569,                 # Investments
        "ontroerend": 43000,                # Real estate
        "schuld": 10000,                    # Debts
        "uw_deel": 1.0,                     # Your share of the assets (1.0 for full ownership)
        "WOZ_Waarde": 316000                # WOZ value of real estate
    }
    return input_data