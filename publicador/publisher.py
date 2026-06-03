import time
import random
import json
import paho.mqtt.client as mqtt


# Configuración del Broker Público de Pruebas
BROKER = "broker.hivemq.com"
PUERTO = 1883
TOPICO = "unmsm/callao/camara"


def conectar_mqtt():
    # Inicializar cliente MQTT utilizando la API moderna v2
    client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
    
    print(f"Conectando al broker {BROKER}...")
    client.connect(BROKER, PUERTO, 60)
    return client

def main():
    cliente = conectar_mqtt()
    cliente.loop_start() # Iniciar el bucle de red de fondo
    
    camaras = [101, 102]
    contador = 0
    try:
        while True:
            # Generar datos simulados del sensor
            #temperatura = round(random.uniform(15.0, 35.0), 2)
            #datos_sensor = {
            #    "sensor_id": 404,
             #   "timestamp": time.time(),
              #  "valor": temperatura,
               # "unidad": "Celsius"
            #}
            camara_id = camaras[contador % 2]
            topico = f"{TOPICO}/{camara_id}/telemetria"

            # Generar falla cada 5 mensajes
            if contador % 5 == 0 and contador != 0:

                # Alternar tipos de error
                if contador % 10 == 0:
                    valor = "ERROR_SENSOR"
                else:
                    valor = 200

            else:
                valor = round(random.uniform(15.0, 35.0), 2)

            datos_sensor = {
                "sensor_id": camara_id,
                "timestamp": time.time(),
                "valor": valor,
                "unidad": "Celsius"
            }
            # Serializar diccionario a JSON string
            mensaje = json.dumps(datos_sensor)
            
            # Publicar el mensaje con QoS 1 (Asegurar entrega)
            info = cliente.publish(TOPICO, mensaje, qos=1)
            info.wait_for_publish() # Bloquear hasta asegurar el envío
            
            print(f"[PUBLISHER] Enviado a {TOPICO}: {mensaje}")
            contador += 1
            time.sleep(3) # Esperar 3 segundos
            
    except KeyboardInterrupt:
        print("\nDeteniendo publicador...")
    finally:
        cliente.loop_stop()
        cliente.disconnect()

if __name__ == "__main__":
    main()

