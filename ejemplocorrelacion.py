import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(filepath):
    df = pd.read_excel(filepath)
    df.columns = df.iloc[0]
    df = df[1:]
    df.columns = [str(col).strip() for col in df.columns]
    return df

def calculate_correlation(df):
    numeric_df = df.select_dtypes(include='number')
    correlation_matrix = numeric_df.corr()
    return correlation_matrix

def plot_correlation_heatmap(correlation_matrix):
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Heatmap de la Matriz de Correlación')
    plt.show()

example_file = 'ruta'

data = load_data(example_file)

correlation_matrix = calculate_correlation(data)
print("Matriz de correlación:")
print(correlation_matrix)

plot_correlation_heatmap(correlation_matrix)
