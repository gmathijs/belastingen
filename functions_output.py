"""Output Modules """
import os
from tabulate import tabulate

def handle_output(results_box1, results_box3, premies):
    """
    Format and export the Box 3 tax calculation results.
    """
    # Format and display the results as a table
    table1 = format_table_box1(results_box1)
    table2 = format_table_premies(premies)
    table3 = format_table_box3(results_box3)
    print(table1)
    print(table2)
    print(table3)

    # Define the file name
    filename = "taxes.txt"
    # Check if the file exists before deleting
    if os.path.exists(filename):
        os.remove(filename)

    # Write the table to a text file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(table1+"\n")
        file.write(table2+"\n")
        file.write(table3)

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
        ["Inkomen uit arbeid", f"€{data['Inkomen uit arbeid']:,.2f}"],
        ["Pensioen of uitkering", f"€{data['Pensioen of uitkering']:,.2f}"],
        ["-" * 35, "-" * 23],  # Separator line
        ["Loonheffing", f"€{data['loonheffing']:,.2f}"],
        ["Heffingskorting", f"€{data['heffingskorting']:,.2f}"],
        ["Arbeidskorting", f"€{data['arbeidskorting']:,.2f}"],
        ["Netto Inkomen", f"€{data['netto_inkomen']:,.2f}"]
    ]

    # Format the table with left alignment and pretty formatting
    table = tabulate(table_data, headers=["Description", "Amount"], tablefmt="pretty", colalign=("left", "left"))
    return table

def format_table_premies(data):
    """
    Format the premies results as a table. 
    """
    table_data = [
        ["AOW Premie", f"€{data['premie_aow']:,.0f}"],
        ["ANW Premie", f"€{data['premie_anw']:,.0f}"],
        ["WLZ Premie", f"€{data['premie_wlz']:,.0f}"],
        ["Premies Totaal ", f"€{data['totale_premie']:,.0f}"],
        ["-" * 35, "-" * 23]  # Separator line
    ]

    # Format the table with left alignment and pretty formatting
    table = tabulate(table_data, headers=["Description", "Amount"], tablefmt="pretty", colalign=("left", "left"))
    return table

def format_table_box3(data):
    """
    Format the results as a table using tabulate.
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
    table = tabulate(table_data, headers=["Description", "Amount"], tablefmt="pretty", colalign=("left", "left"))
    return table

def export_to_json(data, filename):
    """
    Export the results to a JSON file.
    """
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def export_to_csv(data, filename):
    """
    Export the results to a CSV file.
    """
    import csv
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Description", "Amount"])
        for key, value in data.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    writer.writerow([f"{key} - {subkey}", subvalue])
            else:
                writer.writerow([key, value])

