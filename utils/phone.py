from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import config;

def encrypt_phone_number(phone_number):
    cipher = AES.new(config.MD5_KEY.encode(), AES.MODE_ECB)
    encrypted_number = cipher.encrypt(pad(phone_number.encode(), AES.block_size))
    return b64encode(encrypted_number).decode()

def decrypt_phone_number(encrypted_number):
    cipher = AES.new(config.MD5_KEY.encode(), AES.MODE_ECB)
    decrypted_number = unpad(cipher.decrypt(b64decode(encrypted_number)), AES.block_size)
    return decrypted_number.decode()