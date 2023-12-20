import requests
from datetime import datetime
import json


def size_column_excel(writer, sheet, name):
    for column in sheet:
        column_length = max(sheet[column].astype(str).map(len).max(), len(column))
        col_idx = sheet.columns.get_loc(column)
        writer.sheets[name].set_column(col_idx, col_idx, column_length)
    return writer


def send_log_ekl(message):
    try:
        # Verifica que el mensaje esté presente
        if not message:
           print({'error': 'El campo "message" es requerido.'})

        # Construye la URL y realiza la petición a Elasticsearch
        index_name = 'quotation-microservice'
        url = f'http://localhost:9200/{index_name}/_doc'
        payload = {
            'message': message,
            'timestamp': str(datetime.now())
        }

        # Establecer el tipo de contenido a application/json
        headers = {
            "Content-Type": "application/json"
        }

        # Realiza la petición POST a Elasticsearch
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        # Verifica la respuesta de Elasticsearch
        if response.status_code == 201:
           print({'success': f'Log enviado: {message}'})
        else:
           print({'error': 'Error al enviar el log a Elasticsearch.'})
           print(response.text)

    except Exception as e:
       print({'error': f'Error inesperado: {str(e)}'})