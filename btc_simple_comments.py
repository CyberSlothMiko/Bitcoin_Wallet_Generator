#!/usr/bin/env python3

##### DEPENDANCIES #####
from secp256k1 import PrivateKey
import hashlib
import base58

##### VERSION BYTES #####
VersionByte = "00"
WIFByte = "80"

##### COLOURS #####
reset = "\u001b[0m"
green = "\u001b[32m"
magenta = "\u001b[35m"

################################### GENERATE SECP256K1 KEY-PAIR ###################################

NewKeyPair = PrivateKey()

################################### GENERATE PUBLIC KEY ###################################

# Use Hashlib to hash bytecode pubkey_bc to sha256 as byte code (digest)
pubkey_sha256hashed = hashlib.sha256(NewKeyPair.pubkey.serialize()).digest()

# Use Hashlib to take sha256 as byte code (digest) and hash it using RIPEMD-160
pubkey_ripmd160hashed = hashlib.new('ripemd160',pubkey_sha256hashed).digest()

# Append 00 to the RIPEMD-160 hash 
pubkey_versionbyte = VersionByte + pubkey_ripmd160hashed.hex()

# Use Hashlib to hash bytecode pubkey_bc to sha256 as byte code (digest)
pubkey_sha256hashed_versionbyte = hashlib.sha256(bytes.fromhex(pubkey_versionbyte)).digest()

# Use Hashlib to ake the sha256 hash with version code and hash it using SHA256
pubkey_2_sha256hashed_versionbyte = hashlib.sha256(pubkey_sha256hashed_versionbyte).digest()

# Convert to Hex and take the first 4 byes
checksum = pubkey_2_sha256hashed_versionbyte.hex()[0:8]

# Append the checksum to the RIPMD-160 version byte hash
BinaryBitcoinAddress = pubkey_versionbyte + checksum

# Hash 25 byte Binary Bitcoin Address with BASE58
Public_Key_Output = base58.b58encode(bytes.fromhex(BinaryBitcoinAddress))

################################### PRIVATE KEY TO WIF ###################################

# Add the main-net byte to the private key
privkey_mainnet_byte = WIFByte + NewKeyPair.serialize()

# Perform SHA256 on the extended private key
privkey_sha256hashed_versionbyte = hashlib.sha256(bytes.fromhex(privkey_mainnet_byte)).digest()

# Perform SHA256 on the SHA256(extended private key)
privkey_sha256hashed_versionbyte2 = hashlib.sha256(privkey_sha256hashed_versionbyte).digest()

# Take the first 4 bytes of SHA256(SHA256(extended private key)) this is the checksum
privkey_checksum = privkey_sha256hashed_versionbyte2.hex()[0:8]

# Add the checksum to the extended private key
privkey_final = privkey_mainnet_byte + privkey_checksum

# Base58 check encode the privkey_final top get the WIF format
WIF_Key_Output = base58.b58encode(bytes.fromhex(privkey_final))

################################### OUTPUT ###################################
print ('==================================================================================')
print (green + "Bitcoin Private Key (WIF)        : " + reset + magenta + WIF_Key_Output.decode() + reset)
print (green + "Bitcoin Public Key               : " + reset + magenta + Public_Key_Output.decode() + reset)
print ('==================================================================================')