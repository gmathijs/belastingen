""" 
    Main module to calculate the income tax
    Updated for year 2020 towards 2024
    GMa Last update 2025-03
"""
from functions_output import handle_output
from functions_input import get_user_input, check_input
from function_calculations import (calculate_aanslag_for_person)

def main():
    """# Main program """ 

    # Step 1: Get user input 
    input_data = get_user_input()
    input_data = check_input(input_data)
    all_results ={}
    all_results ['input'] = input_data
    all_results['totaal'] = {}


    # Bereken eerste persoon
    all_results['primary']= calculate_aanslag_for_person(input_data, input_data['primary'])
    aanslag = all_results ['primary'] ['Nieuw_bedrag_aanslag']

    # Bereken tweede persoon indien die er is.
    if input_data['primary']['heeft_partner']:
        all_results['partner']= calculate_aanslag_for_person(input_data, input_data['partner'])
        aanslag_totaal = aanslag + all_results ['partner'] ['Nieuw_bedrag_aanslag']


    all_results['totaal']['aanslag'] = aanslag_totaal

    # Step 3: Handle output (formatting and exporting)
    handle_output(all_results)   #functions_output

    if aanslag < 0:
        print(f"U krijgt terug : €{-aanslag_totaal:,.0f}")
    else:
        print(f"U moet betalen : €{aanslag_totaal:,.0f}")


if __name__ == "__main__":
    main()