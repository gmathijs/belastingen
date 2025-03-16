import sqlite3

class PremiesVolksverzekeringen:
    def __init__(self):
        # Connect to the database
        self.conn = sqlite3.connect('mijn_belastingen.db')
        self.cursor = self.conn.cursor()

    def get_premie_tarief(self, year, aow_age):
        """
        Fetch the premium rates and maximum income threshold for the given year and AOW age status.
        """
        self.cursor.execute("""
            SELECT aow_tarief, anw_tarief, wlz_tarief, maximaal_inkomen
            FROM tax_premies_volksverzekeringen
            WHERE year = ? AND aow_age = ?
        """, (year, aow_age))
        result = self.cursor.fetchone()
        if result:
            return {
                'aow_tarief': result[0],
                'anw_tarief': result[1],
                'wlz_tarief': result[2],
                'maximaal_inkomen': result[3]
            }
        return None

    def bereken_premies(self, brutojaarsalaris, year, aow_age):
        """
        Calculate the premiums for AOW, ANW, and Wlz based on the given income, year, and AOW age status.
        """
        # Fetch the premium rates and maximum income threshold for the given year and AOW age status
        premie_data = self.get_premie_tarief(year, aow_age)
        if not premie_data:
            raise ValueError(f"No premium data found for year {year} and AOW age status {aow_age}")

        # Extract the premium rates and maximum income threshold
        aow_tarief = premie_data['aow_tarief']
        anw_tarief = premie_data['anw_tarief']
        wlz_tarief = premie_data['wlz_tarief']
        maximaal_inkomen = premie_data['maximaal_inkomen']

        # Calculate the total premium rate
        totaal_tarief = aow_tarief + anw_tarief + wlz_tarief

        # Calculate the premiums
        if brutojaarsalaris > maximaal_inkomen:
            # If income exceeds the maximum threshold, use the maximum income
            premie_aow = (aow_tarief / 100) * maximaal_inkomen
            premie_anw = (anw_tarief / 100) * maximaal_inkomen
            premie_wlz = (wlz_tarief / 100) * maximaal_inkomen
        else:
            # Calculate premiums based on the income
            premie_aow = (aow_tarief / 100) * brutojaarsalaris
            premie_anw = (anw_tarief / 100) * brutojaarsalaris
            premie_wlz = (wlz_tarief / 100) * brutojaarsalaris

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