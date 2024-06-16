from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

from base64 import b64encode
from base64 import b64decode

from json import dumps, loads

def fetchkey():
    return get_random_bytes(32)

def encrypt(data, key):
    header = b""
    
    cipher = ChaCha20_Poly1305.new(key=key)
    cipher.update(header)
    cipherdata, tag = cipher.encrypt_and_digest(data)

    j = {
        "nonce" : b64encode(cipher.nonce).decode("utf-8"),
        "header" : b64decode(header).decode("utf-8"),
        "cipherdata" : b64encode(cipherdata).decode("utf-8"),
        "tag" : b64encode(tag).decode("utf-8")
    }

    result = dumps(j)
    return result

def decrypt(data, key):
        data = loads(data)

        cipherdata = b64decode(data["cipherdata"])
        tag = b64decode(data["tag"])
        nonce = b64decode(data["nonce"])
        header = b64decode(data["header"])

        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        cipher.update(header)

        plain = cipher.decrypt_and_verify(cipherdata, tag)
        return plain