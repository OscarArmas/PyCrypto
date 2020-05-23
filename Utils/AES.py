from base64 import b64encode,b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad

def generarKey():
    key = b64encode(get_random_bytes(24)).decode("utf-8")
    return key
def cifrar(mensaje,key):
    print("Cifrando con la llave: ",key)
    key = b64decode(key)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(mensaje, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    return ct,iv
def descifrar(ct,key,iv):
    try:
        key = b64decode(key)
        iv = b64decode(iv)
        ct = b64decode(ct)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
    except:
        return b"El mensaje o la firma fueron alterados"
    return pt
