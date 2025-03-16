""" Main file to calculate dutch income tax for Box1 (Income) 
and Box3 (Assets, stocks, savings) 

"""
import os 
from tabulate import tabulate
from loonheffing import LoonbelastingCalculator
from heffingskorting import HeffingskortingCalculator
from arbeidskorting import ArbeidskortingCalculator
from VermogensBelasting import VermogensBelastingCalculator
from premies_volksverzekeringen import PremiesVolksverzekeringen
from eigenwoningforfait import EigenWoningForfaitCalculator

def bereken_inkomstenbelasting(bruto, jaar, aow_age):
    loonbelasting_calculator = LoonbelastingCalculator()
    loonheffing = loonbelasting_calculator.bereken_loonheffing(bruto, jaar, aow_age)

    arbeidskorting_calculator = ArbeidskortingCalculator()
    arbeidskorting = arbeidskorting_calculator.bereken_arbeidskorting(bruto, jaar, aow_age)

    heffingskorting_calculator = HeffingskortingCalculator()
    heffingskorting = heffingskorting_calculator.bereken_heffingskorting(bruto, jaar, aow_age)

    inkomstenbelasting = round(loonheffing - arbeidskorting - heffingskorting, 2)
    netto = bruto - inkomstenbelasting

    # Necessary for very low income exceptions
    if netto > bruto:
        netto = bruto
        inkomstenbelasting = 0


    # Calculate Premies Volksverzekeringen
    premies_calculator = PremiesVolksverzekeringen()
    premies = premies_calculator.bereken_premies(bruto, jaar, aow_age)
    premies_calculator.close()

    # Create a dictionary with the results
    inkomstenbelasting_details = {
        'bruto': bruto,
        'loonheffing': loonheffing,
        'arbeidskorting': arbeidskorting,
        'heffingskorting': heffingskorting,
        'inkomstenbelasting': inkomstenbelasting,
        'netto': netto,
        'premie_aow': premies['premie_aow'],
        'premie_anw': premies['premie_anw'],
        'premie_wlz': premies['premie_wlz'],
        'totale_premie': premies['totale_premie']
    }

    # Convert the dictionary to a list of tuples for tabulate
    table_data = [
        ("Bruto Inkomen","", f"€{inkomstenbelasting_details['bruto']:.2f}"),
        ("Loonheffing", f"€{inkomstenbelasting_details['loonheffing']:.2f}"),
        ("Arbeidskorting", f"€{inkomstenbelasting_details['arbeidskorting']:.2f}"),
        ("Heffingskorting", f"€{inkomstenbelasting_details['heffingskorting']:.2f}"),
        ("Inkomstenbelasting","", f"€{inkomstenbelasting_details['inkomstenbelasting']:.2f}"),
        ["-" * 35, "-" * 10, "-" * 10],  # Separator line
        ("AOW Premie", f"€{inkomstenbelasting_details['premie_aow']:.2f}"),
        ("ANW Premie", f"€{inkomstenbelasting_details['premie_anw']:.2f}"),
        ("Wlz Premie", f"€{inkomstenbelasting_details['premie_wlz']:.2f}"),
        ("Totale Premie",f"€{inkomstenbelasting_details['totale_premie']:.2f}"),
        ("Netto Inkomen","", f"€{inkomstenbelasting_details['netto']:.2f}")
    ]

    # Use tabulate to format the table
    table = tabulate(table_data, headers=["Description"," " ,"Amount"], tablefmt="pretty", colalign=("left", "left"))

    return table


if __name__ == '__main__':

    db_path = "mijn_belastingen.db" 
    year = 2024          # Tax year
    aow_er = 1            # 0 geen AOW, 1 AOW na 1946, 2 AOW voor 1946
    heeft_partner = True # Whether you have a fiscal partner
    income   = 50000      # Bruto inkomen
    # Input voor Box 3
    spaargeld = 109929   # Savings
    belegging = 69569    # Investments
    ontroerend = 43000   # Real estate
    schuld = 10000       # Debts
    uw_deel = 1.0        # Your share of the assets (1.0 for full ownership)
    WOZ_Waarde = 316000  # Replace with the actual WOZ value

    # Calculate income tax
    result_table = bereken_inkomstenbelasting(income, year, 1)
    print(result_table)  # Output to terminal


    # Calculate Box 3 tax and generate the table
    calculator = VermogensBelastingCalculator()
    box3_table = calculator.bereken_box3_belasting(spaargeld, belegging, ontroerend, schuld, uw_deel, heeft_partner, year)
    print(box3_table)     # Output to terminal
    calculator.close()

    # calculate EigenWoningForfait

    # Create an instance of the EigenWoningForfaitCalculator class
    eigenwoningforfait_calculator = EigenWoningForfaitCalculator(db_path)




    # Calculate the Eigen Woning Forfait
    table_woz = eigenwoningforfait_calculator.bereken_eigenwoningforfait(WOZ_Waarde, year)
    print(table_woz)     # Output to terminal

    # Close the database connection
    eigenwoningforfait_calculator.close()

    # Define the file name
    filename = "taxes.txt"

    # Check if the file exists before deleting
    if os.path.exists(filename):
        os.remove(filename)


    # Write the table to a text file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(result_table +"\n")
        file.write(table_woz+"\n")
        file.write(box3_table)

    # Open the text file automatically (Mac-specific)
    os.system(f"open {filename}")  # This works on macOS
