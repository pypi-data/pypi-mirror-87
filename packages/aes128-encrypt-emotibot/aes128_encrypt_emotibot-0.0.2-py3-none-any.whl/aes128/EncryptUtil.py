import base64
import os
import sys


from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


aes_key = os.environ.get('ENCRYPT_KEY', 'Emotibot20201204')
iv = '1234567890123456'
mode = AES.MODE_CBC

BLOCK_SIZE = 16
KEY_SIZE = 16


def process_key(key):
    if len(key) >= KEY_SIZE:
        return key[:KEY_SIZE]
    key += '0' * (KEY_SIZE - len(key))
    return key


def encrypt(text):
    cryptor = AES.new(process_key(aes_key).encode('utf8'), mode, iv.encode('utf8'))
    padded = pad(bytes(text, encoding='utf8'), BLOCK_SIZE)
    result = cryptor.encrypt(padded)
    return base64.b64encode(result).decode()


def decrypt(text):
    cryptor = AES.new(process_key(aes_key).encode('utf8'), mode, iv.encode('utf8'))
    decode = base64.b64decode(text)
    result = cryptor.decrypt(decode)
    return unpad(result, BLOCK_SIZE).decode('utf8')


if __name__ == '__main__':
    string = sys.argv[1];
    encoded = encrypt(string)
    print(encoded)
    print(decrypt(encoded))
