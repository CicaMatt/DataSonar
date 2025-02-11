from Crypto import Random
from Crypto.Cipher import AES
import base64

def encrypt(message, key=None, key_size=256):
    def pad(s):
        return s + bytes([AES.block_size - len(s) % AES.block_size]) * (AES.block_size - len(s) % AES.block_size)

    padded_message = pad(message)

    if key is None:
        key = Random.new().read(key_size // 8)

    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return base64.b64encode(iv + cipher.encrypt(padded_message))  # Encode to base64

def decrypt(ciphertext, key):
    unpad = lambda s: s[:-s[-1]]
    ciphertext = base64.b64decode(ciphertext) # Decode from base64
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[AES.block_size:])) 

    return plaintext

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as f: # Read in binary mode
        plaintext = f.read()
    enc = encrypt(plaintext, key)
    with open(file_name, 'wb') as f: # Write in binary mode
        f.write(enc)


def decrypt_file(file_name, key):
    with open(file_name, 'rb') as f:  # Read in binary mode
        ciphertext = f.read()
    dec = decrypt(ciphertext, key)
    with open(file_name, 'wb') as f:  # Write in binary mode
        f.write(dec)



key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

encrypt_file('to_enc.txt', key)
decrypt_file('to_enc.txt', key)