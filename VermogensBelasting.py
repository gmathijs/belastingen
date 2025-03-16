import sqlite3
import math
from tabulate import tabulate

class VermogensBelastingCalculator:
    def __init__(self):
        # Connect to the database
        self.conn = sqlite3.connect('mijn_belastingen.db')
        self.cursor = self.conn.cursor()

    def get_box3_data(self, year):
        """
        Fetch the Box 3 tax rates and thresholds for the given year.
        """
        self.cursor.execute("""
            SELECT perc_spaargeld, perc_belegging, perc_schuld, perc_box3, 
                   heffingsvrij_vermogen, drempel_schuld
            FROM tax_box3
            WHERE year = ?
        """, (year,))
        result = self.cursor.fetchone()
        if result:
            return {
                'perc_spaargeld': result[0],
                'perc_belegging': result[1],
                'perc_schuld': result[2],
                'perc_box3': result[3],
                'heffingsvrij_vermogen': result[4],
                'drempel_schuld': result[5]
            }
        return None

    def bereken_box3_belasting(self, spaargeld, belegging, ontroerend, schuld, uw_deel, heeft_partner, year):
        """
        Calculate the Box 3 tax and generate a detailed table.
        """
        # Fetch the Box 3 data for the given year
        box3_data = self.get_box3_data(year)
        if not box3_data:
            raise ValueError(f"No Box 3 data found for year {year}")

        # Extract the rates and thresholds
        perc_spaargeld = box3_data['perc_spaargeld']
        perc_belegging = box3_data['perc_belegging']
        perc_schuld = box3_data['perc_schuld']
        perc_box3 = box3_data['perc_box3']
        heffingsvrij_vermogen = box3_data['heffingsvrij_vermogen'] * 2 if heeft_partner else box3_data['heffingsvrij_vermogen']
        drempel_schuld = box3_data['drempel_schuld'] * 2 if heeft_partner else box3_data['drempel_schuld']

        # Calculate the taxable income
        totaal_vermogen = spaargeld + belegging + ontroerend
        schulden = max(0, schuld - drempel_schuld)
        rendementsgrondslag = totaal_vermogen - schulden
        rendement_schulden = math.floor(schulden * perc_schuld)
        belastbaar_rendement_vermogen = (perc_spaargeld * spaargeld) + (perc_belegging * belegging) + (perc_belegging * ontroerend)
        belastbaar_rendement_totaal = (perc_spaargeld * spaargeld) + (perc_belegging * belegging) + (perc_belegging * ontroerend) - rendement_schulden
        grondslag = max(0, rendementsgrondslag - heffingsvrij_vermogen)
        mijn_grondslag = grondslag * uw_deel
        perc_mijn_aandeel = mijn_grondslag/rendementsgrondslag

        rendementspercentage = belastbaar_rendement_vermogen / totaal_vermogen if totaal_vermogen > 0 else 0
        voordeel_sparen_en_beleggen = belastbaar_rendement_vermogen * mijn_grondslag / totaal_vermogen if totaal_vermogen > 0 else 0

        box3_belasting = perc_box3 * voordeel_sparen_en_beleggen

        table_data = [
            ["Fiscale partner", "Yes" if heeft_partner else "No"],
            ["Vermogen", ""],
            ["Bank en Spaargeld", f"€{spaargeld:,.0f}"],
            ["Beleggingen", f"€{belegging:,.0f}"],
            ["Ontroerende zaken in NL", f"€{ontroerend:,.0f}"],
            ["Totaal vermogen", f"€{totaal_vermogen:,.0f}"],
            ["-" * 35, "-" * 23],  # Separator line
            ["Forfaitair rendement vermogen", ""],
            ["Spaargeld", f"€{perc_spaargeld * spaargeld:,.0f}"],
            ["Beleggingen", f"€{perc_belegging * belegging:,.0f}"],
            ["Ontroerende zaken in NL", f"€{perc_belegging * ontroerend:,.0f}"],  
            ["Belastbaar rendement op vermogen", f"€{belastbaar_rendement_vermogen:,.0f}"],

            ["-" * 35, "-" * 23],  # Another separator line
            ["Schulden", f"€{schuld:,.0f}"],
            ["Drempel schulden", f"€{drempel_schuld:,.0f}"],
            ["Totaal schulden", f"€{schulden:,.0f}"],
            ["Belastbaar rendement op schulden", f"€{rendement_schulden:,.0f}"],

            ["-" * 35, "-" * 23],  # Another separator line
            ["Totaal=rendementsgrondslag", f"€{rendementsgrondslag:,.0f}"],
            ["Totaal Belastbaar rendement", f"€{belastbaar_rendement_totaal:,.0f}"],
            ["-" * 35, "-" * 23],  # Another separator line
            ["Heffingsvrij vermogen", f"€{heffingsvrij_vermogen:,.0f}"],
            ["Grondslag sparen en beleggen", f"€{grondslag:,.0f}"],
            ["-" * 30, "-" * 23],  # Another separator line
            ["Verdeling ik neem", f"{uw_deel * 100:.0f}%"],
            ["Mijn grondslag sparen en beleggen", f"€{mijn_grondslag:,.0f}"],
            ["Rendements grondslag uw aandeel", f"{perc_mijn_aandeel* 100:.1f}%"],
            ["-" * 35, "-" * 23],  # Another separator line
            ["Rendements Percentage", f"{rendementspercentage * 100:.2f}%"],
            ["Totaal voordeel Sparen en Beleggen", f"€{voordeel_sparen_en_beleggen:,.0f}"],
            ["Box 3 Belasting percentage", f"{perc_box3 * 100:.0f}%"],
            ["BOX 3 BELASTING", f"€{box3_belasting:,.0f}"]
        ]

        # Format the table with left alignment and pretty formatting
        table = tabulate(table_data, headers=["Description", "Amount"], tablefmt="pretty", colalign=("left", "left"))

        return table

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()