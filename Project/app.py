# Importa las librerías necesarias
from flask import Flask, render_template, request, jsonify  # Flask y herramientas para el backend web
import json, csv, os  # Manejo de archivos JSON, CSV y operaciones con el sistema operativo
from math import radians, sin, cos, sqrt, atan2  # Funciones matemáticas para calcular distancias geográficas

# Crea la aplicación Flask
app = Flask(__name__)

# Rutas de los archivos
RESPONSES_FILE = 'data/responses.csv'  # Archivo donde se guardan las respuestas del formulario
LUGARES_FILE = 'data/places.json'      # Archivo con los datos de los sitios turísticos

# Si el archivo de respuestas no existe o está vacío, lo crea con encabezados
if not os.path.exists(RESPONSES_FILE) or os.path.getsize(RESPONSES_FILE) == 0:
    with open(RESPONSES_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rango de Edad', 'Genero', 'Region de Residencia', 'Intereses', 'Latitud', 'Longitud'])

# Ruta raíz: carga el formulario HTML
@app.route('/')
def form():
    return render_template('index.html')

# Ruta que recibe el formulario al hacer submit
@app.route('/submit', methods=['POST'])
def submit():
    # Obtiene los datos del formulario
    edad = request.form.get('Rango de Edad') or None
    genero = request.form.get('Género') or None
    origen = request.form.get('Región de Residencia') or None
    intereses = request.form.getlist('Intereses') or None  # Lista de intereses seleccionados
    lat = request.form.get('Latitud') or None
    lon = request.form.get('Longitud') or None

    # Guarda la información del usuario en el CSV
    with open(RESPONSES_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([edad, genero, origen, ','.join(intereses), lat, lon])

    # Carga el JSON con los lugares turísticos
    with open(LUGARES_FILE, 'r', encoding='utf-8') as f:
        lugares = json.load(f)

    # Intenta convertir las coordenadas a números decimales
    try:
        lat = float(lat)
        lon = float(lon)
    except:
        lat = lon = None  # Si no son válidas, se ignora el cálculo de distancia

    # Lista donde se almacenarán los lugares recomendados
    lugares_filtrados = []

    # Recorre todos los lugares del archivo JSON
    for lugar in lugares:
        # Verifica si alguno de los intereses del usuario coincide con el tipo de atractivo
        if any(i in lugar.get('tipo_de_atractivo', '') for i in intereses):
            # Si hay coordenadas del usuario y del lugar, calcula la distancia
            if lat and lon and 'formato_google_maps' in lugar and lugar['formato_google_maps']:
                try:
                    # Extrae latitud y longitud del lugar desde el campo 'formato_google_maps'
                    lat_str, lon_str = lugar['formato_google_maps'].split(',')
                    lat_lugar = float(lat_str.strip())
                    lon_lugar = float(lon_str.strip())

                    # Aplica la fórmula Haversine para calcular la distancia
                    R = 6378.0  # Radio de la Tierra en kilómetros
                    dlat = radians(lat_lugar - lat)
                    dlon = radians(lon_lugar - lon)
                    a = sin(dlat / 2) ** 2 + cos(radians(lat)) * cos(radians(lat_lugar)) * sin(dlon / 2) ** 2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))
                    distancia = round(R * c, 2)  # Redondea a 2 decimales
                    lugar['distancia_km'] = distancia  # Añade la distancia al diccionario del lugar
                except:
                    lugar['distancia_km'] = None  # Si ocurre un error, deja la distancia vacía

            # Agrega el lugar filtrado (con o sin distancia) a la lista de resultados
            lugares_filtrados.append(lugar)

    # Renderiza la plantilla con los lugares recomendados
    return render_template('recomendaciones.html', lugares=lugares_filtrados)

# Inicia la aplicación en modo desarrollo si se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)
