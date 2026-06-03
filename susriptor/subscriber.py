import json
import paho.mqtt.client as mqtt
from pydantic import BaseModel, Field, ValidationError

# Definimos el esquema de datos esperado usando Pydantic
class LecturaSensor(BaseModel):
    sensor_id: int
    timestamp: float
    valor: float = Field(..., ge=-50.0, le=100.0) # Validación de límites físicos de temperatura
    unidad: str

BROKER = "broker.hivemq.com"
PUERTO = 1883
TOPICO = "unmsm/callao/camara/+/telemetria."

# Callback cuando el cliente recibe una confirmación de conexión (CONNACK) del broker
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Conectado exitosamente al Broker MQTT")
        # Suscribirse al tópico de interés
        client.subscribe(TOPICO)
        print(f"Suscrito a: {TOPICO}")
    else:
        print(f"Error de conexión. Código de retorno: {rc}")

# Callback cuando llega un mensaje publicado al tópico suscrito
def on_message(client, userdata, msg):

    raw_payload = msg.payload.decode()

    print(f"\n[SUBSCRIBER] Mensaje recibido en {msg.topic}")

    try:

        datos_json = json.loads(raw_payload)

        lectura = LecturaSensor(**datos_json)

        print(
            f"-> Datos Validados Correctamente. "
            f"ID: {lectura.sensor_id}"
        )

        print(
            f"-> Temperatura Registrada: "
            f"{lectura.valor} {lectura.unidad}"
        )

        # Alerta de cadena de frío
        if lectura.valor > 5:
            print(
                f"[PELIGRO] ¡Pérdida de cadena de frío en Cámara "
                f"{lectura.sensor_id}! "
                f"Temperatura registrada: {lectura.valor} °C"
            )

    except json.JSONDecodeError:

        with open("log_errores.txt", "a", encoding="utf-8") as archivo:
            archivo.write(
                f"\n[{msg.topic}] JSON inválido\n"
            )
            archivo.write(
                f"Payload recibido: {raw_payload}\n"
            )
            archivo.write("-" * 50 + "\n")

        print("[ERROR] JSON inválido.")

    except ValidationError as e:

        with open("log_errores.txt", "a", encoding="utf-8") as archivo:
            archivo.write(
                f"\n[{msg.topic}] Error de validación\n"
            )
            archivo.write(
                f"Payload recibido: {raw_payload}\n"
            )
            archivo.write(
                f"Detalle: {e}\n"
            )
            archivo.write("-" * 50 + "\n")

        print(
            "[ERROR] Datos descartados y registrados "
            "en log_errores.txt"
        )

def main():
    cliente = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    
    # Asignar los callbacks de eventos de red
    cliente.on_connect = on_connect
    cliente.on_message = on_message
    
    cliente.connect(BROKER, PUERTO, 60)
    
    # Iniciar bucle síncrono infinito para escuchar mensajes de red
    cliente.loop_forever()

if __name__ == "__main__":
    main()
