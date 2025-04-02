""" 
    Main module to calculate the income tax
    Updated for year 2020 towards 2024
    Gaston: Last update 2025-03
"""
import csv
import os
import tkinter as tk
from tkinter import filedialog
#from functions_output import handle_output
from functions_input import get_user_input, check_input
from function_calculations import (calculate_aanslag_for_person)
from save_input import write_input_to_csv, read_input_from_csv, validate_tax_csv

def ask_input():
    """ Routine to ask if user wants to read an input file """

    # Initialize Tkinter (hidden root window)
    root = tk.Tk()
    root.withdraw()

    # Get directory where main program is located
    initial_dir = os.path.dirname(os.path.abspath(__file__))

    # Ask user to pick a CSV file
    file_path = filedialog.askopenfilename(
        title="Select a input CSV file (or Cancel for manual input)",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialdir=initial_dir  # Set to program's directory
    )

    if file_path:  # User selected a file
        print(f"Using selected file: {file_path}")

        try:
            tax_data = validate_tax_csv(file_path)
            print("Using validated tax data from:", file_path)
            # Continue processing with tax_data
        except ValueError as e:
            print(f"Invalid tax file: {e}, please retry and chooose a valid input file")
            # Handle error (ask to select another file or use manual input)


        input_data = read_input_from_csv(file_path)


    else:  # User cancelled - proceed with manual input
        print("No file selected - using manual input")
        # Initialize variables to store the minimum aanslag and corresponding values
        # Step 1: Get user input 
        input_data = get_user_input()
        input_data = check_input(input_data)

        # Write the input data to a csv file 
        base_name = input_data['opslagnaam']
        filename = f"input_{base_name}.csv"
        counter = 1

        # Delete all input_csv files with the same base name
        while os.path.exists(filename):
            # wis file 
            os.remove(filename)
            filename = f"input_{base_name}_{counter}.csv"  # Fixed to use consistent naming
            counter += 1

        filename = f"{base_name}.txt"
        # Delete all txt  files with the same base name
        while os.path.exists(filename):
            # wis file 
            os.remove(filename)
            filename = f"{base_name}_{counter}.txt"  # Fixed to use consistent naming
            counter += 1     

        filename = f"input_{base_name}.csv"

        write_input_to_csv(input_data, filename)
        print(f"Input data saved to: {filename}")

    return input_data



def belastingen(input_data):
    """Belastingen is the main Module 
    This functions just 
    1. Takes input data  (input_data)
    2. Perform calculations
    3. Return results  (all_results)
    Routine to ask if user wants to read an input file """
    # Validate input structure
    if not isinstance(input_data, dict):
        raise ValueError("Input data must be a dictionary")
    
    # Ensure required keys exist
    required_keys = ['primary', 'programsetting']
    for key in required_keys:
        if key not in input_data:
            raise ValueError(f"Missing required key in input data: {key}")
    
    # If partner exists but no partner data, initialize empty
    if input_data['primary'].get('heeft_partner') and 'partner' not in input_data:
        input_data['partner'] = {}
    #input_data = ask_input()

    all_results ={}
    all_results ['input'] = input_data
    all_results['totaal'] = {}
    besteverdeling = False

    min_aanslag = float('inf')  # Start with a very high value
    best_deel_box1 = 0
    best_deel_box3 = 0
    best_deel_div = 0
    teller = 0
    resultaat_lijst = []  # Initialize an empty list to store results

    if input_data['primary']['heeft_partner'] and input_data['programsetting']['programsetting_mode'] ==2: 
        besteverdeling = True

        """        for step in [0.1, 0.05, 0.01]:
            num_steps = int(1 / step) + 1
            print(f"\nStep size: {step} ({num_steps} steps)")
            for val in [i * step for i in range(num_steps)]:
                print(round(val, 2), end=" ")

        step = 0.1      # Make sure to check if the step size is divisible by 1
                        # steps smaller then 0.05 must be avoide due to calculation time
        assert (1 % step) == 0, f"Step {step} must divide 1 without remainder!"

        num_steps = int(1 / step) + 1"""

        step=0.1
        num_steps=11

        for deel_box1 in [i * step for i in range(num_steps)]:
            input_data['primary']['deel_box1'] = deel_box1
            input_data['partner']['deel_box1'] = 1-deel_box1

            # Loop over deel_box3 from 0 to 1 in steps of 0.1
            for deel_box3 in [i * step for i in range(num_steps)]:
                input_data['primary']['deel_box3'] = deel_box3
                input_data['partner']['deel_box3'] = 1-deel_box3

                # Loop over deel_div from 0 to 1 in steps of 0.1
                for deel_div in [i * step for i in range(num_steps)]:
                    input_data['primary']['deel_div'] = deel_div
                    input_data['partner']['deel_div'] = 1-deel_div

                    # Bereken eerste persoon
                    all_results['primary']= calculate_aanslag_for_person(input_data, input_data['primary'])
                    aanslag = all_results ['primary'] ['Nieuw_bedrag_aanslag']

                    # Bereken tweede persoon indien die er is.
                    if input_data['primary']['heeft_partner']:
                        all_results['partner']= calculate_aanslag_for_person(input_data, input_data['partner'])
                        aanslag = all_results ['primary'] ['Nieuw_bedrag_aanslag'] + all_results ['partner'] ['Nieuw_bedrag_aanslag']

                    # Check if the current aanslag is the lowest so far
                                # Store results in a dictionary
                    resultaat = {
                        'teller': teller,
                        'aanslag': f"€{aanslag:,.0f}",
                        'deel_box1': f"{deel_box1:,.2f}",
                        'deel_box3': f"{deel_box3:,.2f}",
                        'deel_div': f"{deel_div:,.2f}"
                    }

                    # Append the dictionary to the list
                    resultaat_lijst.append(resultaat)
                    
                    teller += 1
                    print(f"{teller} : aanslag :  €{aanslag:,.0f}  box1:{deel_box1:,.2f}    box3:{deel_box3:,.2f}    div: {deel_div:,.2f}  ")

                    if aanslag < min_aanslag:
                        min_aanslag = aanslag
                        best_deel_box1 = deel_box1
                        best_deel_box3 = deel_box3
                        best_deel_div = deel_div

        # On screen output for debugging
        print(f"Eind resultaat min aanslag :  €{min_aanslag:,.0f}  voor box1 {best_deel_box1} voor box3 {best_deel_box3}  voor div {best_deel_div}    ")
        # Define the CSV file name


        # Intermediate output to a csv file for debugging
        csv_file = 'resultaat.csv'
        # Open the CSV file for writing the intermediate results
        with open(csv_file, mode='w', newline='') as file:
            # Extract the fieldnames (column headers) from the first dictionary
            fieldnames = resultaat_lijst[0].keys()
            # Create a DictWriter object
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            # Write the header row
            writer.writeheader()
            # Write the data rows
            for result in resultaat_lijst:
                writer.writerow(result)
        print(f"Results have been written to {csv_file}")

        # Zet de meest gunstige combinatie klaar 
        input_data['primary']['deel_box1'] = best_deel_box1
        input_data['partner']['deel_box1'] = 1-best_deel_box1
        input_data['primary']['deel_box3'] = best_deel_box3
        input_data['partner']['deel_box3'] = 1-best_deel_box3
        input_data['primary']['deel_div'] = best_deel_box3
        input_data['partner']['deel_div'] = 1-best_deel_box3
        # Einde loop beste verdeling 

    # Calculate once for normal and for the optimal results
    # Bereken eerste persoon
    all_results['primary']= calculate_aanslag_for_person(input_data, input_data['primary'])
    aanslag = all_results ['primary'] ['Nieuw_bedrag_aanslag']

    # Bereken tweede persoon indien die er is.
    if input_data['primary']['heeft_partner']:
        all_results['partner']= calculate_aanslag_for_person(input_data, input_data['partner'])
        aanslag = all_results ['primary'] ['Nieuw_bedrag_aanslag'] + all_results ['partner'] ['Nieuw_bedrag_aanslag']

    all_results['totaal']['aanslag'] = aanslag

    # Step 3: Handle output (formatting and exporting to .txt file) In class 
    # handle_output(all_results)   #functions_output

    # Debug messages 
    if besteverdeling:
        if min_aanslag < 0:
            print(f"U krijgt terug:  €{min_aanslag:,.0f}  voor box1 {best_deel_box1} voor box3 {best_deel_box3}  voor div {best_deel_div}    ")
        else:
            print(f"U moet betalen:  €{min_aanslag:,.0f}  voor box1 {best_deel_box1} voor box3 {best_deel_box3}  voor div {best_deel_div}    ")

    # At the end of the function, return the results:
    return all_results
