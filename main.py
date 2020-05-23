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
    #if not (destinatario in contactos):
    #    resultado = "Destinatario no encontrado :("
    #else:
    public = rsa.importKey(key)
    #private = keys[1]
    cifrado = b64encode(rsa.encrypt(mensaje, public)).decode()
    print(cifrado)
    #firma = b64encode(rsa.sign(mensaje, private, "SHA-512")).decode()
    #resultado = "--- INICIO MENSAJE CIFRADO ---\n%s\n%s\n--- FIN MENSAJE CIFRADO ---"%(cifrado,firma)
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
    '''regex = r"--- INICIO MENSAJE CIFRADO ---(.+)--- FIN MENSAJE CIFRADO ---"
    data = re.findall(regex,mensaje.replace("\n","\\n"),re.MULTILINE)
    try:
        data = data[0]
    except:
        print("No se encontro el mensaje")
        return
    data = data.replace("--- INICIO MENSAJE CIFRADO ---\\n","")
    data = data.replace("\\n--- FIN MENSAJE CIFRADO ---","")
    print(data)'''
    private = keys[1]
    mensaje = rsa.decrypt(b64decode(mensajeCifrado),private).decode()
    eel.ActualizarDescifrarTextoRSA(mensaje)
if __name__ == '__main__':
    main()

'''
msg1 = b"Hola mundo, usuario a"
msg2 = b"Hola mundo, usuario b"
keysize = 2048
(public, private) = rsa.newkeys(keysize)
encrypted = b64encode(rsa.encrypt(msg1, public))
decrypted = rsa.decrypt(b64decode(encrypted), private)
signature = b64encode(rsa.sign(msg1, private, "SHA-512"))
verify = rsa.verify(msg1, b64decode(signature), public)

print(private.exportKey('PEM'))
print(public.exportKey('PEM'))
print("Encrypted: " ,encrypted)
print("Decrypted: '%s'" % decrypted)
print("Signature: ",signature)
print("Verify: %s" % verify)
data = rsa.verify(msg2, b64decode(signature), public)
print(data)
'''
