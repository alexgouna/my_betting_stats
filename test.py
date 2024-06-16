import pandas as pd
import numpy as np

# Create a random table with 5 columns and 10 rows
data = np.random.rand(10, 5)
columns = ['A', 'B', 'C', 'D', 'E']
df = pd.DataFrame(data, columns=columns)

# Save the DataFrame to an Excel file
file_path = 'C:/Users/AlexPc/Desktop/random.xlsx'
df.to_excel(file_path, index=False)

print(f"Random table saved to {file_path}")