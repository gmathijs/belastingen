"""Output Modules """
import os
import csv
import json
from tabulate import tabulate 


def handle_output(all_results):
    """
    Format and export the Box 3 tax calculation results.
    """
    # Extract individual results from the dictionary
    input = all_results['input']
    results_box1a = all_results['box1a']  
    results_box1 = all_results['box1']
    results_box3 = all_results['box3']
    premies = all_results['premies']
    ouderenkorting = all_results['ouderenkorting']
    
    # Format and display the results as a table
    table1 = format_table_box1a(results_box1a)          #Inkomen werk en Woning"
    table4a = format_table_box3_grof(results_box3)      #Box 3 Inkomsten Belasting Grof"
    table2 = format_table_box1(results_box1)
    table3 = format_table_premies(premies)
    table4 = format_table_box3(results_box3)
    table5 = format_table_ok(ouderenkorting)
    print(table1)   
    print(table4a)
    print(table2)
    print(table3)
    print(table4)
    print(table5)

    # Define the file name
    filename = "taxes.txt"
    # Check if the file exists before deleting
    if os.path.exists(filename):
        os.remove(filename)

    # Write the table to a text file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(table1+"\n")
        file.write(table4a+"\n")       
        file.write(table2+"\n")
        file.write(table3+"\n")
        file.write(table4+"\n")
        file.write(table5)

    # Open the text file automatically (Mac-specific)
    os.system(f"open {filename}")  # This works on macOS

    
    # Export the results to JSON and CSV
    # export_to_json(results_box3, "box3_results.json")
    # export_to_csv(results_box3, "box3_results.csv")

def format_table_box1(data):
    """
    Format the Box 1 results as a table.
    """
    table_data = [
        ["Inkomen uit arbeid", f"€{data['Inkomen uit arbeid']:,.0f}"],
        ["Pensioen of uitkering", f"€{data['Pensioen of uitkering']:,.0f}"],
        ["Inkomen werk en woning", f"€{data['Inkomen uit Werk en Woning']:,.0f}"],
        ["-" * 35, "-" * 23],  # Separator line
        ["Loonheffing", f"€{data['loonheffing']:,.0f}"],
        ["Heffingskorting", f"€{data['heffingskorting']:,.0f}"],
        ["Arbeidskorting", f"€{data['arbeidskorting']:,.0f}"],
        ["EigenWoning Forfait", f"€{data['arbeidskorting']:,.0f}"],       
        ["Netto Inkomen", f"€{data['netto_inkomen']:,.0f}"]
    ]

    # Format the table with left alignment and pretty formatting
    table = tabulate(table_data, headers=["Box1 berekening", "Amount"], tablefmt="pretty", colalign=("left", "right"))
    return table

def format_table_box1a(data):
    """
    Format the Box 1 results as a table.
    """
    table_data = [
        ["Totaal Bruto Inkomen ", f"€{data['BrutoInkomen']:,.0f}"],
        ["Inkomsten Eigen Woning", f"€{data['EigenWoningForfait']:,.0f}"],
        ["Aftrekbare Uitgaven eigen Woning", f"€{data['AftrekbareUitgavenEigenwoning']:,.0f}"],
        ["- Eigen Woning toerekenen", f"{data['UwDeel']*100:.0f}%"],
        ["-" * 35, "-" * 23],  # Separator line
        ["Inkomen Werk en Woning", f"€{data['InkomenWerkenWoning']:,.0f}"]
    ]

    # Format the table with left alignment and pretty formatting
    table = tabulate(table_data, headers=["Inkomen Werk en Woning", "Amount"], tablefmt="pretty", colalign=("left", "right"))
    return table

def format_table_ok(data):
    """
    Format the ouderenkorting results as a table. 
    """
    table_data = [
        ["VerzamelInkomen", f"€{data['Verzamelinkomen']:,.0f}"],
        ["Ouderenkorting", f"€{data['Ouderenkorting']:,.0f}"],
        ["-" * 35, "-" * 23]  # Separator line
    ]

    # Format the table with left alignment and pretty formatting
    table = tabulate(table_data, headers=["Ouderen Korting", "Bedrag"], tablefmt="pretty", colalign=("left", "right"))
    return table


def format_table_premies(data):
    """
    Format the premies volksverzekeringen results as a table. 
    """
    table_data = [
        ["AOW Premie", f"€{data['premie_aow']:,.0f}"],
        ["ANW Premie", f"€{data['premie_anw']:,.0f}"],
        ["WLZ Premie", f"€{data['premie_wlz']:,.0f}"],
        ["Premies Totaal ", f"€{data['totale_premie']:,.0f}"],
        ["-" * 35, "-" * 23]  # Separator line
    ]

    # Format the table with left alignment and pretty formatting
    table = tabulate(table_data, headers=["Premies Volksverzekering", "Bedrag"], tablefmt="pretty", colalign=("left", "right"))
    return table

def format_table_box3(data):
    """
    Format the results as a table using tabulate.
    This lists all the details of Box 3
    """
    table_data = [
        ["Fiscale partner", data["Fiscale partner"]],
        ["Vermogen", ""],
        ["Bank en Spaargeld", f"€{data['Vermogen']['Bank en Spaargeld']:,.0f}"],
        ["Beleggingen", f"€{data['Vermogen']['Beleggingen']:,.0f}"],
        ["Ontroerende zaken in NL", f"€{data['Vermogen']['Ontroerende zaken in NL']:,.0f}"],
        ["Totaal vermogen", f"€{data['Vermogen']['Totaal vermogen']:,.0f}"],
        ["-" * 35, "-" * 23],  # Separator line
        ["Forfaitair rendement vermogen", ""],
        ["Spaargeld", f"€{data['Forfaitair rendement vermogen']['Spaargeld']:,.0f}"],
        ["Beleggingen", f"€{data['Forfaitair rendement vermogen']['Beleggingen']:,.0f}"],
        ["Ontroerende zaken in NL", f"€{data['Forfaitair rendement vermogen']['Ontroerende zaken in NL']:,.0f}"],
        ["Belastbaar rendement op vermogen", f"€{data['Forfaitair rendement vermogen']['Belastbaar rendement op vermogen']:,.0f}"],
        ["-" * 35, "-" * 23],  # Separator line
        ["Schulden", f"€{data['Schulden']['Schulden']:,.0f}"],
        ["Drempel schulden", f"€{data['Schulden']['Drempel schulden']:,.0f}"],
        ["Totaal schulden", f"€{data['Schulden']['Totaal schulden']:,.0f}"],
        ["Belastbaar rendement op schulden", f"€{data['Schulden']['Belastbaar rendement op schulden']:,.0f}"],
        ["-" * 35, "-" * 23],  # Separator line
        ["Totaal rendementsgrondslag", f"€{data['Rendementsgrondslag']['Totaal rendementsgrondslag']:,.0f}"],
        ["Totaal Belastbaar rendement", f"€{data['Rendementsgrondslag']['Totaal Belastbaar rendement']:,.0f}"],
        ["-" * 35, "-" * 23],  # Separator line
        ["Heffingsvrij vermogen", f"€{data['Heffingsvrij vermogen']:,.0f}"],
        ["Grondslag sparen en beleggen", f"€{data['Grondslag sparen en beleggen']:,.0f}"],
        ["-" * 30, "-" * 23],  # Separator line
        ["Verdeling", ""],
        ["Uw deel", data['Verdeling']['Uw deel']],
        ["Mijn grondslag sparen en beleggen", f"€{data['Verdeling']['Mijn grondslag sparen en beleggen']:,.0f}"],
        ["Rendements grondslag uw aandeel", data['Verdeling']['Rendements grondslag uw aandeel']],
        ["-" * 35, "-" * 23],  # Separator line
        ["Rendements Percentage", data['Rendements Percentage']],
        ["Totaal voordeel Sparen en Beleggen", f"€{data['Totaal voordeel Sparen en Beleggen']:,.0f}"],
        ["Box 3 Belasting percentage", data['Box 3 Belasting percentage']],
        ["BOX 3 BELASTING", f"€{data['BOX 3 BELASTING']:,.0f}"]
    ]

    # Format the table with left alignment and pretty formatting
    table = tabulate(table_data, headers=["Box3 (nieuw)", "Bedrag"], tablefmt="pretty", colalign=("left", "right"))
    return table

def format_table_box3_grof(data):
    """
    Format the results as a table using tabulate.
    This is the summary of Box 3
    """
    table_data = [
        ["Totaal vermogen", f"€{data['Vermogen']['Totaal vermogen']:,.0f}"],
        ["Grondslag sparen en beleggen", f"€{data['Grondslag sparen en beleggen']:,.0f}"],
        ["Uw deel", data['Verdeling']['Uw deel']],
        ["-" * 35, "-" * 23],  # Separator line
        ["Mijn grondslag sparen en beleggen", f"€{data['Verdeling']['Mijn grondslag sparen en beleggen']:,.0f}"],
        ["Rendements grondslag uw aandeel", data['Verdeling']['Rendements grondslag uw aandeel']],
        ["Box 3 Belasting percentage", data['Box 3 Belasting percentage']],
        ["BOX 3 BELASTING", f"€{data['BOX 3 BELASTING']:,.0f}"]
    ]

    # Format the table with left alignment and pretty formatting
    table = tabulate(table_data, headers=["Box3 Summary", "Bedrag"], tablefmt="pretty", colalign=("left", "right"))
    return table


def export_to_json(data, filename):
    """
    Export the results to a JSON file.
    """

    with open(filename, 'w',encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def export_to_csv(data, filename):
    """
    Export the results to a CSV file.
    """

    with open(filename, 'w', newline='',encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Description", "Amount"])
        for key, value in data.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    writer.writerow([f"{key} - {subkey}", subvalue])
            else:
                writer.writerow([key, value])

