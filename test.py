from secp256k1 import PrivateKey, PublicKey

privkey = PrivateKey()

privkey_der = privkey.serialize()
pubkey_der = privkey.pubkey.serialize()

pubkey = privkey.pubkey

pub = pubkey.serialize()

pubkey2 = PublicKey(pub, raw=True)

print(privkey_der)
print(pubkey_der.decode("hex"))