from secp256k1 import PrivateKey
import hashlib
import base58

# ===================================================
# Main-Net Version Byte (0x00)
# ===================================================
VersionByte = "00"

# ===================================================
# Colours
# ===================================================
reset = "\u001b[0m"
green = "\u001b[32m"
magenta = "\u001b[35m"

# ===================================================
# Generate Initial SECP256K1 Key-Pair
# ===================================================

# Generate new SECP256K1 Key-pair
NewKeyPair = PrivateKey()

# Private Key in Byte Code
privkey_bc = NewKeyPair.private_key

# Public Key in Byte Code
pubkey_bc = NewKeyPair.pubkey.serialize()

# Private Key in Hex
privkey_hex = NewKeyPair.serialize()

# Public Key in Hex
pubkey_hex = NewKeyPair.pubkey.serialize().hex()

######################################### MANUAL TEST #########################################

#pubkey_bc = bytes.fromhex('0250863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b2352')

#print(pubkey_bc)

######################################### MANUAL TEST END #########################################

# Use Hashlib to hash bytecode pubkey_bc to sha256 as byte code (digest)
pubkey_sha256hashed = hashlib.sha256(pubkey_bc).digest()

# Use Hashlib to take sha256 as byte code (digest) and hash it using RIPEMD-160
pubkey_ripmd160hashed = hashlib.new('ripemd160',pubkey_sha256hashed).digest()

# Append 00 to the RIPEMD-160 hash 
pubkey_versionbyte = VersionByte + pubkey_ripmd160hashed.hex()

# ===================================================
# The Below is Base58 Checking
# Can be implimented in a few ways (diffrent libraries)
# ===================================================

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

################################### OUTPUT ###################################
print("========== SECP256K1 ==========")
print("[Hex]  Private Key                                                     : " + privkey_hex)
print("[Hex]  Public Key                                                      : " + pubkey_hex)
print("[Byte] Private Key                                                     : " + str(privkey_bc))
print("[Byte] Public Key                                                      : " + str(pubkey_bc))
print ('[Hex][Public Key] SHA256 Hash                                          : ' + pubkey_sha256hashed.hex())
print ('[Hex][Public Key] RIPEMD-160 Hash                                      : ' + pubkey_ripmd160hashed.hex())
print ('[Hex][Public Key] RIPEMD-160 Hash + Version Byte                       : ' + pubkey_versionbyte)
print ('[Hex][Public Key] SHA256 Hash (RIPEMD-160 Hash + Version Byte)         : ' + pubkey_sha256hashed_versionbyte.hex())
print ('[Hex][Public Key] SHA256 Second Hash (RIPEMD-160 Hash + Version Byte)  : ' + pubkey_2_sha256hashed_versionbyte.hex())
print ('[Hex][Public Key] SHA256 Checksum (First 4 Bytes of SHA256 Second Hash): ' + checksum)
print ('[Hex][Public Key] RIPEMD-160 Hash + Checksum                           : ' + BinaryBitcoinAddress)
print ('==================================================================================')
print (green + "Bitcoin Public Key: " + reset + magenta + Public_Key_Output.decode() + reset)
print ('==================================================================================')