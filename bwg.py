from secp256k1 import PrivateKey, PublicKey

privkey = PrivateKey()
privkey_der = privkey.serialize()
assert privkey.deserialize(privkey_der) == privkey.private_key

sig = privkey.ecdsa_sign(b'hello')
verified = privkey.pubkey.ecdsa_verify(b'hello', sig)
assert verified

sig_der = privkey.ecdsa_serialize(sig)
sig2 = privkey.ecdsa_deserialize(sig_der)
vrf2 = privkey.pubkey.ecdsa_verify(b'hello', sig2)
assert vrf2

pubkey = privkey.pubkey
pub = pubkey.serialize()

pubkey2 = PublicKey(pub, raw=True)
assert pubkey2.serialize() == pub
assert pubkey2.ecdsa_verify(b'hello', sig)

print(privkey_der)
print(pub)