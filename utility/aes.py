# coding: utf8

from Crypto.Cipher import AES
import base64
import urllib

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


def encrypt(raw, key):
    """
    Returns hex encoded encrypted value!
    """
    cipher = AES.new(key, AES.MODE_ECB)
    enc = cipher.encrypt(pad(raw)).encode('hex')
    return urllib.quote(base64.encodestring(enc))


def decrypt(enc, key):
    """
    Requires hex encoded param to decrypt
    """
    enc = base64.decodestring(urllib.unquote(enc)).decode('hex')
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(enc))
