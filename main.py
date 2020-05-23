import eel
from Utils import RSA as rsa
from base64 import b64encode, b64decode
from Utils.Init import loadData
import re
from Utils.Store import guardarContactos
from Utils import AES
global keys
global contactos

keys,contactos = loadData()
def main():
    print("Datos cargados")
    eel.init('gui')
    eel.start('index.html', port=8080)    # Start

@eel.expose
def cifrarRSA(mensaje,key):
    print("Hola")
    mensaje = mensaje.encode()
    public = rsa.importKey(key)

    cifrado = b64encode(rsa.encrypt(mensaje, public)).decode()
    print(cifrado)

    resultado = cifrado
    eel.ActualizarCifrarTextoRSA(resultado)
    return

@eel.expose
def cifrarMensaje(mensaje,destinatario):
    mensaje = mensaje.encode()
    if not destinatario in contactos:
        resultado = "Destinatario no encontrado :("
    else:
        contacto = contactos[destinatario]
        key = contacto["AES"]
        ct,iv = AES.cifrar(mensaje,key)
        private = keys[1]
        firma = b64encode(rsa.sign(mensaje, private, "SHA-512")).decode()
        resultado = "--- INICIO MENSAJE CIFRADO ---\n%s\n%s\n%s\n--- FIN MENSAJE CIFRADO ---"%(ct,iv,firma)
    eel.ActualizarCifrarTexto(resultado)
@eel.expose
def descifrarMensaje(ct,emisor):
    if not emisor in contactos:
        resultado = "Destinatario no encontrado :("
    result = re.search('--- INICIO MENSAJE CIFRADO ---(.|\s)+--- FIN MENSAJE CIFRADO ---', ct,re.M)
    if result == None:
        print("ummm")
        return
    contacto = contactos[emisor]
    result = result.group(0)
    result = result.replace("--- INICIO MENSAJE CIFRADO ---\n","")
    result = result.replace("\n--- FIN MENSAJE CIFRADO ---","")
    mensaje,iv,firma = result.split("\n")
    mensaje = AES.descifrar(mensaje,contacto["AES"],iv)
    public = rsa.importKey(contacto["RSA"])
    valido = rsa.verify(mensaje, b64decode(firma),public)
    eel.ActualizarDescifrarTexto(mensaje.decode(),valido)

@eel.expose
def generarAESKey():
    key = AES.generarKey()
    print(key)
    eel.ActualizarAES(key)

@eel.expose
def frontReady():
    if not contactos:
        eel.ActualizarContactos(["No hay contactos"])
    else:
        eel.ActualizarContactos(list(contactos.keys()))

@eel.expose
def nuevoContacto(nombre,RSAKey,AESKey):
    contactos[nombre] = {"RSA":RSAKey.encode(),"AES":AESKey.encode()}
    guardarContactos(contactos)
    eel.ActualizarContactos(list(contactos.keys())) # Actualizar contactos

@eel.expose
def descifrarRSA(mensajeCifrado):
    private = keys[1]
    mensaje = rsa.decrypt(b64decode(mensajeCifrado),private).decode()
    eel.ActualizarDescifrarTextoRSA(mensaje)
if __name__ == '__main__':
    main()
