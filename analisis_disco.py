#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from pathlib import Path

def obtener_tamanos_archivos(directorio):
    tamanos = []
    rutas = []
    
    for ruta, dirs, archivos in os.walk(directorio):
        for archivo in archivos:
            try:
                path_completo = os.path.join(ruta, archivo)
                tamaño = os.path.getsize(path_completo)
                tamanos.append(tamaño)
                rutas.append(path_completo)
            except (OSError, PermissionError):
                # Ignorar archivos inaccesibles
                continue
    
    return tamanos, rutas

def analizar_disco(tamanos, archivo_salida):
    # Convertir a DataFrame
    df = pd.DataFrame(tamanos, columns=['tamaño'])
    
    # Filtrar valores extremos para mejor visualización
    q95 = df['tamaño'].quantile(0.95)
    df_filtrado = df[df['tamaño'] <= q95]
    
    # Estadísticas básicas
    print("ESTADÍSTICAS DE TAMAÑOS DE ARCHIVOS")
    print("====================================")
    print(f"Total de archivos: {len(df)}")
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
    n, bins, patches = plt.hist(df_filtrado['tamaño'], bins=50, alpha=0.7, 
                               color='lightgreen', edgecolor='black')
    
    plt.xlabel('Tamaño de archivos (bytes)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de tamaños de archivos en disco')
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
    tabla.to_csv('tabla_frecuencias_disco.csv', index=False)
    print(f"\nTabla de frecuencias guardada en 'tabla_frecuencias_disco.csv'")
    
    return tabla

if __name__ == "__main__":
    directorio = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"Analizando archivos en: {os.path.abspath(directorio)}")
    
    tamanos, rutas = obtener_tamanos_archivos(directorio)
    tabla = analizar_disco(tamanos, 'histograma_disco.png')
    
    print(f"\nAnálisis completado. Gráfica guardada en 'histograma_disco.png'")