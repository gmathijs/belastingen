"""
Calculation Functions
1. def calculate_box1(input_data):
      inclusief loonheffing, heffingskorting, arbeidskorting
2. def calculate_premies(input_data):
3. def calculate_box3(input_data):
4. def calculate_ouderenkorting(input_data):


"""
from classes_IB import (
    HeffingskortingCalculator,
    PremiesVolksverzekeringen,
    VermogensBelastingCalculator,
    LoonbelastingCalculator,
    ArbeidskortingCalculator,
    OuderenKorting, EigenWoningForfaitCalculator
)
def calculate_box1(input_data):
    """
    Perform Box 3 tax calculation based on input data.
    """
    # Initialize the calculator and perform calculations
    loonbelasting_calculator = LoonbelastingCalculator(input_data["db_path"])
    bruto = input_data["Inkomen"] +   input_data["Pensioen"]                                       
    loonheffing = loonbelasting_calculator.bereken_loonheffing(bruto, input_data["year"], input_data["aow_er"])

    # Bereken de Heffingskorting 
    heffingskorting_calculator = HeffingskortingCalculator(input_data["db_path"])
    heffingskorting = heffingskorting_calculator.bereken_heffingskorting(bruto,input_data["year"], input_data["aow_er"])

    # Iemand die een inkomen uit arbeid heeft krijgt dit dus in dit geval alleen Inkomen 
    arbeidskorting_calculator = ArbeidskortingCalculator(input_data["db_path"])
    arbeidskorting = arbeidskorting_calculator.bereken_arbeidskorting(input_data["Inkomen"] , input_data["year"], input_data["aow_er"])

    # Bereken het EigenWoning forfait
    calculator_ewf = EigenWoningForfaitCalculator(input_data["db_path"])
    # Perform the calculation
    eigenwoningforfait = calculator_ewf.bereken_eigenwoningforfait(  input_data["WOZ_Waarde"],input_data["year"])

    # Box 1 gegoochel 
    inkomstenbelasting = round(loonheffing - arbeidskorting - heffingskorting, 2)
    netto = bruto - inkomstenbelasting

    inkomen_woning = eigenwoningforfait - input_data["AftrekEW"]
    inkomen_werk_woning = bruto + inkomen_woning

    # Bereken de ouderen korting moet gebaseerd zijn op het verzamel inkomen wat weer op zijn beurt 
    # kan worden bereken na box3
    calculator_ok = OuderenKorting(input_data["db_path"])
    verzamelinkomen = input_data["Inkomen"] + input_data["Pensioen"]  # Nog goed uitrekenen
    results_ouderenkorting = calculator_ok.calculate_korting(verzamelinkomen,  input_data["year"], input_data["aow_er"])
    ouderenkorting = results_ouderenkorting["Ouderenkorting"] 

    # Create the results_box1 dictionary
    results_box1 = {
        "Inkomen uit arbeid": input_data["Inkomen"] ,           # Total gross income
        "Pensioen of uitkering": input_data["Pensioen"] ,       # Total gross income
        "Inkomen uit Werk en Woning":inkomen_werk_woning ,      # Inkomen uit werk en woning
        "loonheffing": loonheffing,                             # Wage tax
        "arbeidskorting": arbeidskorting,                       # Employment tax credit
        "heffingskorting": heffingskorting,                     # General tax credit
        "Inkomstenbelasting": inkomstenbelasting,               # Totaal aan Box1 belastingen
        "Eigenwoningforfait": eigenwoningforfait,               # Eigenwoning forfait
        "netto_inkomen": netto,                                 # Net income after taxes and credits
        "Ouderenkorting": ouderenkorting                        # Ouderenkorting
        }
    # Close the calculator
    loonbelasting_calculator.close()
    heffingskorting_calculator.close()
    arbeidskorting_calculator.close()
 

    return results_box1


def calculate_inkomen_werkenwoning(input_data):
    """
    Calculate the steps for the calculation of het 
    inkomen werk en woning
    """
    # Initialize the calculator and perform calculations
    bruto = input_data["Inkomen"] +   input_data["Pensioen"]    

    # Bereken het EigenWoning forfait
    calculator_ewf = EigenWoningForfaitCalculator(input_data["db_path"])
    eigenwoningforfait = calculator_ewf.bereken_eigenwoningforfait(  input_data["WOZ_Waarde"],input_data["year"])

    inkomen_werk_woning = bruto + eigenwoningforfait - input_data["AftrekEW"]


    # Create results_inkomen_werkenwoning
    results_inkomen_werkenwoning = {
        "BrutoInkomen": bruto ,                                  #   Bruto Inkomen            
        "EigenWoningForfait": eigenwoningforfait,                #   Eigen Woning Forfait# Total gross income
        "AftrekbareUitgavenEigenwoning": input_data["AftrekEW"], #   Aftrek eigenwoning
        "UwDeel": input_data["deel_box1"], #   Aftrek eigenwoning        
        "InkomenWerkenWoning": inkomen_werk_woning               #   Inkomen wek en woning
        }
    
    # Close the calculator
    calculator_ewf.close()

    return results_inkomen_werkenwoning 


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

    # Perform the calculation with the input data 
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

def calculate_ouderenkorting(input_data, verzamelinkomen):
    """
    Berekent de ouderenkorting op basis van het verzamelinkomen
    """
    # Initialize the calculator
    calculator_ok = OuderenKorting(input_data["db_path"])

    # Perform the calculation
    results_ouderenkorting = calculator_ok.calculate_korting(verzamelinkomen,  input_data["year"], input_data["aow_er"])

    # Close the calculator
    calculator_ok.close()

    return results_ouderenkorting

def calculate_ew_forfait(input_data):
    """
    Perform Box 3 tax calculation based on input data.
    """
    # Initialize the calculator
    calculator_ewf = EigenWoningForfaitCalculator(input_data["db_path"])

    # Perform the calculation
    results_ewf = calculator_ewf.bereken_eigenwoningforfait(  input_data["WOZ_Waarde"],input_data["year"])

    # Close the calculator
    calculator_ewf.close()

    return results_ewf

def calculate_verzamelinkomen(InkomenWerkWoning, VoordeelBox3):
    """
    Berekent het verzamel Inkomen
    """

    verzamelinkomen = InkomenWerkWoning + VoordeelBox3

    return verzamelinkomen