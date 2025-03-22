"""
Classes Used for Calculation of Inkomsten Belasting
The following classes are incorporated

1: class LoonbelastingCalculator:
2: class VermogensBelastingCalculator:
3: class HeffingskortingCalculator:
4: class ArbeidskortingCalculator:
5: class PremiesVolksverzekeringen:
6: class EigenWoningForfaitCalculator:
7: class OuderenKorting:
8: class TariefAanpassingEigenWoning:
"""
import sqlite3
import math

class LoonbelastingCalculator:
    """ Class description """
    def __init__(self, db_path):
        # Connect to the database
        self.conn = sqlite3.connect(db_path)
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

class HeffingskortingCalculator:
    """ Class description """
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_heffingskortingschijf(self, inkomen_werk_woning, year, aow_age):
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
        """, (year, effective_aow_age, inkomen_werk_woning, inkomen_werk_woning))
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

    def bereken_heffingskorting(self, inkomen_werk_woning, year, aow_age):
        """
        Calculate the tax credit based on the given year, income, and AOW age status.
        """
        relevante_schijf = self.get_heffingskortingschijf(inkomen_werk_woning, year, aow_age)
        if not relevante_schijf:
            raise ValueError(f"No tax credit bracket found for year {year} and income {inkomen_werk_woning}")

        heffingskorting = relevante_schijf['base_credit'] + \
                          relevante_schijf['credit_percentage'] * (inkomen_werk_woning - relevante_schijf['lower_limit']-1)

        return round(heffingskorting, 2)

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()



class ArbeidskortingCalculator:
    """ Class description """
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_arbeidskortingschijf(self, inkomen_uit_arbeid, year, aow_age):
        """ function description
        """

        # Treat aow_age = 2 as aow_age = 1
        effective_aow_age = 1 if aow_age == 2 else aow_age

        self.cursor.execute("""
            SELECT bracket_number, lower_limit, upper_limit, base_credit, credit_percentage
            FROM tax_arbeidskorting
            WHERE year = ? AND aow_age = ? AND lower_limit <= ? AND upper_limit >= ?
        """, (year, effective_aow_age, inkomen_uit_arbeid, inkomen_uit_arbeid))
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

    def bereken_arbeidskorting(self, brutojaarsalaris, year, aow_age):
        """function decription"""
        relevante_schijf = self.get_arbeidskortingschijf(brutojaarsalaris, year, aow_age)
        if not relevante_schijf:
            raise ValueError(f"No arbeidskorting bracket found for year {year} and income {brutojaarsalaris}")

        arbeidskorting = relevante_schijf['base_credit'] + \
                         relevante_schijf['credit_percentage'] * (brutojaarsalaris - relevante_schijf['lower_limit'] -1 )

        return round(arbeidskorting, 2)

    def close(self):
        """closure"""
        self.conn.close()

class PremiesVolksverzekeringen:
    """ Class description """
    def __init__(self, db_path):
        # Connect to the database
        self.conn = sqlite3.connect(db_path)
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


class VermogensBelastingCalculator:
    """ Class description """
    def __init__(self, db_path):
        # Connect to the database
        self.conn = sqlite3.connect(db_path)
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

    def bereken_box3_belasting(self, spaargeld, belegging, ontroerend, schuld, deel_box3, 
                               heeft_partner, year):
        """
        Calculate the Box 3 tax and return the results as a dictionary.
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
        mijn_grondslag = grondslag * deel_box3

        perc_mijn_aandeel = mijn_grondslag / rendementsgrondslag

        rendementspercentage = belastbaar_rendement_vermogen / totaal_vermogen if totaal_vermogen > 0 else 0
        voordeel_sparen_en_beleggen = belastbaar_rendement_vermogen * mijn_grondslag / totaal_vermogen if totaal_vermogen > 0 else 0

        box3_belasting = perc_box3 * voordeel_sparen_en_beleggen

        # Return the results as a dictionary
        return {
            "Fiscale partner": "Yes" if heeft_partner else "No",
            "Vermogen": {
                "Bank en Spaargeld": spaargeld,
                "Beleggingen": belegging,
                "Ontroerende zaken in NL": ontroerend,
                "Totaal vermogen": totaal_vermogen
            },
            "Forfaitair rendement vermogen": {
                "Spaargeld": perc_spaargeld * spaargeld,
                "Beleggingen": perc_belegging * belegging,
                "Ontroerende zaken in NL": perc_belegging * ontroerend,
                "Belastbaar rendement op vermogen": belastbaar_rendement_vermogen
            },
            "Schulden": {
                "Schulden": schuld,
                "Drempel schulden": drempel_schuld,
                "Totaal schulden": schulden,
                "Belastbaar rendement op schulden": rendement_schulden
            },
            "Rendementsgrondslag": {
                "Totaal rendementsgrondslag": rendementsgrondslag,
                "Totaal Belastbaar rendement": belastbaar_rendement_totaal
            },
            "Heffingsvrij vermogen": heffingsvrij_vermogen,
            "Grondslag sparen en beleggen": grondslag,
            "Verdeling": {
                "Uw deel": f"{deel_box3 * 100:.0f}%",
                "Mijn grondslag sparen en beleggen": mijn_grondslag,
                "Rendements grondslag uw aandeel": f"{perc_mijn_aandeel * 100:.1f}%"
            },
            "Rendements Percentage": f"{rendementspercentage * 100:.2f}%",
            "Totaal voordeel Sparen en Beleggen": voordeel_sparen_en_beleggen,
            "Box 3 Belasting percentage": f"{perc_box3 * 100:.0f}%",
            "BOX 3 BELASTING": box3_belasting
        }

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()


class EigenWoningForfaitCalculator:
    """ Class description """
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

        return eigenwoningforfait
    

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()

class OuderenKorting:
    """class description"""
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def calculate_korting(self, verzamelinkomen, year, aow):
        """function description"""
        if not aow:
            return {
                'Verzamelinkomen': verzamelinkomen,
                'Ouderenkorting': 0
            }


        self.cursor.execute("""
            SELECT lower_limit, upper_limit, bedrag, perc
            FROM tbl_ouderenkorting
            WHERE year = ? AND ? >= lower_limit AND ? < upper_limit
        """, (year, verzamelinkomen, verzamelinkomen))

        result = self.cursor.fetchone()
        if result:
            lower_limit, upper_limit, bedrag, perc = result
            korting = bedrag + perc * (verzamelinkomen - lower_limit - 1)
        else:
            korting = 0

        return {
            'Verzamelinkomen': verzamelinkomen,
            'Ouderenkorting': korting
        }


    def close(self):
        """function description"""
        self.conn.close()
class TariefAanpassingEigenWoning:
    """Class Description: Berekent de tariefsaanpassing voor hogere inkomsten ivm aftrekbare schulden"""
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()


    def calculate_tarief_aanpassing(self, aftrek, inkomen, year):
        """
        Calculate the mortgage interest deduction adjustment based on income and year.
        
        Args:
            aftrek (float): The mortgage interest deduction amount.
            inkomen (float): The income of the taxpayer.
            year (int): The year for which the calculation is performed.
        
        Returns:
            float: The calculated adjustment.
        """
        self.cursor.execute("""
            SELECT income_threshold, percentage
            FROM tbl_tarief_aanpassing
            WHERE year = ?
        """, (year,))

        result = self.cursor.fetchone()
        if result:
            income_threshold, percentage = result
            if inkomen > income_threshold:
                return aftrek * percentage
            else:
                return 0.0
        else:
            return 0.0

    def close(self):
        """Close the database connection."""
        self.conn.close()