# PyCrypto
## Introducción
Como parte integral de la formación en la asignatura de Cryptography se llevará a cabo un proyecto para complementar los conocimientos adquiridos aplicándolos a un problema de la vida real, por lo que para el proyecto Secure letters se plantea analizar e identificar las distintas primitivas criptográficas, además de realizar una implementación que ayude a resolver el problema planteado, haciendo uso de las primitivas criptográficas.
## Problemática
> Un grupo de amigos quieren comunicarse entre sí  a través de un canal seguro. Ellos usualmente utilizan emails para ello, saben que la comunicación punto a punto es segura, pero los correos son guardados en texto plano en el servidor. Ellos necesitan emular un canal de comunicación seguro tradicional para mandar mensajes, por ejemplo, el emisor escribe un mensaje, lo firma y pone la carta en un sobre y lo envía al destinatario, pero en un mundo digital, ellos saben que utilizando las primitivas criptográficas pueden “firmar” los mensajes y usando los mecanismos de cifrado “poner la carta en un sobre”. Ayuda a estos amigos a diseñar un software para firmar y hacer la carta confidencial a través de un canal digital

| Primitiva | Razón |
| --- | --- |
| Confidencialidad |  Ya que los mensajes se almacenan en texto claro en un servidor puede quedar expuesto los mensajes intercambiados para el administrador de este servicio, por lo que se necesita utilizar algún mecanismo de cifrado. |
| Autenticación  |  Para verificar que los mensajes recibidos sean del destinatario que dice ser es necesario emular una “firma”, es por esto que utilizaremos una “firma digital” |
| No repudio  |  Para cumplir con el objetivo de tener una manera de firmar el mensaje que se envía haremos uso de una firma digital, con lo cual aseguraremos que ningún usuario niegue lo escrito en el mensaje (no repudio), y además de esta forma el receptor puede tener la seguridad de que el mensaje proviene del emisor correcto |

## Solución propuesta
Ya con las primitivas identificadas y los problema que implican utilizar uno u otro podemos resolver el problema haciendo uso de ambos mecanismos criptográficos, funcionará de la siguiente manera:
1. El usuario A y B crean sus llaves(pública y privada) utilizando RSA
2. El usuario A crea una llave para poder cifrar utilizando AES
3. El usuario A cifra la llave AES utilizando la llave publica de usuario B (de esta forma puede enviar la llave por un canal inseguro)
4. El usuario B descifra la llave y entonces ambas partes ya cuentan con la simétrica para poder comunicarse.
5. Cuando se envía un mensaje la primer parte será el mensaje cifrado, la segunda parte será la firma utilizando su propia llave privada de RSA
Es así cómo pueden usarse ambos algoritmos para poder brindar privacidad (AES) y autenticación (RSA).
## Diagrama
![diagrama](https://raw.githubusercontent.com/JackCloudman/PyCrypto/master/diagrama.jpg)
## Resultado
![resultado](https://raw.githubusercontent.com/JackCloudman/PyCrypto/master/resultado.JPG)
## Instalación
1. Instalar Python 3.7
2. Instala las bibliotecas necesarias.
eel (para la interfaz):
```
pip install Eel==0.10.4
```
pycryptodome (biblioteca criptográfica):
```
pip install pycryptodome
```
## Ejecuta el programa
```
python main.py
```
