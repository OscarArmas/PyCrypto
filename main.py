import eel
from Utils import RSA as rsa
from base64 import b64encode, b64decode
from Utils.Init import loadData
global keys
global contactos

keys,contactos = loadData()
def main():
    print("Datos cargados")
    eel.init('gui')
    eel.start('index.html', options={"port":8080})    # Start


@eel.expose
def cifrar(mensaje,destinatario):
    mensaje = mensaje.encode()
    public = keys[0]
    private = keys[1]
    cifrado = b64encode(rsa.encrypt(mensaje, public)).decode()
    firma = b64encode(rsa.sign(mensaje, private, "SHA-512")).decode()
    resultado = "--- INICIO MENSAJE CIFRADO ---\n%s\n%s\n--- FIN MENSJAE CIFRADO ---"%(cifrado,firma)
    eel.ActualizarCifrarTexto(resultado)
    return resultado

def descifrar(mensaje):
    print("descifrar")

if __name__ == '__main__':
    main()
