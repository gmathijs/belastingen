""" 
    Main module to calculate the income tax
    Updated for year 2020 towards 2024
    GMa Last update 2025-03
"""
from functions_output import handle_output
from functions_input import get_user_input
from function_calculations import (calculate_box1, calculate_box3, calculate_premies, 
                                   calculate_ouderenkorting, calculate_inkomen_werkenwoning, 
                                   calculate_verzamelinkomen
)

def main():
    """ Main program """
    # Step 1: Get user input 
    input_data = get_user_input()

    # Step 2: Perform calculations the order is irrelevant
    results_box1a = calculate_inkomen_werkenwoning(input_data)
    results_box1 = calculate_box1(input_data)
    results_premies = calculate_premies(input_data)
    results_box3 = calculate_box3(input_data)
    verzamelinkomen = calculate_verzamelinkomen (results_box1a['InkomenWerkenWoning'],results_box3['Totaal voordeel Sparen en Beleggen'])
    results_ok = calculate_ouderenkorting(input_data, verzamelinkomen)

    # Gather all results into one dictionary
    all_results = {
        'input': input_data,
        'box1a': results_box1a,
        'box1': results_box1,
        'premies': results_premies,
        'ouderenkorting': results_ok,
        'box3': results_box3,
        'verzamelinkomen': verzamelinkomen
    }
    # Step 3: Handle output (formatting and exporting)
    handle_output(all_results)   #functions_output

if __name__ == "__main__":
    main()