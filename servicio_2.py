import logging
from io import StringIO
import requests
from datetime import datetime

# Configuración del logging
log_stream = StringIO()  # Crea un objeto StringIO para capturar los logs
handler = logging.StreamHandler(log_stream)  # Crea un handler para escribir en el StringIO
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)  # Aplica el formato al handler

logger = logging.getLogger('servicio_2')  # Obtiene el logger
logger.setLevel(logging.DEBUG)  # Establece el nivel de logging
logger.addHandler(handler)  # Añade el handler al logger

def servicio_2(palabra):
    if len(palabra) == 5:
        logger.info('La palabra tiene 5 letras')
    else:
        logger.error('La palabra no tiene 5 letras')

# Obtener la entrada del usuario
palabra = input('Ingrese una palabra de 5 letras: ')

# Llamar a la función
servicio_2(palabra)

def mandar_logs():
    # Captura los logs
    data_log = log_stream.getvalue()  # Obtiene el contenido del StringIO
    
    # Enviar logs a la URL
    url = "http://127.0.0.1:5000/logs"
    headers = {'Authorization': 'def456'}  # Usa la clave API correcta

    # Divide los logs en mensajes individuales si es necesario
    log_messages = data_log.splitlines()

    for log_message in log_messages:
        if log_message.strip():  # Asegúrate de que el mensaje de log no esté vacío
            try:
                # Crea el payload para la solicitud POST
                payload = {
                    'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),  # Usa la hora actual
                    'service_name': 'servicio_2',
                    'severity_level': log_message.split(' - ')[2],  # Extrae el nivel de severidad del mensaje
                    'message': log_message.split(' - ')[3]  # Extrae el mensaje del log
                }
                
                # Envía la solicitud POST
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    print('Log enviado con éxito')
                else:
                    print(f'Error al enviar log: {response.status_code}')
                    
            except requests.RequestException as e:
                print(f'Error al enviar log: {e}')

# Mandar los logs
mandar_logs()







