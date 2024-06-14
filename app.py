import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import expon, norm, lognorm

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            return redirect(url_for('analysis', filename=file.filename))
    return render_template('index.html')

@app.route('/analysis/<filename>')
def analysis(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_excel(filepath)

    df.columns = df.iloc[0]
    df = df[1:]
    df.columns = [str(col).strip() for col in df.columns]

    df = df.apply(pd.to_numeric, errors='ignore')

    numeric_df = df.select_dtypes(include='number')

    analysis_results = {}

    if not numeric_df.empty:
        try:
            analysis_results['stats'] = numeric_df.describe(include='all').to_html()
        except Exception as e:
            analysis_results['stats'] = f"No se pudieron calcular estadísticas básicas: {e}"

        try:
            analysis_results['outliers'] = numeric_df[(numeric_df < (numeric_df.mean() - 3 * numeric_df.std())) | (numeric_df > (numeric_df.mean() + 3 * numeric_df.std()))].dropna(how='all').to_html()
        except Exception as e:
            analysis_results['outliers'] = f"No se pudieron detectar datos atípicos: {e}"

        try:
            analysis_results['semana_mas_asistencia'] = df.loc[df['Días asistidos por semana'].idxmax()]['Semana del año']
        except Exception as e:
            analysis_results['semana_mas_asistencia'] = f"No se pudo determinar: {e}"

        try:
            mes_mas_asistencia = df.groupby('Mes')['Días asistidos por semana'].sum().idxmax()
            analysis_results['mes_mas_asistencia'] = mes_mas_asistencia
        except Exception as e:
            analysis_results['mes_mas_asistencia'] = f"No se pudo determinar: {e}"

        try:
            mes_menos_asistencia = df.groupby('Mes')['Días asistidos por semana'].sum().idxmin()
            analysis_results['mes_menos_asistencia'] = mes_menos_asistencia
        except Exception as e:
            analysis_results['mes_menos_asistencia'] = f"No se pudo determinar: {e}"

        try:
            analysis_results['promedio_asistencia_semana'] = df['Días asistidos por semana'].mean()
        except Exception as e:
            analysis_results['promedio_asistencia_semana'] = f"No se pudo determinar: {e}"

        try:
            promedio_asistencia_mes = df.groupby('Mes')['Días asistidos por semana'].mean().to_dict()
            analysis_results['promedio_asistencia_mes'] = promedio_asistencia_mes
        except Exception as e:
            analysis_results['promedio_asistencia_mes'] = f"No se pudo determinar: {e}"

        try:
            analysis_results['productividad'] = numeric_df['Productividad del 1-10'].mean()
        except Exception as e:
            analysis_results['productividad'] = f"No se pudo determinar: {e}"

        try:
            analysis_results['dieta'] = numeric_df['Seguimiento de dieta 1-10'].mean()
        except Exception as e:
            analysis_results['dieta'] = f"No se pudo determinar: {e}"

        try:
            analysis_results['variacion_peso'] = numeric_df['Variacion en el peso'].sum()
        except Exception as e:
            analysis_results['variacion_peso'] = f"No se pudo determinar: {e}"

    
        try:
            analysis_results['desviacion_estandar'] = numeric_df.std().to_frame().to_html()
        except Exception as e:
            analysis_results['desviacion_estandar'] = f"No se pudo determinar: {e}"

        try:
            analysis_results['mediana'] = numeric_df.median().to_frame().to_html()
        except Exception as e:
            analysis_results['mediana'] = f"No se pudo determinar: {e}"

        try:
            analysis_results['moda'] = numeric_df.mode().to_frame().to_html()
        except Exception as e:
            analysis_results['moda'] = f"No se pudo determinar: {e}"

    
        try:
            plt.figure(figsize=(10, 10))
            sns.scatterplot(data=numeric_df, x='Días asistidos por semana', y='Productividad del 1-10')
            scatterplot_path = os.path.join('static', 'scatterplot.png')
            plt.savefig(scatterplot_path)
            plt.close()
            analysis_results['scatterplot_path'] = scatterplot_path
        except Exception as e:
            analysis_results['scatterplot_path'] = None
            print(f"Error al generar la gráfica de dispersión: {e}")


        try:
            plt.figure(figsize=(10, 10))
            sns.histplot(numeric_df['Días asistidos por semana'], kde=True, stat="density", linewidth=0)
            sns.kdeplot(norm.pdf(numeric_df['Días asistidos por semana']), label='Normal', color='r')
            sns.kdeplot(expon.pdf(numeric_df['Días asistidos por semana']), label='Exponencial', color='g')
            sns.kdeplot(lognorm.pdf(numeric_df['Días asistidos por semana'], 0.954), label='Log-normal', color='b')
            distplot_path = os.path.join('static', 'distplot.png')
            plt.savefig(distplot_path)
            plt.close()
            analysis_results['distplot_path'] = distplot_path
        except Exception as e:
            analysis_results['distplot_path'] = None
            print(f"Error al generar las gráficas de distribución: {e}")

        try:
            plt.figure(figsize=(10, 10))
            numeric_df.hist(figsize=(10, 10))
            histogram_path = os.path.join('static', 'histogram.png')
            plt.savefig(histogram_path)
            plt.close()
            analysis_results['histogram_path'] = histogram_path
        except Exception as e:
            analysis_results['histogram_path'] = None
            print(f"Error al generar el histograma: {e}")

        try:
            plt.figure(figsize=(10, 10))
            sns.boxplot(data=numeric_df, orient="h", palette="Set2")
            boxplot_path = os.path.join('static', 'boxplot.png')
            plt.savefig(boxplot_path)
            plt.close()
            analysis_results['boxplot_path'] = boxplot_path
        except Exception as e:
            analysis_results['boxplot_path'] = None
            print(f"Error al generar el boxplot: {e}")

    return render_template('analysis.html', analysis_results=analysis_results, filename=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
