import pickle
def guardarContactos(contactos):
    print("Guardando contactos...")
    pickle.dump(contactos,open("data/contactos.data", "wb"))
