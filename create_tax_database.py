import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('mijn_belastingen.db')
cursor = conn.cursor()

# Drop existing tables if they exist (to overwrite data)
cursor.execute("DROP TABLE IF EXISTS tax_loonheffing")
cursor.execute("DROP TABLE IF EXISTS tax_heffingskorting")
cursor.execute("DROP TABLE IF EXISTS tax_arbeidskorting")
cursor.execute("DROP TABLE IF EXISTS tax_vermogensbelasting")
cursor.execute("DROP TABLE IF EXISTS tax_premies_volksverzekeringen")
cursor.execute("DROP TABLE IF EXISTS tax_box3")
cursor.execute("DROP TABLE IF EXISTS tbl_eigenwoningforfait")
cursor.execute("DROP TABLE IF EXISTS tbl_ouderenkorting")
cursor.execute("DROP TABLE IF EXISTS tbl_tarief_aanpassing")



# Create the tax_loonheffing table
cursor.execute("""
    CREATE TABLE tax_loonheffing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        bracket_number INTEGER NOT NULL,
        lower_limit REAL NOT NULL,
        upper_limit REAL NOT NULL,
        tax_rate REAL NOT NULL,
        AOW_age INTEGER NOT NULL
    )
""")

# Create the tax_heffingskorting table
cursor.execute("""
    CREATE TABLE tax_heffingskorting (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        bracket_number INTEGER NOT NULL,
        lower_limit REAL NOT NULL,
        upper_limit REAL NOT NULL,
        base_credit REAL NOT NULL,
        credit_percentage REAL NOT NULL,
        AOW_age INTEGER NOT NULL            
    )
""")

# Create the tax_arbeidskorting table
cursor.execute("""
    CREATE TABLE tax_arbeidskorting (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        bracket_number INTEGER NOT NULL,
        lower_limit REAL NOT NULL,
        upper_limit REAL NOT NULL,
        base_credit REAL NOT NULL,
        credit_percentage REAL NOT NULL,
        AOW_age INTEGER NOT NULL      
    )
""")

# Create the tax_vermogensbelasting table
cursor.execute("""
    CREATE TABLE tax_vermogensbelasting (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        asset_type TEXT NOT NULL,
        lower_limit REAL NOT NULL,
        upper_limit REAL NOT NULL,
        tax_rate REAL NOT NULL 
    )
""")

# Create tax_premies_volksverzekeringen table
cursor.execute("""
    CREATE TABLE tax_premies_volksverzekeringen (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        aow_tarief REAL NOT NULL,
        anw_tarief REAL NOT NULL,
        wlz_tarief REAL NOT NULL,
        maximaal_inkomen REAL NOT NULL,
        aow_age INTEGER NOT NULL
    )
""")


# Create the tax_box3 table
cursor.execute("""
    CREATE TABLE tax_box3 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        perc_spaargeld REAL NOT NULL,
        perc_belegging REAL NOT NULL,
        perc_schuld REAL NOT NULL,
        perc_box3 REAL NOT NULL,
        heffingsvrij_vermogen REAL NOT NULL,  
        drempel_schuld REAL NOT NULL
    )
""")

# Create the table eigenwoning forfait
cursor.execute("""
    CREATE TABLE tbl_eigenwoningforfait (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        schijf_no INTEGER NOT NULL,
        limit_WOZ REAL NOT NULL,
        percentage REAL NOT NULL,
        bedrag REAL NOT NULL
    );
""")



# Create the table ouderenkorting forfait
cursor.execute("""
    CREATE TABLE tbl_ouderenkorting (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        schijf_no INTEGER NOT NULL,
        lower_limit REAL NOT NULL,
        upper_limit REAL NOT NULL,
        bedrag REAL NOT NULL,
        perc REAL NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_tarief_aanpassing (
        year INTEGER,
        income_threshold REAL,
        percentage REAL
    )
""")

# Insert data into the tax_loonheffing table (example for 2023)
tax_loonheffing_data = [
    # 2019 drie schalen
    (2019, 1,     0,  20384, 0.3665,  0),
    (2019, 2, 20385,  68507, 0.3810,  0),
    (2019, 3, 68508, 999999, 0.5175,  0),
    # 2019 AOW after  1 Januari 1946
    (2019, 1,     0,  20384, 0.1875,  1),
    (2019, 2, 20385,  34817, 0.2020,  1),
    (2019, 3, 34818,  68507, 0.3810,  1),
    (2019, 4, 68508, 999999, 0.5175,  1),
    # 2019 AOW before  1 Januari 1946
    (2019, 1,     0,  20384, 0.1875,  2),
    (2019, 2, 20385,  34817, 0.2020,  2),
    (2019, 3, 34818,  68507, 0.3810,  2),
    (2019, 4, 68508, 999999, 0.5175,  2),

    # 2020 2 schalen========================
    (2020, 1,     0,  68507, 0.3735, 0),
    (2020, 2, 68508, 999999, 0.4950, 0),

    (2020, 1,     0,  35375, 0.1945, 1),
    (2020, 2, 35376,  68507, 0.3735, 1),
    (2020, 3, 68508, 999999, 0.4950, 1),


    (2020, 1,     0,  34712, 0.1945, 2),
    (2020, 2, 34713,  68507, 0.3735, 2),
    (2020, 3, 68508, 999999, 0.4950, 2),

    # 2021 twee schalen
    (2021, 1,     0,  68507, 0.3710,  0),
    (2021, 2, 68508, 999999, 0.4950,  0),

    (2021, 1,     0,  35129, 0.1902,  1),
    (2021, 2, 35130,  68507, 0.3710,  1),
    (2021, 3, 68508, 999999, 0.4950,  1),

    (2021, 1,     0,  35941, 0.1902,  2),
    (2021, 2, 35942,  68507, 0.3710,  2),
    (2021, 3, 68508, 999999, 0.4950,  2),

    # 2022
    (2022, 1,     0,  69398, 0.3707, 0),
    (2022, 2, 69399, 999999, 0.4950, 0),

    (2022, 1,     0,  35472, 0.1902, 1),
    (2022, 2, 35473,  69398, 0.3707, 1),   
    (2022, 3, 69399, 999999, 0.4950, 1),

    (2022, 1,     0,  36409, 0.1902, 2),
    (2022, 2, 36410,  69398, 0.3707, 2),   
    (2022, 3, 69399, 999999, 0.4950, 2),

    # 2023
    (2023, 1,     0,  73030, 0.3693,  0),
    (2023, 2, 73031, 999999,  0.495,  0),

    (2023, 1,     0,  37149, 0.1903,  1),
    (2023, 2, 37150,  73030, 0.3693,  1),
    (2023, 3, 73031, 999999, 0.495,   1),

    (2023, 1,     0,  38702, 0.1903,  2),
    (2023, 2, 38703,  73030, 0.3693,  2),
    (2023, 3, 73031, 999999, 0.4950,  2),

    #2024  Niet in de AOW
    (2024, 1,     0,   75517, 0.3697, 0),
    (2024, 2, 75518, 9999999, 0.4950, 0),

    #2024 AOW After 1 januari 1946
    (2024, 1,     0,   38098, 0.1907,  1),
    (2024, 2, 38098,   75517, 0.3697,  1),
    (2024, 3, 75518, 9999999, 0.4950,  1),

    #2024 AOW before 1 januari 1946
    (2024, 1,     0,   40021,   0.1907, 2),
    (2024, 2, 40021,   75518,   0.3697, 2),  
    (2024, 3, 75518, 9999999,   0.4950, 2),

    # Bron: Bijlage bij de Nieuwsbrief Loonheffingen 2025
    # 12 December 2024
    #2024  Niet in de AOW
    (2025, 1,     0,   38441, 0.3582, 0),
    (2025, 2, 38441,   76817, 0.3748, 0),
    (2025, 3, 76817, 9999999, 0.4950, 0),

    #2024 AOW After 1 januari 1946
    (2025, 1,     0,   38441, 0.1792,  1),
    (2025, 2, 38441,   76817, 0.3748,  1),
    (2025, 3, 76817, 9999999, 0.4950,  1),

    #2024 AOW before 1 januari 1946
    (2025, 1,     0,   40502,   0.1792, 2),
    (2025, 2, 40502,   76817,   0.3748, 2),
    (2025, 3, 76817, 9999999,   0.4950, 2)

]

cursor.executemany("""
    INSERT INTO tax_loonheffing (year, bracket_number, lower_limit, upper_limit, tax_rate, aow_age)
    VALUES (?, ?, ?, ?, ?, ?)
""", tax_loonheffing_data)

# Insert data into the tax_heffingskorting table (example for 2023)
tax_heffingskorting_data = [
    # 2019
    (2019, 1,     0,    20384, 2477,        0, 0),
    (2019, 2, 20384,    68507, 2477, -0.05147, 0),
    (2019, 3, 68507, 99999999,     0,       0, 0),

    (2019, 1,     0,    20384, 1268,        0,  1),
    (2019, 2, 20384,    68507, 1268, -0.02633,  1),
    (2019, 3, 68507, 99999999,    0,        0,  1),

    # 2020
    (2020, 1,     0,     20711, 2711,        0,  0),
    (2020, 2, 20711,     68508, 2711, -0.05672,  0),
    (2020, 3, 68508,  99999999,    0,        0,  0),

    (2020, 1,     0,     20711, 1413,        0,  1),
    (2020, 2, 20711,     68508, 1413, -0.02954,  1),
    (2020, 3, 68508,   99999999,    0,       0,  1),

    # 2021
    (2021, 1,     0,      21044,  2837,        0,  0),
    (2021, 2, 21044,       68508, 2837, -0.05977,  0),
    (2021, 3, 68508,    99999999,    0,       0,   0),
    # 2021 AOW Leeftijd
    (2021, 1,     0,       21044, 1469,        0,  1),
    (2021, 2, 21044,       68508, 1469, -0.03093,  1),
    (2021, 3, 68508,    99999999,    0,        0,  1),

    # 2022
    (2022, 1,     0,    21317, 2888,        0,  0),
    (2022, 2, 21317,    69398, 2888, -0.06007,  0),
    (2022, 3, 69398,  99999999,   0,        0,  0),
    # 2022 AOW Leeftijd
    (2022, 1,     0,    21317,  1494,        0,  1),
    (2022, 2, 21317,    69398,  1494, -0.03106,  1),
    (2022, 3, 69398, 99999999,     0,        0,  1),

    # 2023
    (2023, 1,     0,    22661, 3070,       0,   0),
    (2023, 2, 22661,    73030, 3070, -0.06095,  0),
    (2023, 3, 73031,  99999999,   0,        0,  0),

    # 2023 AOW Leeftijd
    (2023, 1,     0,     22661, 1583,        0,  1),
    (2023, 2, 22661,     73030, 1583, -0.03141,  1),
    (2023, 3, 73031,  99999999,    0,        0,  1),

    # 2024
    (2024, 1,     0,    24813, 3362,        0,  0),
    (2024, 2, 24813,    75518, 3362, -0.06630,  0),
    (2024, 3, 75518, 99999999,    0,        0,  0),

    # 2024 AOW Leeftijd
    (2024, 1,     0,    24813, 1735,        0,  1),
    (2024, 2, 24813,    75518, 1735, -0.03421,  1),
    (2024, 3, 75518, 99999999,    0,        0,  1),

    # 2025 Bron: Zie loonhefing eerste tabel
    (2025, 1,     0,    28406, 3068,        0,  0),
    (2025, 2, 28406,    76817, 3068, -0.06337,  0),
    (2025, 3, 76817, 99999999,    0,        0,  0),

    # 2025 AOW Leeftijd
    (2025, 1,     0,    28406, 1536,        0,  1),
    (2025, 2, 28406,    76817, 1536, -0.03170,  1),
    (2025, 3, 76817, 99999999,    0,        0,  1)
]

cursor.executemany("""
    INSERT INTO tax_heffingskorting (year, bracket_number, lower_limit, upper_limit, base_credit, credit_percentage, aow_age)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", tax_heffingskorting_data)

# Insert data into the tax_arbeidskorting table (2019–2023)
tax_arbeidskorting_data = [
    # 2019
    (2019, 1,      0,      9694,    0,  0.01754, 0),
    (2019, 2,   9694,     20940,  170,  0.28712, 0),
    (2019, 3,  20940,     34060, 3399,        0, 0),
    (2019, 4,  34060,     90710, 3399,    -0.06, 0),
    (2019, 5,  90711, 999999999,    0,        0, 0),
    # 2019 AOW 
    (2019, 1,      0,      9694,    0,  0.00898, 1),
    (2019, 2,   9694,     20940,   88,  0.14689, 1),
    (2019, 3,  20940,     34060, 1740,        0, 1),
    (2019, 4,  34060,     90710, 1740, -0.03069, 1),
    (2019, 5,  90711, 999999999,    0,        0, 1),    

    # 2020
    (2020, 1,      0,      9921,    0,  0.02812, 0),
    (2020, 2,   9921,     21430,  279,  0.28812, 0),
    (2020, 3,  21430,     34954, 3595,  0.01656, 0),
    (2020, 4,  34954,     98604, 3819,    -0.06, 0),
    (2020, 5,  98604, 999999999,    0,        0, 0),
    # 2021 AOW
    (2020, 1,      0,      9921,    0,  0.01464, 1),
    (2020, 2,   9921,     21430,  279,  0.15004, 1),
    (2020, 3,  21430,     34954, 3595,  0.00862, 1),
    (2020, 4,  34954,     98604, 3819, -0.03124, 1),
    (2020, 5,  98604, 999999999,    0,        0, 1),

    # 2021
    (2021, 1,      0,     10109,    0,  0.02813, 0),
    (2021, 2,  10109,     21836,  463,  0.28771, 0),
    (2021, 3,  21836,     35653, 3873,  0.02663, 0),
    (2021, 4,  35653,    105737, 4205,    -0.06, 0),
    (2021, 5, 105737, 999999999,    0,        0, 0),
    # 2021 AOW
    (2021, 1,      0,     10109,    0,  0.02371, 1),
    (2021, 2,  10109,     21836,  463,  0.14890, 1),
    (2021, 3,  21836,     35653, 3873,  0.01378, 1),
    (2021, 4,  35653,    105737, 4205, -0.03105, 1),
    (2021, 5, 105737, 999999999,    0,        0, 1),

    # 2022
    (2022, 1,      0,     10350,    0,  0.04541, 0),
    (2022, 2,  10350,     22357,  470,  0.28461, 0),
    (2022, 3,  22357,     36650, 3887,  0.02610, 0),
    (2022, 4,  36650,    109347, 4260, -0.05860, 0),
    (2022, 5, 109347, 999999999,    0,        0, 0),
    # 2022 AOW
    (2022, 1,      0,     10350,    0,  0.02348, 1),
    (2022, 2,  10350,     22357,  244,  0.14718, 1),
    (2022, 3,  22357,     36650, 2011,  0.01349, 1),
    (2022, 4,  36650,    109347, 2204, -0.03030, 1),
    (2022, 5, 109347, 999999999,    0,        0, 1),

    # 2023
    (2023, 1,      0,     10741,    0,  0.08231, 0),
    (2023, 2,  10741,     23201,  884,  0.29861, 0),
    (2023, 3,  23201,     37691, 4605,  0.03085, 0),
    (2023, 4,  37691,    115295, 5052, -0.06510, 0),
    (2023, 5, 115295, 999999999,    0,        0, 0),
    # 2023 AOW
    (2023, 1,      0,     10741,    0,  0.04241, 1),
    (2023, 2,  10741,     23201,  457,  0.15388, 1),
    (2023, 3,  23201,     37691, 2374,  0.01589, 1),
    (2023, 4,  37691,    115295, 2604, -0.03355, 1),
    (2023, 5, 115295, 999999999,    0,        0, 1),


    # 2024
    (2024, 1,      0,     11441,   0 ,  0.084251, 0),
    (2024, 2,  11441,     24821,  968,   0.31443, 0),
    (2024, 3,  24821,     39958, 5158,   0.02471, 0),
    (2024, 4,  39958,    124935, 5532,  -0.06510, 0),
    (2024, 5, 124935, 999999999,    0,         0, 0),
    #2024 AOW
    (2024, 1,      0,     11441,   0 ,   0.04436, 1),
    (2024, 2,  11441,     24821,  501,   0.16214, 1),
    (2024, 3,  24821,     39958, 2662,   0.01275, 1),
    (2024, 4,  39958,    124935, 2854,  -0.03358, 1),
    (2024, 5, 124935, 999999999,    0,         0, 1),

    # 2025 bron zie loonheffing eerste tabel
    (2025, 1,      0,     12169,   0 ,   0.08053, 0),
    (2025, 2,  12169,     26288,  980,    0.3030, 0),
    (2025, 3,  26288,     43071, 5220,   0.02258, 0),
    (2025, 4,  43071,    129078, 5599,  -0.06510, 0),
    (2025, 5, 129078, 999999999,    0,         0, 0),

    #2025 AOW
    (2025, 1,      0,     12169,   0 ,   0.04029, 1),
    (2025, 2,  12169,     26288,  491,   0.15023, 1),
    (2025, 3,  26288,     43071, 2612,   0.01130, 1),
    (2025, 4,  43071,    129078, 2802,  -0.03257, 1),
    (2025, 5, 129078, 999999999,    0,         0, 1)

]

cursor.executemany("""
    INSERT INTO tax_arbeidskorting (year, bracket_number, lower_limit, upper_limit, base_credit, credit_percentage, aow_age)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", tax_arbeidskorting_data)


# Insert data into the tax_premies_volksverzekeringen table
tax_premies_volksverzekeringen = [
    # 2025
    (2025, 17.9, 0.1, 9.65, 38441, 0),
    (2025,    0, 0.1, 9.65, 38441, 1),
    (2025,    0, 0.1, 9.65, 38441, 2),
    # 2024
    (2024, 17.9, 0.1, 9.65, 38098, 0),
    (2024,    0, 0.1, 9.65, 38098, 1),
    (2024,    0, 0.1, 9.65, 40021, 2),
    # 2023
    (2023, 17.9, 0.1, 9.65, 37149, 0),
    (2023,    0, 0.1, 9.65, 37149, 1),
    (2023,    0, 0.1, 9.65, 38703, 2),
    # 2022
    (2022, 17.9, 0.1, 9.65, 35472, 0),
    (2022,    0, 0.1, 9.65, 35472, 1),
    (2022,    0, 0.1, 9.65, 36140, 2),
    # 2021
    (2021, 17.9, 0.1, 9.65, 35129, 0),
    (2021,    0, 0.1, 9.65, 35942, 1),
    (2021,    0, 0.1, 9.65, 35129, 2)
]

cursor.executemany("""
    INSERT INTO tax_premies_volksverzekeringen (year, aow_tarief, anw_tarief, wlz_tarief, maximaal_inkomen, aow_age)
    VALUES (?, ?, ?, ?, ?, ?)
""", tax_premies_volksverzekeringen)

# Dit is oude zooi.
tax_vermogensbelasting_data = [
    (2023, 'banktegoed', 0, 50000, 0.02),
    (2023, 'banktegoed', 50001, 100000, 0.03),
    (2023, 'beleggingen', 0, 50000, 0.04),
    (2023, 'beleggingen', 50001, 100000, 0.05),
    (2023, 'ontroerendgoed', 0, 50000, 0.06),
    (2023, 'ontroerendgoed', 50001, 100000, 0.07)
]

cursor.executemany("""
    INSERT INTO tax_vermogensbelasting (year, asset_type, lower_limit, upper_limit, tax_rate)
    VALUES (?, ?, ?, ?, ?)
""", tax_vermogensbelasting_data)

# Insert data into the tax_box3 table
tax_box3_data = [
    # Year, perc_spaargeld, perc_belegging, perc_schuld, perc_box3, heffingsvrij_vermogen,
    # drempel_schuld
    (2025, 0.0144, 0.0588, 0.0262, 0.36, 57684,  3700),
    (2024, 0.0144, 0.0604, 0.0261, 0.36, 57000,  3700),
    (2023, 0.0092, 0.0617, 0.0246, 0.32, 57000,  3400),
    (2022, 0.0000, 0.0553, 0.0228, 0.31, 50650,  3200),
    (2021, 0.0001, 0.0569, 0.0246, 0.30, 50000,  3200),
    (2020, 0.0004, 0.0528, 0.0274, 0.30, 30846,  3000),
    (2019, 0.0008, 0.0559, 0.0300, 0.33, 30360,  3000),
    (2018, 0.0012, 0.0539, 0.0320, 0.33, 30360,  3000),
    (2017, 0.0025, 0.0538, 0.0343, 0.33, 30360,  3000)
]
# Data 2024 - 2021 gecontroleerd op belastingdienst.nl 2020 en lager is de oude methode toegepast
# 2025 is vooralsnog een raadsel

cursor.executemany("""
    INSERT INTO tax_box3 (year, perc_spaargeld, perc_belegging, perc_schuld, perc_box3, heffingsvrij_vermogen, drempel_schuld)
    VALUES (?, ?, ?, ?, ?, ?, ? )
""", tax_box3_data)

# Insert data into the tbl_eigenwoningforfait table
tbl_eigenwoning =[
    #2025
    (2025, 1,    12500,   0.000,    0),
    (2025, 2,    25000,   0.001,    0),
    (2025, 3,    50000,   0.002,    0),
    (2025, 4,    75000,  0.0025,    0),
    (2025, 5,  1330000,  0.0035,    0),
    (2025, 6, 99000000, 0.00235, 4655),
    #2024
    (2024, 1, 12500, 0.0, 0),
    (2024, 2, 25000, 0.001, 0),
    (2024, 3, 50000, 0.002, 0),
    (2024, 4, 75000, 0.0025, 0),
    (2024, 5, 1310000, 0.0035, 0),
    (2024, 6, 99000000, 0.00235, 4586),
    #2023
    (2023, 1, 12500, 0.0, 0),
    (2023, 2, 25000, 0.001, 0),
    (2023, 3, 50000, 0.002, 0),
    (2023, 4, 75000, 0.0025, 0),
    (2023, 5, 1130000, 0.0035, 0),
    (2023, 6, 99000000, 0.00235, 4200),
    #2022
    (2022, 1, 12500, 0.0, 0),
    (2022, 2, 25000, 0.0015, 0),
    (2022, 3, 50000, 0.0025, 0),
    (2022, 4, 75000, 0.0035, 0),
    (2022, 5, 1130000, 0.0045, 0),
    (2022, 6, 99000000, 0.00235, 5085),
    #2021
    (2021, 1, 12500, 0.0, 0),
    (2021, 2, 25000, 0.002, 0),
    (2021, 3, 50000, 0.002, 0),
    (2021, 4, 75000, 0.004, 0),
    (2021, 5, 1110000, 0.005, 0),
    (2021, 6, 99000000, 0.00235, 5550),
    #2020
    (2020, 1, 12500, 0.0, 0),
    (2020, 2, 25000, 0.002, 0),
    (2020, 3, 50000, 0.0035, 0),
    (2020, 4, 75000, 0.0045, 0),
    (2020, 5, 1090000, 0.006, 0),
    (2020, 6, 99000000, 0.00235, 6540)
]




cursor.executemany("""
    INSERT INTO tbl_eigenwoningforfait(year, schijf_no, limit_WOZ, percentage, bedrag)
    VALUES (?, ?, ?, ?, ? )
""", tbl_eigenwoning)

# Insert data into the tbl_eigenwoningforfait table
tbl_ouderenkorting =[
    #2025
    (2025, 1,        0,   45308,  2035,   0),
    (2025, 2,    45308,   58875,  2035, .15),
    (2025, 3,    58875,99999999,     0,   0),

    #2024
    (2024, 1,        0,   44771,  2010,   0),
    (2024, 2,    44771,   58170,  2010, .15),
    (2024, 3,    58710,99999999,     0,   0),

    #2023
    (2023, 1,        0,   40889,  1835,   0),
    (2023, 2,    40889,   53122,  1835, .15),
    (2023, 3,    53122,99999999,     0,   0),

    #2022
    (2022, 1,        0,   38465,  1726,   0),
    (2022, 2,    38465,   49972,  1726, .15),
    (2022, 3,    49972,99999999,     0,   0),

    #2021
    (2021, 1,        0,   37971,  1703,   0),
    (2021, 2,    37971,   49324,  1703, .15),
    (2021, 3,    49324,99999999,     0,   0)

]

cursor.executemany("""
    INSERT INTO tbl_ouderenkorting(year, schijf_no, lower_limit, upper_limit, bedrag, perc)
    VALUES (?, ?, ?, ?, ?, ? )
""", tbl_ouderenkorting)

# Insert data into the tbl_tarief_aanpassing table
tbl_tarief_aanpassing =[
    (2025, 76817, 0.1201),  #Door de aanpassing krijgt u in 2025 over al uw aftrekposten in de hoogste belastingschijf maximaal 37,48% belasting 
    (2024, 75518, 0.1253),  # 36.97%
    (2023, 73031, 0.1257),  # 36.93%
    (2022, 69399, 0.0950),  # 40%
    (2021, 69507, 0.0065),  # 43%
    (2020, 68507, 0.0350)   # 46%
]

cursor.executemany("""
    INSERT INTO tbl_tarief_aanpassing(year, income_threshold, percentage)
    VALUES (?, ?, ?)
""", tbl_tarief_aanpassing)



# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Database and tables created successfully. Data inserted.")