#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import sys
from datetime import datetime

def extraer_tiempos(archivo_pcap):
    comando = ['tshark', '-r', archivo_pcap, '-T', 'fields', '-e', 'frame.time_epoch']
    resultado = subprocess.run(comando, capture_output=True, text=True)
    tiempos = [float(x) for x in resultado.stdout.splitlines() if x.strip()]
    return tiempos

def analizar_tiempos(tiempos, archivo_salida):
    # Calcular diferencias entre paquetes consecutivos
    diferencias = np.diff(tiempos)
    
    # Convertir a DataFrame
    df = pd.DataFrame(diferencias, columns=['diferencia'])
    
    # Estadísticas básicas
    print("ESTADÍSTICAS DE TIEMPOS ENTRE LLEGADAS")
    print("======================================")
    print(f"Total de intervalos: {len(df)}")
    print(f"Tiempo mínimo: {df['diferencia'].min():.6f} segundos")
    print(f"Tiempo máximo: {df['diferencia'].max():.6f} segundos")
    print(f"Tiempo promedio: {df['diferencia'].mean():.6f} segundos")
    print(f"Desviación estándar: {df['diferencia'].std():.6f} segundos")
    
    # Crear histograma
    plt.figure(figsize=(12, 6))
    n, bins, patches = plt.hist(df['diferencia'], bins=50, alpha=0.7, 
                               color='lightcoral', edgecolor='black')
    
    plt.xlabel('Tiempo entre llegadas (segundos)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de tiempos entre llegadas de paquetes')
    plt.grid(True, alpha=0.3)
    
    # Guardar gráfica
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Crear tabla de frecuencias
    freq = pd.cut(df['diferencia'], bins=bins).value_counts().sort_index()
    freq_relativa = freq / len(df)
    
    tabla = pd.DataFrame({
        'Rango': [f"{b.left:.6f}-{b.right:.6f}" for b in freq.index],
        'Frecuencia': freq.values,
        'Frecuencia Relativa': freq_relativa.values
    })
    
    # Guardar tabla
    tabla.to_csv('tabla_frecuencias_tiempos_streaming.csv', index=False)
    print(f"\nTabla de frecuencias guardada en 'tabla_frecuencias_tiempos_streaming.csv'")
    
    return tabla

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 analisis_tiempos.py <archivo.pcap>")
        sys.exit(1)
    
    archivo_pcap = sys.argv[1]
    print(f"Analizando {archivo_pcap}...")
    
    tiempos = extraer_tiempos(archivo_pcap)
    tabla = analizar_tiempos(tiempos, 'histograma_tiempos_streaming.png')
    
    print(f"\nAnálisis completado. Gráfica guardada en 'histograma_tiempos_streaming.png'")