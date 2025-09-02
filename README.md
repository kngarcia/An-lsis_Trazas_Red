# Análisis de Tráfico de Red y Disco (Ver documento Trazas_Trafico_Red.pdf)

## Descripción del laboratorio

Este laboratorio realiza un análisis completo del tráfico de red en diferentes escenarios (normal y streaming) junto con un análisis de la distribución de tamaños de archivos en el disco. Incluye captura de paquetes, procesamiento de datos, análisis estadístico y visualización de resultados.

## Herramientas Utilizadas

- **tcpdump**: Captura de paquetes de red
- **Wireshark/tshark**: Análisis de archivos pcap
- **Python 3**: Análisis y procesamiento de datos
- **Librerías Python**: pandas, matplotlib, numpy

## Guía de Uso

### 1. Captura de Paquetes de Red

**Captura básica (50000 paquetes):**
```bash
sudo tcpdump -i any -w captura_red_normal.pcap -c 50000
```

Opciones útiles de tcpdump:
- -i any: Todas las interfaces de red

- -c N: Capturar N paquetes

- port X: Filtrar por puerto específico

- host X.X.X.X: Filtrar por dirección IP

- -s 0: Capturar paquetes completos (sin truncar)

