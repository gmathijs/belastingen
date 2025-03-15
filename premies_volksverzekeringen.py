"""Premies VolksVerzekeringen"""

import sqlite3

class PremiesVolksverzekeringen:
    def __init__(self):
        # Connect to the database
        self.conn = sqlite3.connect('mijn_belastingen.db')
        self.cursor = self.conn.cursor()

    def get_premie_tarief(self, year):
        """
        Fetch the premium rates and maximum income threshold for the given year.
        """
        print(year)
        self.cursor.execute("""
            SELECT year, aow_tarief, anw_tarief, wlz_tarief, totaal_tarief, maximaal_inkomen, maximaal_premie
            FROM tax_premies_volksverzekeringen
            WHERE year = ?
        """, (year,))
        result = self.cursor.fetchone()
        if result:
            return {
                'year': result[0],
                'aow_tarief': result[1],
                'anw_tarief': result[2],
                'wlz_tarief': result[3],
                'totaal_tarief': result[4],
                'maximaal_inkomen': result[5],
                'maximaal_premie': result[6]
            }
        return None

    def bereken_premies(self, brutojaarsalaris, year):
        """
        Calculate the premiums for AOW, ANW, and Wlz based on the given income and year.
        """
        # Fetch the premium rates and maximum income threshold for the given year
        premie_data = self.get_premie_tarief(year)
        if not premie_data:
            raise ValueError(f"No premium data found for year {year}")

        # Extract the premium rates and maximum income threshold
        aow_tarief = premie_data['aow_tarief']
        anw_tarief = premie_data['anw_tarief']
        wlz_tarief = premie_data['wlz_tarief']
        totaal_tarief = premie_data['totaal_tarief']
        maximaal_inkomen = premie_data['maximaal_inkomen']
        maximaal_premie = premie_data['maximaal_premie']

        # Calculate the premiums
        if brutojaarsalaris > maximaal_inkomen:
            # If income exceeds the maximum threshold, use the maximum premium
            premie_aow = maximaal_premie * (aow_tarief / totaal_tarief)
            premie_anw = maximaal_premie * (anw_tarief / totaal_tarief)
            premie_wlz = maximaal_premie * (wlz_tarief / totaal_tarief)
        else:
            # Calculate premiums based on the income
            premie_aow = brutojaarsalaris * (aow_tarief / 100)
            premie_anw = brutojaarsalaris * (anw_tarief / 100)
            premie_wlz = brutojaarsalaris * (wlz_tarief / 100)

        # Round the premiums to 2 decimal places
        premie_aow = round(premie_aow, 2)
        premie_anw = round(premie_anw, 2)
        premie_wlz = round(premie_wlz, 2)

        # Calculate the total premium
        totale_premie = premie_aow + premie_anw + premie_wlz

        return {
            'premie_aow': premie_aow,
            'premie_anw': premie_anw,
            'premie_wlz': premie_wlz,
            'totale_premie': totale_premie
        }

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()