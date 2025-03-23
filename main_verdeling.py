""" 
    Main module to calculate the income tax
    Updated for year 2020 towards 2024
    GMa Last update 2025-03
"""
import csv
from functions_output import handle_output
from functions_input import get_user_input, check_input
from function_calculations import (calculate_aanslag_for_person)


def main():
    """# Main program """ 
    # Initialize variables to store the minimum aanslag and corresponding values


    # Step 1: Get user input 
    input_data = get_user_input()
    input_data = check_input(input_data)
    all_results ={}
    all_results ['input'] = input_data
    all_results['totaal'] = {}

    min_aanslag = float('inf')  # Start with a very high value
    best_deel_box1 = 0
    best_deel_box3 = 0
    best_deel_div = 0
    teller = 0
    resultaat_lijst = []  # Initialize an empty list to store results

    for deel_box1 in [i * 0.05 for i in range(21)]:
        input_data['primary']['deel_box1'] = deel_box1
        input_data['partner']['deel_box1'] = 1-deel_box1

        # Loop over deel_box3 from 0 to 1 in steps of 0.1
        for deel_box3 in [i * 0.05 for i in range(21)]:
            input_data['primary']['deel_box3'] = deel_box3
            input_data['partner']['deel_box3'] = 1-deel_box3

            # Loop over deel_div from 0 to 1 in steps of 0.1
            for deel_div in [i * 0.05 for i in range(21)]:
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
                    'aanslag': aanslag,
                    'deel_box1': deel_box1,
                    'deel_box3': deel_box3,
                    'deel_div': deel_div
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


    print(f"Eind resultaat min aanslag :  €{min_aanslag:,.0f}  voor box1 {best_deel_box1} voor box3 {best_deel_box3}  voor div {best_deel_div}    ")
    # Define the CSV file name
    csv_file = 'resultaat.csv'

    # Open the CSV file for writing
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

    # Bereken eerste persoon
    all_results['primary']= calculate_aanslag_for_person(input_data, input_data['primary'])
    aanslag = all_results ['primary'] ['Nieuw_bedrag_aanslag']

    # Bereken tweede persoon indien die er is.
    if input_data['primary']['heeft_partner']:
        all_results['partner']= calculate_aanslag_for_person(input_data, input_data['partner'])
        aanslag = all_results ['primary'] ['Nieuw_bedrag_aanslag'] + all_results ['partner'] ['Nieuw_bedrag_aanslag']

    all_results['totaal']['aanslag'] = aanslag

    # Step 3: Handle output (formatting and exporting)
    handle_output(all_results)   #functions_output

    if min_aanslag < 0:
        print(f"U krijgt terug:  €{min_aanslag:,.0f}  voor box1 {best_deel_box1} voor box3 {best_deel_box3}  voor div {best_deel_div}    ")
    else:
        print(f"U moet betalen:  €{min_aanslag:,.0f}  voor box1 {best_deel_box1} voor box3 {best_deel_box3}  voor div {best_deel_div}    ")


if __name__ == "__main__":
    main()