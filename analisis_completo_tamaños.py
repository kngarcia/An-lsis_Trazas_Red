#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import sys

# Extraer tamaños de paquetes usando tshark
def extraer_tamanos(archivo_pcap):
    comando = ['tshark', '-r', archivo_pcap, '-T', 'fields', '-e', 'frame.len']
    resultado = subprocess.run(comando, capture_output=True, text=True)
    tamanos = [int(x) for x in resultado.stdout.splitlines() if x.strip()]
    return tamanos

# Generar histograma y análisis
def analizar_tamanos(tamanos, archivo_salida):
    # Convertir a DataFrame de pandas
    df = pd.DataFrame(tamanos, columns=['tamaño'])
    
    # Estadísticas básicas
    print("ESTADÍSTICAS DE TAMAÑOS DE PAQUETES")
    print("====================================")
    print(f"Total de paquetes: {len(df)}")
    print(f"Tamaño mínimo: {df['tamaño'].min()} bytes")
    print(f"Tamaño máximo: {df['tamaño'].max()} bytes")
    print(f"Tamaño promedio: {df['tamaño'].mean():.2f} bytes")
    print(f"Desviación estándar: {df['tamaño'].std():.2f} bytes")
    print(f"Percentiles:")
    print(f"  25%: {df['tamaño'].quantile(0.25)} bytes")
    print(f"  50%: {df['tamaño'].quantile(0.50)} bytes")
    print(f"  75%: {df['tamaño'].quantile(0.75)} bytes")
    print(f"  95%: {df['tamaño'].quantile(0.95)} bytes")
    
    # Crear histograma
    plt.figure(figsize=(12, 6))
    n, bins, patches = plt.hist(df['tamaño'], bins=50, alpha=0.7, 
                               color='skyblue', edgecolor='black')
    
    plt.xlabel('Tamaño de paquetes (bytes)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de tamaños de paquetes')
    plt.grid(True, alpha=0.3)
    
    # Guardar gráfica
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Crear tabla de frecuencias
    freq = pd.cut(df['tamaño'], bins=bins).value_counts().sort_index()
    freq_relativa = freq / len(df)
    
    tabla = pd.DataFrame({
        'Rango': [f"{int(b.left)}-{int(b.right)}" for b in freq.index],
        'Frecuencia': freq.values,
        'Frecuencia Relativa': freq_relativa.values
    })
    
    # Guardar tabla
    tabla.to_csv('tabla_frecuencias_tamanos_streaming.csv', index=False)
    print(f"\nTabla de frecuencias guardada en 'tabla_frecuencias_tamanos_normal.csv'")
    
    return tabla

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 analisis_completo_tamanos.py <archivo.pcap>")
        sys.exit(1)
    
    archivo_pcap = sys.argv[1]
    print(f"Analizando {archivo_pcap}...")
    
    tamanos = extraer_tamanos(archivo_pcap)
    tabla = analizar_tamanos(tamanos, 'histograma_tamanos_streaming.png')
    
    print(f"\nAnálisis completado. Gráfica guardada en 'histograma_tamanos_streaming.png'")