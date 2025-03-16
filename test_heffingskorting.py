import matplotlib.pyplot as plt
import pandas as pd
from heffingskorting import HeffingskortingCalculator

def test_heffingskorting():
    calculator = HeffingskortingCalculator()
    incomes = range(5000, 100001, 1000)  # Income from €5,000 to €100,000 in steps of €1,000
    heffingskortingen = []

    for income in incomes:
        heffingskorting = calculator.bereken_heffingskorting(income, 2024)
        heffingskortingen.append(heffingskorting)

    # Create a table
    data = {'Income (€)': incomes, 'Heffingskorting (€)': heffingskortingen}
    df = pd.DataFrame(data)
    df.to_csv("test-heffingskorting.csv")
    print("Heffingskorting Table:")
    print(df)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(incomes, heffingskortingen, marker='o', linestyle='-', color='g')
    plt.title('Heffingskorting vs Income (2023)')
    plt.xlabel('Income (€)')
    plt.ylabel('Heffingskorting (€)')
    plt.grid(True)
    plt.show()

    calculator.close()

if __name__ == '__main__':
    test_heffingskorting()