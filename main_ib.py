""" 
    Main module to calculate the income tax
    Updated for year 2020 towards 2024
    GMa Last update 2025-03
"""
from functions_output import handle_output
from functions_input import get_user_input, check_input
from function_calculations import (calculate_box1, calculate_box3, calculate_premies, 
                                   calculate_inkomen_werkenwoning, 
)

def main():
    """ Main program """
    # Step 1: Get user input 
    input_data = get_user_input()
    input_data = check_input(input_data)

    # Step 2: Perform calculations for the primary person
    result1 = {}  # voor de belangrijkste tussen resulaten
    results_1_box1a = calculate_inkomen_werkenwoning(input_data, input_data['primary'], result1)
    # result1['inkomenwerkenwoning']  toegevoegd
    results_1_box3 = calculate_box3(input_data, input_data['primary'],result1)
    # result1['verzamelinkomen'] en tussenresultaat['InkomstenBelastinBox3']toegevoegd
    results_1_premies = calculate_premies(input_data, input_data['primary'], result1)
    # result1['totaalpremies'] toegevoegd
    results_1_box1 = calculate_box1(input_data, input_data['primary'], result1)


    if input_data['primary']['heeft_partner']:
        result2 = {}  # voor de belangrijkste tussen resulaten
        results_2_box1a = calculate_inkomen_werkenwoning(input_data, input_data['partner'], result2)
        # result2['inkomenwerkenwoning']  toegevoegd
        results_2_box3 = calculate_box3(input_data, input_data['partner'],result2)
        # result2['verzamelinkomen'] en tussenresultaat['InkomstenBelastinBox3'] toegevoegd
        results_2_premies = calculate_premies(input_data, input_data['partner'], result2)
        # result2['totaalpremies'] toegevoegd
        results_2_box1 = calculate_box1(input_data, input_data['partner'], result2)

    # Gather all results into one dictionary first for the primary person
    all_results = {
        'input': input_data,
        'primary': {
            'box1a': results_1_box1a,
            'box1': results_1_box1,
            'premies': results_1_premies,
            'box3': results_1_box3,
            }
    }

    # Add partner data if applicable
    if input_data['primary']['heeft_partner']:
        all_results['partner'] = {
            'box1a': results_2_box1a,
            'box1': results_2_box1,
            'premies': results_2_premies,
            'box3': results_2_box3,
        }
    else:
        all_results['partner'] = None  # or {}


    # Step 3: Handle output (formatting and exporting)
    handle_output(all_results)   #functions_output

if __name__ == "__main__":
    main()