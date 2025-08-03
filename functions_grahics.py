""" 
    Module om grafieken weer te geven
    Gaston: Last update 2025-04
"""
# pylint: disable=missing-function-docstring
# pylint: disable=trailing-whitespace
# pylint: disable=line-too-long
# pylint: disable=duplicate-key
# pylint: disable=unused-variable
# Clean and convert values to floats

import matplotlib.pyplot as plt
#from pprint import pprint


def clean_currency(value):
    """Remove '€' and commas, then convert to float."""
    return float(value.replace('€', '').replace(',', ''))

def create_grah_income(resultaat):
    """module create_graph income"""

    #pprint(resultaat)  # Formats with indentation (ideal for medium-sized dicts)


    # Extract data
    incomes = [clean_currency(row['inkomen_arbeid']) for row in resultaat]
    box1_tax = [clean_currency(row['box1_loonheffing']) for row in resultaat]
    box1_total = [clean_currency(row['totale_aanslag']) for row in resultaat]
    premies = [clean_currency(row['premies_volksverz']) for row in resultaat]
    arbeidskorting = [clean_currency(row['arbeidskorting']) for row in resultaat]
    heffingskorting = [clean_currency(row['heffingskorting']) for row in resultaat]
    kortingen = [clean_currency(row['kortingentotaal']) for row in resultaat]

    plt.figure(figsize=(12, 6))

    plt.plot(incomes, box1_tax, label='Box1 Wage Tax', color='blue')
    plt.plot(incomes, box1_total, label='Box1 Total Due', color='red')
    #plt.plot(incomes, premies, label='Premies Volksverz.', color='green')
    #plt.plot(incomes, kortingen, label='Kortingen Totaal', color='purple')

    plt.xlabel('Income (€)')
    plt.ylabel('Amount (€)')
    plt.title('Income vs. Taxes, Premies, and Kortingen')
    plt.legend()
    plt.grid(True)

    # Customize zero axis
    plt.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.7)


    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    ax1.plot(incomes, heffingskorting, label='Heffings Korting', color='blue')
    ax2.plot(incomes, arbeidskorting, label='Arbeids Korting', color='green')
    ax3.plot(incomes, kortingen, label='Kortingen (totaal)', color='red')
    ax1.set_ylabel('Heffing (€)')
    ax2.set_ylabel('Arbeid (€)')
    ax3.set_ylabel('Totaal (€)')
    ax2.set_xlabel('Inkomen Werk en Woning (€)')
    plt.show()
