import sqlite3
from tabulate import tabulate

class EigenWoningForfaitCalculator:
    def __init__(self, db_path):
        """
        Initialize the class with the path to the SQLite database.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_eigenwoningforfait_schijf(self, WOZ_Waarde, year):
        """
        Fetch the tax bracket (schijf) for the given WOZ value and year.
        """
        self.cursor.execute("""
            SELECT schijf_no, limit_WOZ, percentage, bedrag
            FROM tbl_eigenwoningforfait
            WHERE year = ? AND limit_WOZ >= ?
            ORDER BY schijf_no
            LIMIT 1
        """, (year, WOZ_Waarde))
        result = self.cursor.fetchone()

        if result:
            return {
                'schijf_no': result[0],
                'limit_WOZ': result[1],
                'percentage': result[2],
                'bedrag': result[3]
            }
        return None

    def bereken_eigenwoningforfait(self, WOZ_Waarde, year):
        """
        Calculate the Eigen Woning Forfait based on the WOZ value and year.
        """
        # Fetch all tax brackets (schijven) for the given year
        self.cursor.execute("""
            SELECT schijf_no, limit_WOZ, percentage, bedrag
            FROM tbl_eigenwoningforfait
            WHERE year = ?
            ORDER BY schijf_no
        """, (year,))
        schijven = self.cursor.fetchall()

        if not schijven:
            raise ValueError(f"No tax brackets found for year {year}")

        # Initialize the Eigen Woning Forfait
        eigenwoningforfait = 0

        # Iterate through the schijven and calculate the forfait
        for schijf in schijven:
            schijf_no, limit_WOZ, percentage, bedrag = schijf

            if WOZ_Waarde <= limit_WOZ:
                if schijf_no == 1:
                    # First schijf has a fixed forfait of 0
                    eigenwoningforfait = 0
                else:
                    # Calculate forfait based on the percentage
                    eigenwoningforfait = percentage * WOZ_Waarde
                break
        else:
            # If WOZ_Waarde exceeds the highest limit, use the last schijf
            last_schijf = schijven[-1]
            eigenwoningforfait = last_schijf[3] + last_schijf[2] * (WOZ_Waarde - last_schijf[1])

        # Convert the dictionary to a list of tuples for tabulate
        table_woz = [
            ["WOZ Waarde Eigen Woning", f"€{WOZ_Waarde:.0f}"],
            ["Inkomsten Eigen Woning", f"€{eigenwoningforfait:.0f}"],
            ["-" * 35, "-" * 23]  # Another separator line
        ]
        # Render the table
        table = tabulate(table_woz, 
                         headers=["Description", "Amount"], 
                         tablefmt="pretty",
                         colalign=("left", "left")
                         )
        # Create the table with specified column widths
        print(table)


        return table

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()