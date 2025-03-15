import sqlite3

class LoonbelastingCalculator:
    def __init__(self):
        # Connect to the database
        self.conn = sqlite3.connect('mijn_belastingen.db')
        self.cursor = self.conn.cursor()

    def get_loonbelastingschijf(self, brutojaarsalaris, year, aow_age):
        """
        Fetch the tax bracket for the given year, income, and AOW age status.
        """
        self.cursor.execute("""
            SELECT bracket_number, lower_limit, upper_limit, tax_rate
            FROM tax_loonheffing
            WHERE year = ? AND aow_age = ? AND lower_limit <= ? AND upper_limit >= ?
        """, (year, aow_age, brutojaarsalaris, brutojaarsalaris))
        result = self.cursor.fetchone()
        if result:
            return {
                'bracket_number': result[0],
                'lower_limit': result[1],
                'upper_limit': result[2],
                'tax_rate': result[3]
            }
        return None

    def bereken_loonheffing(self, brutojaarsalaris, year, aow_age):
        """
        Calculate the income tax based on the given year, income, and AOW age status.
        """
        # Fetch all tax brackets for the given year and AOW age status
        self.cursor.execute("""
            SELECT bracket_number, lower_limit, upper_limit, tax_rate
            FROM tax_loonheffing
            WHERE year = ? AND aow_age = ?
            ORDER BY bracket_number
        """, (year, aow_age))
        brackets = self.cursor.fetchall()

        if not brackets:
            raise ValueError(f"No tax brackets found for year {year} and AOW age status {aow_age}")

        # Initialize total tax
        total_tax = 0

        # Iterate through the brackets and calculate the tax
        for bracket in brackets:
            bracket_number, lower_limit, upper_limit, tax_rate = bracket

            if brutojaarsalaris >= upper_limit:
                # Income is above or equal to the upper limit of this bracket
                taxable_amount = upper_limit - lower_limit
            else:
                # Income falls within this bracket
                taxable_amount = brutojaarsalaris - lower_limit

            # Add the tax for this bracket
            total_tax += taxable_amount * tax_rate

            # Stop if the income falls within this bracket
            if brutojaarsalaris <= upper_limit:
                break

        return round(total_tax, 2)

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()