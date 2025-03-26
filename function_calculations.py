"""
Calculation Functions
1. def calculate_box1(input_data):
      inclusief loonheffing, heffingskorting, arbeidskorting, ouderenkorting
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
    OuderenKorting, EigenWoningForfaitCalculator,
    TariefAanpassingEigenWoning
)

def calculate_box1(input_data, person, tussenresultaat):
    """
    Perform Box 3 tax calculation based on input data.
    """
    # Initialize the calculator and perform calculations
    loonbelasting_calculator = LoonbelastingCalculator(input_data["db_path"])
    inkomenwerkenwoning =    tussenresultaat['inkomenwerkenwoning']    
    verzamelinkomen =  tussenresultaat['verzamelinkomen'] 
    totaalpremies = tussenresultaat['totaalpremies'] 

  
    # Iemand die een inkomen uit arbeid heeft krijgt dit dus in dit geval alleen Inkomen 
    arbeidskorting_calculator = ArbeidskortingCalculator(input_data["db_path"])
    arbeidskorting = max(0,arbeidskorting_calculator.bereken_arbeidskorting(person['Inkomen'] , input_data["year"], person["aow_er"]))

    loonheffing = loonbelasting_calculator.bereken_loonheffing(inkomenwerkenwoning, input_data["year"], person["aow_er"])
    loonheffing_excl = loonheffing - totaalpremies

    # Bereken de Heffingskorting 
    heffingskorting_calculator = HeffingskortingCalculator(input_data["db_path"])
    heffingskorting = max(0,heffingskorting_calculator.bereken_heffingskorting(inkomenwerkenwoning,input_data["year"], person["aow_er"]))

    # Bereken de ouderen korting moet gebaseerd zijn op het verzamel inkomen wat weer op zijn beurt 
    calculator_ok = OuderenKorting(input_data["db_path"])
    results_ouderenkorting = calculator_ok.calculate_korting(verzamelinkomen,  input_data["year"], person["aow_er"])
    ouderenkorting = max(0,results_ouderenkorting["Ouderenkorting"])

    kortingen_totaal = heffingskorting + arbeidskorting + ouderenkorting

    dividend_deel = input_data['divident'] * person['deel_div']



    # Box 1 
    inkomstenbelasting = round(loonheffing - arbeidskorting - heffingskorting - ouderenkorting, 2)
    netto = inkomenwerkenwoning - inkomstenbelasting

    # Box 3 
    inkomstenbelasting_box3 = tussenresultaat['InkomstenBelastinBox3']

    TotaalInkomstenBelasting = loonheffing_excl + inkomstenbelasting_box3
    TotaalInkomstenBelastingInclBox3 = TotaalInkomstenBelasting + totaalpremies - kortingen_totaal 
    ingehouden_belasting = person['al_ingehouden'] + dividend_deel

    bedrag_aanslag = TotaalInkomstenBelastingInclBox3 - ingehouden_belasting
    nieuw_bedrag_aanslag = bedrag_aanslag - person['voorlopige_aanslag']

    # Create the results_box1 dictionary
    results_box1 = {
        "Inkomen uit arbeid": person["Inkomen"] ,               # Total gross income
        "Pensioen of uitkering": person["Pensioen"] ,           # Total gross income
        "Verzamelinkomen": verzamelinkomen,                     # Verzamelinkomen
        "loonheffing_excl": loonheffing_excl,                   # Wage tax excl. premies 
        "loonheffing": loonheffing,                             # Wage tax excl. premies       
        "arbeidskorting": arbeidskorting,                       # Employment tax credit
        "heffingskorting": heffingskorting,                     # General tax credit
        "ouderenkorting": ouderenkorting,                       # Ouderen korting
        "kortingentotaal": kortingen_totaal,                    # totaal aan kortingen   
        "Inkomstenbelasting": inkomstenbelasting,               # Totaal aan Box1 belastingen
        "TotaalInkomstenbelasting": TotaalInkomstenBelasting,   # Totaal aan Box1 + Box3 belastingen   
        "TotaalInkomstenbelastingInclBox3": TotaalInkomstenBelastingInclBox3,   # Totaal aan Box1 + Box3 belastingen 
        "Dividend uw deel": dividend_deel,                      # Uw deel dividend
        "ingehouden_belasting": ingehouden_belasting,            # Al ingehouden loonheffing + divident  
        "Bedrag_aanslag": bedrag_aanslag,                      # verschuldigd 
        "Nieuw_bedrag_aanslag": nieuw_bedrag_aanslag,           # inclusief al betaald 
        "netto_inkomen": netto,                                 # Net income after taxes and credits
        }
    # Close the calculator
    loonbelasting_calculator.close()
    heffingskorting_calculator.close()
    arbeidskorting_calculator.close()
 

    return results_box1


def calculate_inkomen_werkenwoning(input_data, person, tussenresultaat):
    """
    Box1a
    Calculate the steps for the calculation of het 
    """
    # Initialize the calculator and perform calculations
    bruto = person["Inkomen"] +   person["Pensioen"]    

    # Bereken het EigenWoning forfait
    calculator_ewf = EigenWoningForfaitCalculator(input_data["db_path"])
    eigenwoningforfait = calculator_ewf.bereken_eigenwoningforfait(  input_data["WOZ_Waarde"],input_data["year"])

    # Voeg hier de tariefsaanpassing EigenWoning toe 
    aftrekeigenwoning =  input_data["AftrekEW"]   # totaal bedrag

    # Correcie bepaal extra aftrek ivm tariefsaanpassing hogere inkomens
    calc_tariefsaanpassing = TariefAanpassingEigenWoning(input_data["db_path"])
    aftrek_extra= calc_tariefsaanpassing.calculate_tarief_aanpassing(aftrekeigenwoning, bruto ,input_data["year"])

    aftrekeigenwoning = aftrekeigenwoning-aftrek_extra
    totaaleigenwoning=  (eigenwoningforfait - aftrekeigenwoning)
    totaaleigenwoning_uwdeel = totaaleigenwoning*person['deel_box1']

    inkomen_werk_woning = bruto + totaaleigenwoning_uwdeel


    # resultaat belangrijk voor volgende routines
    tussenresultaat['inkomenwerkenwoning'] = inkomen_werk_woning


    # Create results_inkomen_werkenwoning
    results_inkomen_werkenwoning = {
        "BrutoInkomen": bruto ,                                  #   Bruto Inkomen            
        "EigenWoningForfait": eigenwoningforfait,                #   Eigen Woning Forfait# Total gross income
        "AftrekbareUitgavenEigenwoning": aftrekeigenwoning,      #   Aftrek eigenwoning
        "TotaalEigenWoning": totaaleigenwoning,                  #   Totaal  eigen woning       
        "UwDeel": totaaleigenwoning_uwdeel,                      #   Totaal  voor de betreffende persson       
        "InkomenWerkenWoning": inkomen_werk_woning               #   Inkomen werk en woning
        }
    
    # Close the calculator
    calculator_ewf.close()

    return results_inkomen_werkenwoning


def calculate_premies(input_data,person, tussenresultaat):
    """function description"""
    # Premies zijn gebaseerd op het inkomen werk en woning

    inkomenwerkenwoning = tussenresultaat['inkomenwerkenwoning']
    premies_calculator = PremiesVolksverzekeringen(input_data["db_path"])
    results_premies = premies_calculator.bereken_premies(inkomenwerkenwoning, input_data["year"], person["aow_er"])
    tussenresultaat['totaalpremies']= results_premies['totale_premie']

    premies_calculator.close()

    return results_premies

def calculate_box3(input_data, person, tussenresultaat):
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
        deel_box3=person["deel_box3"],
        heeft_partner=person["heeft_partner"],
        year=input_data["year"]
    )

    voordeel_box3 = results_box3["Totaal voordeel Sparen en Beleggen"]

    tussenresultaat['verzamelinkomen'] = tussenresultaat['inkomenwerkenwoning'] + voordeel_box3
    tussenresultaat['InkomstenBelastinBox3'] = results_box3["BOX 3 BELASTING"]
    # Close the calculator
    calculator_box3.close()

    return results_box3

def calculate_ouderenkorting(input_data, person, verzamelinkomen):
    """
    Berekent de ouderenkorting op basis van het verzamelinkomen
    """
    # Initialize the calculator
    calculator_ok = OuderenKorting(input_data["db_path"])

    # Perform the calculation
    results_ouderenkorting = calculator_ok.calculate_korting(verzamelinkomen,  input_data["year"], person["aow_er"])

    # Close the calculator
    calculator_ok.close()

    return results_ouderenkorting

def calculate_ew_forfait(input_data):
    """
    Perform Box 3 tax calculation based on input data. Is onafhankelijk van persoon
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

def calculate_aanslag_for_person(input_data, person_data):
    """
    Calculate the aanslag and all intermediate results for a given person (primary or partner).
    :param input_data: Dictionary containing all input data.
    :param person_data: Dictionary containing data for the specific person (primary or partner).
    :return: A dictionary containing the calculated aanslag, intermediate results, and detailed calculation results.
    """
    # Initialize a dictionary to store intermediate results
    result = {}

    # Perform calculations for the person
    results_box1a = calculate_inkomen_werkenwoning(input_data, person_data, result)
    results_box3 = calculate_box3(input_data, person_data, result)
    results_premies = calculate_premies(input_data, person_data, result)
    results_box1 = calculate_box1(input_data, person_data, result)

    # Extract the aanslag from the results
    aanslag = results_box1['Nieuw_bedrag_aanslag']

    all_results = {
        'input': input_data,
        'box1a': results_box1a,
        'box1': results_box1,
        'premies': results_premies,
        'box3': results_box3,
        "Nieuw_bedrag_aanslag": aanslag
    }
    return all_results




