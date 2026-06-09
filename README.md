Activamos el entorno:
En la raiz : ./venv/Scripts/activate

En este proyecto encontramos el publicador y el subscriptor los cuales envían datos y reciben de forma asíncrona
utilizando el protocolo MQTT
 1. ¿Por qué no es viable una arquitectura síncrona HTTP REST para interconectar 10 000 sensores industriales
  que reportan datos cada 100 milisegundos? No es viable debido a que al ser síncrono es necesario que el servidor
  esté activo y envíe una confirmación por cada dato que recibe, ello saturaría al sistema que no está preparado para
  esa cantidad de datos en un tiempo tan corto ya que eso implicaría que utilice muchisimos hilos en paralelo para recibirlos,
  dicha cantidad es limitada y no son suficientes, tal genera una sobrecarga denominada Thread Exhaustion. Además de un tardío
  procesamiento.

2. Explique en qué escenarios de desarrollo de software es imperativo utilizar el nivel QoS 2 en lugar de QoS 0
   Como el Qo2 es la calidad de servicio más alta en comparación al Qo0 este debería aplicarse para proyectos que requieren altra precisión
   como por ejemplo el control mediante sensonres en pacientes de enfermedades graves, cuidado o control de productos o elementos altamente
   peligrosos como compuestos radioactivos o explosivos, en software bancario o pasarelas de pago vinculadas a IoT (como estaciones de carga
   de vehículos eléctricos o peajes automáticos), un mensaje duplicado significa cobrarle dos veces al usuario. Tamnbién para softwares de control
   de inventarios ya que un doble mensaje nos brindaría información que no corresponde a la realidad y provocaría una mala gestión logística.

3. El uso ineficiente de protocolos de red aumenta el procesamiento en centros de datos, incrementando la huella de carbono.
¿Cómo contribuye el diseño de protocolos eficientes como MQTT a la sostenibilidad tecnológica de las regiones rurales del Perú?
  Contribuye ampliamente ya que es un protocolo que no requiere una cabecera tan pesada, lo cual la vuelve ligera al momento de su procesamiento.
   Así aunque envíe muchos datos, estos en conjunto no sobrecargaran al sistema y evita que el sistema use demasiados recursos, al no usar tantos recursos
   la energización puede ser abastecida con energía renovable y limpia de baja capacidad, evita muchas veces el uso de refrigeración y el tipo de red que usa
   por la zona que requiere no es una tan avanzada , sino una más sencilla como la 2G. Al consumir poca energía su durabilidad es alta y no requiere el remplazo de
   piezas de forma continua.

