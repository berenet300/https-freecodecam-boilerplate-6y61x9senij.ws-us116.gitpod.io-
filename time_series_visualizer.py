import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Limpiar los datos
df = df.dropna()  # Elimina filas con valores nulos

# Filtrar los datos para eliminar outliers (valores atípicos)
# Por ejemplo, podríamos eliminar las filas donde las visitas sean muy bajas o extremadamente altas
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]



def draw_line_plot():
    # Draw line plot
    # Crear una figura con un tamaño adecuado
    fig, ax = plt.subplots(figsize=(12, 6))  # Crear figura y ejes
    ax.plot(df.index, df['value'], color='red', linewidth=2)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Page Views', fontsize=12)
    ax.grid(True)
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copiar y modificar los datos para el gráfico de barras mensual
    df_bar = df.copy()

    # Crear nuevas columnas para 'year' y 'month' para agrupar los datos
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Agrupar los datos por año y mes, calculando el promedio mensual
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Crear la figura y los ejes para el gráfico
    fig, ax = plt.subplots(figsize=(12, 6))

    # Dibujar el gráfico de barras
    df_bar.plot(kind='bar', ax=ax)
    
    # Añadir título y etiquetas a los ejes
    ax.set_title('Monthly average freeCodeCamp Forum Page Views')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    
    # Añadir leyenda personalizada
    ax.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 
                                      'August', 'September', 'October', 'November', 'December'])
    
    # Guardar el gráfico
    fig.savefig('bar_plot.png')

    # Mostrar el gráfico
    plt.show()

    # Retornar la figura (para que no cambies esta parte)
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

     # Ordenar los meses para que aparezcan en el orden correcto
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=months_order, ordered=True)

    # Dibujar los box plots utilizando Seaborn
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Box plot 1: Año vs Vistas
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Box plot 2: Mes vs Vistas
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
