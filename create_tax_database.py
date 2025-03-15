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
        credit_percentage REAL NOT NULL
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

# Create the tax_premies_volksverzekeringen
cursor.execute("""
    CREATE TABLE tax_premies_volksverzekeringen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    aow_tarief REAL NOT NULL,
    anw_tarief REAL NOT NULL,
    wlz_tarief REAL NOT NULL,
    totaal_tarief REAL NOT NULL,
    maximaal_inkomen REAL NOT NULL,
    maximaal_premie REAL NOT NULL
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
    (2019, 2, 34818,  68507, 0.3810,  1),
    (2019, 3, 68508, 999999, 0.5175,  1),
    # 2019 AOW before  1 Januari 1946
    (2019, 1,     0,  20384, 0.1875,  2),
    (2019, 2, 20385,  34817, 0.2020,  2),
    (2019, 2, 34818,  68507, 0.3810,  2),
    (2019, 3, 68508, 999999, 0.5175,  2),

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
    (2024, 3, 75518, 9999999,   0.4950, 2)

]

cursor.executemany("""
    INSERT INTO tax_loonheffing (year, bracket_number, lower_limit, upper_limit, tax_rate, aow_age)
    VALUES (?, ?, ?, ?, ?, ?)
""", tax_loonheffing_data)

# Insert data into the tax_heffingskorting table (example for 2023)
tax_heffingskorting_data = [
    # 2019
    (2019, 1,     0,    20384, 2477,        0, 0),
    (2019, 2, 20384,    68508, 2477, -0.05147, 0),
    (2019, 3, 68508, 99999999,     0,       0, 0),

    (2019, 1,     0,    20384, 2477,        0,  1),
    (2019, 2, 20384,    68508, 2477, -0.05147,  1),
    (2019, 3, 68508, 99999999,    0,        0,  1),

    # 2020
    (2020, 1,     0,     20711, 2711,        0,  0),
    (2020, 2, 20711,     68508, 2711, -0.05672,  0),
    (2020, 3, 68508,  99999999,    0,        0,  0),

    (2020, 1,     0,     20711, 2711,        0,  1),
    (2020, 2, 20711,     68508, 2711, -0.05672,  1),
    (2020, 3, 68508,   99999999,    0,       0,  1),

    # 2021
    (2021, 1,     0,      21044, 2837,        0,   0),
    (2021, 2, 21044,       68508, 2837, -0.05977,  0),
    (2021, 3, 68508,    99999999,    0,       0,   0),

    (2021, 1,     0,       21044, 2837,        0,  1),
    (2021, 2, 21044,       68508, 2837, -0.05977,  1),
    (2021, 3, 68508,    99999999,    0,        0,  1),

    # 2022
    (2022, 1,     0,   21044, 2837,        0,  0),
    (2022, 2, 21044,   68508, 2837, -0.05977,  0),
    (2022, 3, 68508, 99999999,   0,        0,  0),

    (2022, 1,     0,    21044,  2837,        0,  1),
    (2022, 2, 21044,    68508,  2837, -0.05977,  1),
    (2022, 3, 68508, 99999999,     0,        0,  1),

    # 2023 
    (2023, 1,     0,    22661, 3070,       0,   0),
    (2023, 2, 22661,    73030, 3070, -0.06095,  0),
    (2023, 3, 73031,  99999999,   0,        0,  0),

    (2023, 1,     0,     22661, 3070,        0,  1),
    (2023, 2, 22661,     73030, 3070, -0.06095,  1),
    (2023, 3, 73031,  99999999,    0,        0,  1),

    # 2024
    (2024, 1,     0,    24813, 3362,        0,  1),
    (2024, 2, 24813,    75518, 3362, -0.06630,  1),
    (2024, 3, 75518, 99999999,    0,        0,  1)
]

cursor.executemany("""
    INSERT INTO tax_heffingskorting (year, bracket_number, lower_limit, upper_limit, base_credit, credit_percentage, aow_age)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", tax_heffingskorting_data)

# Insert data into the tax_arbeidskorting table (2019–2023)
tax_arbeidskorting_data = [
    # 2019
    (2019, 1, 0, 9694, 0, 0.01754),
    (2019, 2, 9694, 20940, 170, 0.28712),
    (2019, 3, 20940, 34060, 3399, 0),
    (2019, 4, 34060, 90710, 3399, -0.06),
    (2019, 5, 90711, 999999999, 0, 0),
    # 2020
    (2020, 1, 0, 9921, 0, 0.02812),
    (2020, 2, 9921, 21430, 279, 0.28812),
    (2020, 3, 21430, 34954, 3595, 0.01656),
    (2020, 4, 34954, 98604, 3819, -0.06),
    (2020, 5, 98604, 999999999, 0, 0),
    # 2021
    (2021, 1, 0, 10109, 0, 0.02813),
    (2021, 2, 10109, 21836, 463, 0.28771),
    (2021, 3, 21836, 35653, 3873, 0.02663),
    (2021, 4, 35653, 105737, 4205, -0.06),
    (2021, 5, 105737, 999999999, 0, 0),
    # 2022
    (2022, 1, 0, 10350, 0, 0.04541),
    (2022, 2, 10350, 22357, 470, 0.28461),
    (2022, 3, 22357, 36650, 3887, 0.02610),
    (2022, 4, 36650, 109347, 4260, -0.0586),
    (2022, 5, 109347, 999999999, 0, 0),
    # 2023
    (2023, 1, 0, 10741, 0, 0.08231),
    (2023, 2, 10741, 23201, 884, 0.29861),
    (2023, 3, 23201, 37691, 4605, 0.03085),
    (2023, 4, 37691, 115295, 5052, -0.06510),
    (2023, 5, 115295, 999999999, 0, 0),
    # 2024
    (2024, 1, 0, 11441,0 , 0.084251),
    (2024, 2, 11441, 24821, 968, 0.31443),
    (2024, 3, 24821, 39958, 5158, 0.02471),
    (2024, 4, 39958, 124935, 5532, -0.06510),
    (2024, 5, 124935, 999999999, 0, 0),




]

cursor.executemany("""
    INSERT INTO tax_arbeidskorting (year, bracket_number, lower_limit, upper_limit, base_credit, credit_percentage)
    VALUES (?, ?, ?, ?, ?, ?)
""", tax_arbeidskorting_data)

# Insert data into the tax_vermogensbelasting table (example for 2023)
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

# Insert data into the tax_vermogensbelasting table
tax_premies_volksverzekeringen = [
    (2025, 17.9, 0.1, 9.65, 27.65, 38441, 10628),
    (2024, 17.9, 0.1, 9.65, 27.65, 38098, 10534),
    (2023, 17.9, 0.1, 9.65, 27.65, 37149, 10271),
    (2022, 17.9, 0.1, 9.65, 27.65, 35472, 9808),
    (2021, 17.9, 0.1, 9.65, 27.65, 35129, 9713)
]

cursor.executemany("""
    INSERT INTO tax_premies_volksverzekeringen (year, aow_tarief, anw_tarief, wlz_tarief, totaal_tarief, maximaal_inkomen, maximaal_premie)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", tax_premies_volksverzekeringen)


# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Database and tables created successfully. Data inserted.")