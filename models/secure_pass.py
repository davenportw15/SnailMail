
from hashlib import sha512 # crypto-secure hashing algorithm
from pbkdf2 import PBKDF2 # key-stretching algorithm
from os import urandom # crypto-secure random number gen

ITERATIONS = 5000
SALT_LEN = 32 # 256-bit salt
KEY_LEN = 64 # 512-bit key
class Password:
    def __init__(self, password):
        self.salt = urandom(SALT_LEN) 
        self.key = PBKDF2(
                passphrase=password,
                salt=self.salt,
                iterations=ITERATIONS,
                digestmodule=sha512
                ).read(KEY_LEN)
        

    def get_hash(self):
        return self.key
    
    def get_salt(self):
        return self.salt

    @staticmethod
    def check_pass(password, key, thesalt):
        return PBKDF2(
                passphrase=password,
                salt=thesalt,
                iterations=ITERATIONS,
                digestmodule=sha512
                ).read(KEY_LEN) \
                == \
                key



