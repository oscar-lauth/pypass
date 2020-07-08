import sqlite3
import secrets
import string
import hashlib
import hmac
from Crypto.Cipher import AES

def in_vault(check_service, db_path):  # returns if check_service is in vault
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for service in c.execute("SELECT service FROM vault"):
        if check_service == service[0]:
            conn.close()
            return True
    conn.close()
    return False


def pass_gen(length=10):  # generates random password, default length of 10, length>=2
    password = ''
    for i in range(length - 2):
        password += secrets.choice(string.ascii_letters + string.digits)
    r_symbol = secrets.randbelow(length)
    password = password[:r_symbol] + secrets.choice('!@#$%^&*()-_?') + password[r_symbol:]  # ensures 1 symbol
    r_digit = secrets.randbelow(length)
    password = password[:r_digit] + secrets.choice(string.digits) + password[r_digit:]  # ensures at least 1 digit
    return password


def hash_salt_pass(password): # hashes and salts password
    salt = secrets.token_bytes(16)
    hash_pass = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100000)
    return hash_pass, salt

def check_hash_pass(hash_pass, salt, password): # returns if hash_pass matches password
    return hmac.compare_digest(hash_pass,hashlib.pbkdf2_hmac('sha512', 
    password.encode(), salt, 100000))

def enc(password, salt): # encrypts password in AES and gets iv
    cipher_encrypt = AES.new(salt, AES.MODE_CFB)
    ciphered_bytes = cipher_encrypt.encrypt(password.encode())
    iv = cipher_encrypt.iv
    ciphered_data = ciphered_bytes
    return ciphered_data, iv

def dec(ciphered_data, salt, iv): # decrypts password as a string
    cipher_decrypt = AES.new(salt, AES.MODE_CFB, iv=iv)
    deciphered_bytes = cipher_decrypt.decrypt(ciphered_data)
    return deciphered_bytes.decode()