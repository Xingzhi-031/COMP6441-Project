from Crypto.PublicKey import DSA
from Crypto.Random import random
from Crypto.Hash import SHA256

def generate_dh_keypair():
    # Generate key pair and extract (p, q, g) params
    key = DSA.generate(2048)
    priv = key.x
    pub = key.y
    return priv, pub, (key.p, key.q, key.g)

def compute_shared_secret(peer_pub, my_priv, params):
    # Basic DH: (peer_pub)^my_priv mod p -> then SHA-256
    p, _, _ = params
    s = pow(peer_pub, my_priv, p)
    return SHA256.new(str(s).encode()).digest()
