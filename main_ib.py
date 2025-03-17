""" 
    Main module to calculate the income tax
    Updated for year 2020 towards 2024
    GMa Last update 2025-03
"""
from functions_output import handle_output
from functions_input import get_user_input
from function_calculations import calculate_box1, calculate_box3, calculate_premies


def main():
    """ Main program """
    # Step 1: Get user input 
    input_data = get_user_input()

    # Step 2: Perform calculations
    results_box1 = calculate_box1(input_data)
    results_premies = calculate_premies(input_data)

    results_box3 = calculate_box3(input_data)

    # Step 3: Handle output (formatting and exporting)
    handle_output(results_box1, results_box3, results_premies)

if __name__ == "__main__":
    main()