"""
Calculation Functions
"""
from classes_IB import (
    HeffingskortingCalculator,
    PremiesVolksverzekeringen,
    VermogensBelastingCalculator,
    LoonbelastingCalculator,
    ArbeidskortingCalculator,
)
def calculate_box1(input_data):
    """
    Perform Box 3 tax calculation based on input data.
    """
    # Initialize the calculator and perform calculations
    loonbelasting_calculator = LoonbelastingCalculator(input_data["db_path"])
    bruto = input_data["Inkomen"] +   input_data["Pensioen"]                                       
    loonheffing = loonbelasting_calculator.bereken_loonheffing(bruto, input_data["year"], input_data["aow_er"])

    heffingskorting_calculator = HeffingskortingCalculator(input_data["db_path"])
    heffingskorting = heffingskorting_calculator.bereken_heffingskorting(bruto,input_data["year"], input_data["aow_er"])

    # Iemand die een inomen uit arbeid heeft krijgt dit dus in dit geval alleen Inkomen 
    arbeidskorting_calculator = ArbeidskortingCalculator(input_data["db_path"])
    arbeidskorting = arbeidskorting_calculator.bereken_arbeidskorting(input_data["Inkomen"] , input_data["year"], input_data["aow_er"])

    

    inkomstenbelasting = round(loonheffing - arbeidskorting - heffingskorting, 2)
    netto = bruto - inkomstenbelasting

    # Create the results_box1 dictionary
    results_box1 = {
        "Inkomen uit arbeid": input_data["Inkomen"] ,       #     Total gross income
        "Pensioen of uitkering": input_data["Pensioen"] ,   # Total gross income        
        "loonheffing": loonheffing,                         # Wage tax
        "arbeidskorting": arbeidskorting,                   # Employment tax credit
        "heffingskorting": heffingskorting,                 # General tax credit
        "Inkomstenbelasting": inkomstenbelasting,           # Totaal aan Box1 belastingen
        "netto_inkomen": netto                              # Net income after taxes and credits
}
    # Close the calculator
    loonbelasting_calculator.close()
    heffingskorting_calculator.close()
    arbeidskorting_calculator.close()
 

    return results_box1

def calculate_premies(input_data):
    """function description"""
    # Premies are based on the total income i.e. from work and uitkeringen
    bruto = input_data["Inkomen"] +   input_data["Pensioen"] 

    premies_calculator = PremiesVolksverzekeringen(input_data["db_path"])
    results_premies = premies_calculator.bereken_premies(bruto, input_data["year"], input_data["aow_er"])

    premies_calculator.close()

    return results_premies

def calculate_box3(input_data):
    """
    Perform Box 3 tax calculation based on input data.
    """
    # Initialize the calculator
    calculator_box3 = VermogensBelastingCalculator(input_data["db_path"])

    # Perform the calculation
    results_box3 = calculator_box3.bereken_box3_belasting(
        spaargeld=input_data["spaargeld"],
        belegging=input_data["belegging"],
        ontroerend=input_data["ontroerend"],
        schuld=input_data["schuld"],
        uw_deel=input_data["uw_deel"],
        heeft_partner=input_data["heeft_partner"],
        year=input_data["year"]
    )

    # Close the calculator
    calculator_box3.close()

    return results_box3