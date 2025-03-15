import matplotlib.pyplot as plt
import pandas as pd
from vermogensbelasting import VermogensBelasting

def test_vermogensbelasting():
    calculator = VermogensBelasting()
    incomes = range(5000, 100001, 1000)  # Income from €5,000 to €100,000 in steps of €1,000
    vermogensbelastingen = []

    for income in incomes:
        # Assume bank balance = income, no investments, no real estate, no debts
        vermogensbelasting = calculator.bereken_vermogensbelasting(2023, income, 0, 0, 0)
        vermogensbelastingen.append(vermogensbelasting)

    # Create a table
    data = {'Income (€)': incomes, 'Vermogensbelasting (€)': vermogensbelastingen}
    df = pd.DataFrame(data)
    df.to_csv("test_vermogensbelasting")
    print("Vermogensbelasting Table:")
    print(df)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(incomes, vermogensbelastingen, marker='o', linestyle='-', color='purple')
    plt.title('Vermogensbelasting vs Income (2023)')
    plt.xlabel('Income (€)')
    plt.ylabel('Vermogensbelasting (€)')
    plt.grid(True)
    plt.show()

    calculator.close()

if __name__ == '__main__':
    test_vermogensbelasting()