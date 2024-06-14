import pandas as pd
import matplotlib.pyplot as plt

# Función para cargar datos desde un archivo Excel
def load_data(filepath):
    df = pd.read_excel(filepath)
    df.columns = df.iloc[0]
    df = df[1:]
    df.columns = [str(col).strip() for col in df.columns]
    return df

# Función para calcular estadísticas básicas
def calculate_statistics(df):
    numeric_df = df.select_dtypes(include='number')
    stats = numeric_df.describe(include='all')
    return stats

# Función para detectar datos atípicos
def detect_outliers(df):
    numeric_df = df.select_dtypes(include='number')
    outliers = numeric_df[(numeric_df < (numeric_df.mean() - 3 * numeric_df.std())) | (numeric_df > (numeric_df.mean() + 3 * numeric_df.std()))].dropna(how='all')
    return outliers

# Función para graficar histogramas
def plot_histogram(df, column):
    plt.figure(figsize=(10, 6))
    df[column].hist(bins=20)
    plt.title(f'Histograma de {column}')
    plt.xlabel(column)
    plt.ylabel('Frecuencia')
    plt.grid(False)
    plt.show()


example_file = 'ruta'


data = load_data(example_file)


statistics = calculate_statistics(data)
print("Estadísticas básicas:")
print(statistics)


outliers = detect_outliers(data)
print("\nDatos atípicos:")
print(outliers)


plot_histogram(data, 'Productividad del 1-10')

# Nota: Reemplaza 'path/to/your/excel/file.xlsx' con la ruta real de tu archivo Excel.
