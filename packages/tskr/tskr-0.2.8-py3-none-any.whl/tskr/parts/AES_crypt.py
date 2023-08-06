
# AES暗号化
# Qiitaより一部改変 (https://qiita.com/tomi_linka/items/3e478d1559e13d832486)

import sys
import base64
import random
from Crypto.Cipher import AES
from hashlib import sha256

class AESCipher(object):
	def __init__(self, key, block_size=32):
		self.bs = block_size
		if len(key) >= len(str(block_size)):
			self.key = key[:block_size]
		else:
			self.key = self._pad(key)

	def generate_salt(self,digit_num):
		DIGITS_AND_ALPHABETS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
		return "".join(random.sample(DIGITS_AND_ALPHABETS, digit_num)).encode()

	def encrypt(self, raw):
		raw = self._pad(raw)
		salt = self.generate_salt(AES.block_size)
		salted = ''.encode()
		dx = ''.encode()
		while len(salted) < 48:
			hash = dx + self.key.encode() + salt
			dx = sha256(hash).digest()
			salted = salted + dx

		key = salted[0:32]
		iv = salted[32:48]

		cipher = AES.new(key, AES.MODE_CBC, iv)
		encoded_bin = base64.b64encode(salt + cipher.encrypt(raw))
		encoded_str = encoded_bin.decode()
		return encoded_str

	def decrypt(self, enc):
		enc_bin = enc.encode()
		enc = base64.b64decode(enc_bin)
		salt = enc[0:16]
		ct = enc[16:]
		rounds = 3

		data00 = self.key.encode() + salt
		hash = {}
		hash[0] = sha256(data00).digest()
		result = hash[0]
		for i in range(1, rounds):
			hash[i] = sha256(hash[i - 1] + data00).digest()
			result += hash[i]

		key = result[0:32]
		iv = result[32:48]
		cipher = AES.new(key, AES.MODE_CBC, iv)
		raw_decoded_text = cipher.decrypt(enc[16:]).decode()
		return self._unpad(raw_decoded_text)

	def _pad(self, s):
		return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

	def _unpad(self, s):
		return s[:-ord(s[len(s)-1:])]
