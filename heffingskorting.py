import sqlite3

class HeffingskortingCalculator:
    def __init__(self):
        self.conn = sqlite3.connect('mijn_belastingen.db')
        self.cursor = self.conn.cursor()

    def get_heffingskortingschijf(self, brutojaarsalaris, year, aow_age):
        """
        Fetch the tax credit bracket for the given year, income, and AOW age status.
        If aow_age is 2 (born before 1 January 1946), treat it as 1 (at/above AOW age).
        """
        # Treat aow_age = 2 as aow_age = 1
        effective_aow_age = 1 if aow_age == 2 else aow_age

        self.cursor.execute("""
            SELECT bracket_number, lower_limit, upper_limit, base_credit, credit_percentage
            FROM tax_heffingskorting
            WHERE year = ? AND aow_age = ? AND lower_limit <= ? AND upper_limit >= ?
        """, (year, effective_aow_age, brutojaarsalaris, brutojaarsalaris))
        result = self.cursor.fetchone()
        if result:
            return {
                'bracket_number': result[0],
                'lower_limit': result[1],
                'upper_limit': result[2],
                'base_credit': result[3],
                'credit_percentage': result[4]
            }
        return None

    def bereken_heffingskorting(self, brutojaarsalaris, year, aow_age):
        """
        Calculate the tax credit based on the given year, income, and AOW age status.
        """
        relevante_schijf = self.get_heffingskortingschijf(brutojaarsalaris, year, aow_age)
        if not relevante_schijf:
            raise ValueError(f"No tax credit bracket found for year {year} and income {brutojaarsalaris}")

        heffingskorting = relevante_schijf['base_credit'] + \
                          relevante_schijf['credit_percentage'] * (brutojaarsalaris - relevante_schijf['lower_limit'])

        return round(heffingskorting, 2)

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()