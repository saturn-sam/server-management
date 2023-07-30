import random
import hashlib
import string
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512

def generateDeviceSecret(length=10):
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

def computeMasterKey(mp,ds):
	password = mp.encode()
	salt = ds.encode()
	key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
	return key