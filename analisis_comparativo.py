import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leer los datos de los análisis previos
def cargar_datos():
    try:
        # Cargar datos de tráfico
        df_trafico_tamanos = pd.read_csv('tabla_frecuencias_tamanos_streaming.csv')
        df_trafico_tiempos = pd.read_csv('tabla_frecuencias_tiempos_streaming.csv')
        df_disco = pd.read_csv('tabla_frecuencias_disco.csv')
        
        return df_trafico_tamanos, df_trafico_tiempos, df_disco
    except FileNotFoundError as e:
        print(f"Error: {e}. Ejecuta primero los análisis individuales.")
        return None, None, None

def crear_comparativa(df_trafico_tamanos, df_disco):
    # Normalizar frecuencias relativas para comparación
    plt.figure(figsize=(14, 8))
    
    # Preparar datos para el gráfico
    # Para tráfico (primeros 20 rangos)
    rangos_trafico = df_trafico_tamanos['Rango'].head(20)
    frec_trafico = df_trafico_tamanos['Frecuencia Relativa'].head(20)
    
    # Para disco (primeros 20 rangos)
    rangos_disco = df_disco['Rango'].head(20)
    frec_disco = df_disco['Frecuencia Relativa'].head(20)
    
    # Crear gráfico comparativo
    x = np.arange(len(rangos_trafico))
    width = 0.35
    
    plt.bar(x - width/2, frec_trafico, width, label='Tráfico de red', alpha=0.7)
    plt.bar(x + width/2, frec_disco[:len(rangos_trafico)], width, label='Archivos en disco', alpha=0.7)
    
    plt.xlabel('Rangos de tamaño')
    plt.ylabel('Frecuencia relativa')
    plt.title('Comparación de distribuciones: Tráfico de red vs Archivos en disco')
    plt.xticks(x, rangos_trafico, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('comparativa_trafico_disco.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Gr�fica comparativa guardada en 'comparativa_trafico_disco.png'")

if __name__ == "__main__":
    df_trafico_tamanos, df_trafico_tiempos, df_disco = cargar_datos()
    
    if df_trafico_tamanos is not None and df_disco is not None:
        crear_comparativa(df_trafico_tamanos, df_disco)
        print("Análisis comparativo completado.")