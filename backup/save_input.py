import csv
import os
from functions_input import get_user_input, check_input
from typing import Dict

def write_input_to_csv(data, filename):
    """
    Write the input data dictionary to a CSV file.
    
    Args:
        data (dict): The input data dictionary to be saved
        filename (str): Path to the CSV file to be created
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['key', 'value'])
        
        # Write top-level items
        for key, value in data.items():
            if key in ['primary', 'partner', 'programsetting']:
                continue  # Skip nested structures for now
            writer.writerow([key, value])
        
        # Write nested structures with prefix
        for section in ['primary', 'partner', 'programsetting']:
            if section in data:
                for key, value in data[section].items():
                    writer.writerow([f"{section}.{key}", value])

def read_input_from_csv(filename):
    """
    Read the input data from a CSV file back into a dictionary.
    
    Args:
        filename (str): Path to the CSV file to be read
    
    Returns:
        dict: The reconstructed input data dictionary
    """
    data = {
        "primary": {},
        "partner": {},
        "programsetting": {}
    }
    
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        
        for row in reader:
            if len(row) < 2:
                continue
                
            key, value = row[0], row[1]
            
            # Handle nested structures
            if '.' in key:
                section, subkey = key.split('.', 1)
                if section in data:
                    # Convert numeric values
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            if value.lower() == 'true':
                                value = True
                            elif value.lower() == 'false':
                                value = False
                    data[section][subkey] = value
            else:
                # Convert numeric values for top-level
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        if value.lower() == 'true':
                            value = True
                        elif value.lower() == 'false':
                            value = False
                data[key] = value
    
    # Run the input validation check
    data = check_input(data)
    
    return data

def get_last_part(s):
    """split string laatstestuk na de punt """
    return s.rsplit('.', 1)[-1]

# Example usage:
if __name__ == "__main__":
    # Get the sample input data
    input_data = get_user_input()
    
    # Write to CSV
    naam_csv = get_last_part(input_data['primary']['naam']) + ".csv"
    write_input_to_csv(input_data, naam_csv)
    print("Data written to tax_input.csv")
    
    # Read back from CSV
    read_data = read_input_from_csv(naam_csv)
    print("\nData read back from CSV:")
    print(read_data)


def validate_tax_csv(file_path: str) -> Dict:
    """
    Validate the structure and content of a tax input CSV file.
    
    Args:
        file_path: Path to the CSV file to validate
        
    Returns:
        dict: Parsed data if valid, raises ValueError if invalid
    """
    # Check if file exists and is readable
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    if not os.access(file_path, os.R_OK):
        raise ValueError(f"Cannot read file: {file_path}")

    required_fields = {
        'opslagnaam', 'db_path', 'year', 'AftrekEW', 'spaargeld', 
        'belegging', 'ontroerend', 'WOZ_Waarde', 'schuld', 'divident',
        'primary.naam', 'primary.aow_er', 'primary.heeft_partner',
        'primary.Inkomen', 'primary.Pensioen', 'primary.deel_box1',
        'primary.deel_box3', 'primary.deel_div', 'primary.al_ingehouden',
        'primary.voorlopige_aanslag', 'programsetting.mode'
    }

    numeric_fields = {
        'year', 'AftrekEW', 'spaargeld', 'belegging', 'ontroerend',
        'WOZ_Waarde', 'schuld', 'divident', 'primary.Inkomen',
        'primary.Pensioen', 'primary.deel_box1', 'primary.deel_box3',
        'primary.deel_div', 'primary.al_ingehouden',
        'primary.voorlopige_aanslag', 'programsetting.mode'
    }

    boolean_fields = {
        'primary.aow_er', 'primary.heeft_partner'
    }

    data = {}
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        if reader.fieldnames is None or 'key' not in reader.fieldnames or 'value' not in reader.fieldnames:
            raise ValueError("CSV must contain 'key' and 'value' columns")

        for row in reader:
            if not row['key'] or not row['value']:
                continue  # Skip empty rows
            data[row['key']] = row['value']

    # Check for missing required fields
    missing_fields = required_fields - set(data.keys())
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    # Validate numeric fields
    for field in numeric_fields:
        if field in data:
            try:
                data[field] = float(data[field])
            except ValueError:
                raise ValueError(f"Invalid numeric value for {field}: {data[field]}")

    # Validate boolean fields
    for field in boolean_fields:
        if field in data:
            val = data[field].lower()
            if val not in {'0', '1', 'true', 'false', 'yes', 'no'}:
                raise ValueError(f"Invalid boolean value for {field}: {data[field]}")
            data[field] = val in {'1', 'true', 'yes'}

    # Additional validation rules
    if data['primary.heeft_partner']:
        partner_fields = {
            'partner.naam', 'partner.aow_er', 'partner.heeft_partner',
            'partner.Inkomen', 'partner.Pensioen', 'partner.al_ingehouden',
            'partner.voorlopige_aanslag'
        }
        missing_partner = partner_fields - set(data.keys())
        if missing_partner:
            raise ValueError(f"Missing partner fields: {', '.join(missing_partner)}")

    return data
