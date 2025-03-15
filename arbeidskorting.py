import sqlite3

class ArbeidskortingCalculator:
    def __init__(self):
        self.conn = sqlite3.connect('mijn_belastingen.db')
        self.cursor = self.conn.cursor()

    def get_arbeidskortingschijf(self, brutojaarsalaris, year):
        self.cursor.execute("""
            SELECT bracket_number, lower_limit, upper_limit, base_credit, credit_percentage
            FROM tax_arbeidskorting
            WHERE year = ? AND lower_limit <= ? AND upper_limit >= ?
        """, (year, brutojaarsalaris, brutojaarsalaris))
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

    def bereken_arbeidskorting(self, brutojaarsalaris, year):
        relevante_schijf = self.get_arbeidskortingschijf(brutojaarsalaris, year)
        if not relevante_schijf:
            raise ValueError(f"No arbeidskorting bracket found for year {year} and income {brutojaarsalaris}")

        arbeidskorting = relevante_schijf['base_credit'] + \
                         relevante_schijf['credit_percentage'] * (brutojaarsalaris - relevante_schijf['lower_limit'] )

        return round(arbeidskorting, 2)

    def close(self):
        self.conn.close()