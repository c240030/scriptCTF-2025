from Crypto.Cipher import AES
import itertools

def key_from_seed(b0,b1):
    return (bin(b0)[2:].zfill(8)+bin(b1)[2:].zfill(8)).encode()

def enc_block(seed_pair, data):
    k = key_from_seed(*seed_pair)
    return AES.new(k, AES.MODE_ECB).encrypt(data)

def dec_block(seed_pair, data):
    k = key_from_seed(*seed_pair)
    return AES.new(k, AES.MODE_ECB).decrypt(data)

X = bytes.fromhex("19574ac010cc9866e733adc616065e6c019d85dd0b46e5c2190c31209fc57727")
Q = bytes.fromhex("0239bcea627d0ff4285a9e114b660ec0e97f65042a8ad209c35a091319541837")
Y = bytes.fromhex("4b3d1613610143db984be05ef6f37b31790ad420d28e562ad105c7992882ff34")

# MITM to find (k3,k4) such that Q = E_k4(E_k3(X))
# Build map of E_k3(X) -> k3
emap = {}
for b0 in range(256):
    for b1 in range(256):
        k3 = (b0,b1)
        mid = enc_block(k3, X)
        emap[mid] = k3
#Knowing length of emap
found_k3k4 = None
for b0 in range(256):
    for b1 in range(256):
        k4 = (b0,b1)
        mid2 = dec_block(k4, Q)
        if mid2 in emap:
            found_k3k4 = (emap[mid2], k4)
            break
    if found_k3k4:
        break
#Knowing value of k3k4
emap2 = {}
for b0 in range(256):
    for b1 in range(256):
        k1 = (b0,b1)
        mid = enc_block(k1, Y)
        emap2[mid] = k1
found_k1k2 = None
for b0 in range(256):
    for b1 in range(256):
        k2 = (b0,b1)
        mid2 = dec_block(k2, Q)
        if mid2 in emap2:
            found_k1k2 = (emap2[mid2], k2)
            break
    if found_k1k2:
        break
###k1k2 found
def seed_to_bytes(seed):
    return bytes(seed)
k1_seed, k2_seed = found_k1k2
def dec_with_seeds(s1,s2, data):
    return dec_block(s1, dec_block(s2, data))

secret = dec_with_seeds(k1_seed, k2_seed, X)
#secret is part of the flag
k1 = seed_to_bytes(k1_seed)  # (101,52) -> b'e4'
k2 = seed_to_bytes(k2_seed)  # (98,51) -> b'b3'
k3 = seed_to_bytes(found_k3k4[0]) # (102,56) -> b'f8'
k4 = seed_to_bytes(found_k3k4[1]) # (100,125) -> b'd}'
flag = secret + k1 + k2 + k3 + k4
print(flag)