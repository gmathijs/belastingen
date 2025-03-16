import matplotlib.pyplot as plt
import pandas as pd
from loonheffing import LoonbelastingCalculator

def test_loonbelasting():
    calculator = LoonbelastingCalculator()
    incomes = range(5000, 100001, 1000)  # Income from €5,000 to €100,000 in steps of €1,000
    loonbelastingen = []

    for income in incomes:
        loonbelasting = calculator.bereken_loonheffing(income, 2023,0)
        loonbelastingen.append(loonbelasting)

    # Create a table
    data = {'Income (€)': incomes, 'Loonbelasting (€)': loonbelastingen}
    df = pd.DataFrame(data)
    df.to_csv("test_loonbelasting.csv")
    print("Loonbelasting Table:")

    print(df)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(incomes, loonbelastingen, linestyle='-', color='b')
    plt.title('Loonbelasting vs Income (2023)')
    plt.xlabel('Income (€)')
    plt.ylabel('Loonbelasting (€)')
    plt.grid(True)
    plt.show()

    calculator.close()

if __name__ == '__main__':
    test_loonbelasting()