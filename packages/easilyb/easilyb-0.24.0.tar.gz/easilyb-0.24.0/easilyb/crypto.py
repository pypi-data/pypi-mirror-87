from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto import Random
from Crypto.PublicKey.pubkey import pubkey
from base64 import b64encode, b64decode


def generate_rsa_key(key_size=2048):
    key = RSA.generate(key_size, Random.new().read)
    private, public = key, key.publickey()
    return public, private


def import_key(key):
    if isinstance(key, pubkey):
        return key
    return RSA.importKey(key)


def sign(message, private_key, base64_encode=True):
    private_key = import_key(private_key)
    if isinstance(message, str):
        message = message.encode()
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA512.new()
    digest.update(message)
    signature = signer.sign(digest)
    if base64_encode:
        signature = b64encode(signature)
    return signature


def verify(message, signature, public_key, base64_decode=True):
    public_key = import_key(public_key)
    if isinstance(message, str):
        message = message.encode()
    if base64_decode:
        signature = b64decode(signature)
    signer = PKCS1_v1_5.new(public_key)
    digest = SHA512.new()
    digest.update(message)
    return signer.verify(digest, signature)
