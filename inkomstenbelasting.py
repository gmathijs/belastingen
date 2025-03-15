from tabulate import tabulate
from loonheffing import LoonbelastingCalculator
from heffingskorting import HeffingskortingCalculator
from arbeidskorting import ArbeidskortingCalculator
from VermogensBelasting import VermogensBelastingCalculator
from premies_volksverzekeringen import PremiesVolksverzekeringen

def bereken_inkomstenbelasting(bruto, jaar, aow_age):
    loonbelasting_calculator = LoonbelastingCalculator()
    loonheffing = loonbelasting_calculator.bereken_loonheffing(bruto, jaar, aow_age)

    arbeidskorting_calculator = ArbeidskortingCalculator()
    arbeidskorting = arbeidskorting_calculator.bereken_arbeidskorting(bruto, jaar)

    heffingskorting_calculator = HeffingskortingCalculator()
    heffingskorting = heffingskorting_calculator.bereken_heffingskorting(bruto, jaar)

    inkomstenbelasting = round(loonheffing - arbeidskorting - heffingskorting, 2)
    netto = bruto - inkomstenbelasting

    # Necessary for very low income exceptions
    if netto > bruto:
        netto = bruto
        inkomstenbelasting = 0


    # Calculate Premies Volksverzekeringen
    premies_calculator = PremiesVolksverzekeringen()
    premies = premies_calculator.bereken_premies(bruto, jaar)
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
        ("AOW Premie", f"€{inkomstenbelasting_details['premie_aow']:.2f}"),
        ("ANW Premie", f"€{inkomstenbelasting_details['premie_anw']:.2f}"),
        ("Wlz Premie", f"€{inkomstenbelasting_details['premie_wlz']:.2f}"),
        ("Totale Premie",f"€{inkomstenbelasting_details['totale_premie']:.2f}"),
        ("Netto Inkomen","", f"€{inkomstenbelasting_details['netto']:.2f}")
    ]

    # Use tabulate to format the table
    table = tabulate(table_data, headers=["Description"," " ,"Amount"], tablefmt="pretty")

    return table


if __name__ == '__main__':
    result_table = bereken_inkomstenbelasting(50000, 2023, 1)
    print(result_table)