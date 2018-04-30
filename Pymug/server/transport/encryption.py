from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

def load_server_key(keypath):
    f = open(keypath, 'rt')
    k = RSA.import_key(f.read())
    f.close()
    return k.exportKey()

def private_decrypt(key, ciphertext):
    keyobj = RSA.importKey(key)
    cipher = PKCS1_OAEP.new(key)
    payload = cipher.decrypt(ciphertext)
    return payload

def symmetric_encrypt(key, payload):
    cipher

def symmetric_decrypt(key, ciphertext):