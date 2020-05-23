import os.path
from os import path,remove,mkdir
from Utils import RSA
import pickle

__KEY_SIZE__ = 2048
#contactos = { "nombre":"path.key"}
def removeKeys():
    # Borramos llaves previas
    if path.exists("data/public.pem"): os.remove("data/public.pem")
    if path.exists("data/private.pem"): os.remove("data/private.pem")
def createKeys():
    print("Generando llaves...")
    (public,private) = RSA.newkeys(__KEY_SIZE__)
    with open("data/private.pem",'wb') as f:
        f.write(private.exportKey('PEM'))
    with open("data/public.pem",'wb') as f:
        f.write(public.exportKey('PEM'))
        return public,private

def loadData():
    if not path.exists("data/public.pem") or not  path.exists("data/private.pem") :
        print("Una de las llaves no fué encontrada, borrando....")
        removeKeys()
        keys = createKeys()
    else:
        with open("data/public.pem",'rb') as f:
            public = RSA.importKey(f.read())
        with open("data/private.pem",'rb') as f:
            private = RSA.importKey(f.read())
        keys = public,private
    if not path.exists("data/contactos.data"):
        print("Creando contactos")
        contactos = {}
        pickle.dump( contactos, open( "data/contactos.data", "wb"))
    else:
        contactos = pickle.load(open( "data/contactos.data", "rb"))
    if not path.exists("archivos"):
        os.mkdir("archivos")
    return keys,contactos
