import matplotlib.pyplot as plt
import pandas as pd
from oudspul.arbeidskorting import ArbeidskortingCalculator

def test_arbeidskorting():
    calculator = ArbeidskortingCalculator()
    incomes = range(0, 150000, 1000)  # Income from €5,000 to €100,000 in steps of €1,000
    arbeidskortingen = []
    year = 2026

    for income in incomes:
        arbeidskorting = calculator.bereken_arbeidskorting(income, year, 1)
        arbeidskortingen.append(arbeidskorting)

    # Create a table
    data = {'Income (€)': incomes, 'Arbeidskorting (€)': arbeidskortingen}
    df = pd.DataFrame(data)
    df.to_csv("test_arbeidskorting.csv")
    print("Arbeidskorting Table:")
    print(df)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(incomes, arbeidskortingen, marker='o', linestyle='-', color='r')
    plt.title(f'Arbeidskorting vs Income ({year})')
    plt.xlabel('Income (€)')
    plt.ylabel('Arbeidskorting (€)')
    plt.grid(True)
    plt.show()

    calculator.close()

if __name__ == '__main__':
    test_arbeidskorting()