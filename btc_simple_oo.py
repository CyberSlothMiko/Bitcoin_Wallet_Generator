#!/usr/bin/env python3

from secp256k1 import PrivateKey
import hashlib
import base58
import datetime

VersionByte = "00"
WIFByte = "80"

reset = "\u001b[0m"
green = "\u001b[32m"
magenta = "\u001b[35m"

def main():
    generate_keypair()
    generate_publickey()
    generate_privatekey()
    generate_output()

def generate_keypair():
    global NewKeyPair
    NewKeyPair = PrivateKey()

def generate_publickey():
    global Public_Key_Output
    pubkey_ripmd160hashed = hashlib.new('ripemd160',hashlib.sha256(NewKeyPair.pubkey.serialize()).digest()).hexdigest()
    Public_Key_Output = base58.b58encode(bytes.fromhex(VersionByte + pubkey_ripmd160hashed + hashlib.sha256(hashlib.sha256(bytes.fromhex(VersionByte + pubkey_ripmd160hashed)).digest()).hexdigest()[0:8]))

def generate_privatekey():
    global WIF_Key_Output
    WIF_Key_Output = base58.b58encode(bytes.fromhex(WIFByte + NewKeyPair.serialize() + hashlib.sha256(hashlib.sha256(bytes.fromhex(WIFByte + NewKeyPair.serialize())).digest()).hexdigest()[0:8]))

def generate_output():
    print ("==================================================================================")
    print (green + "Bitcoin Private Key (WIF)  : " + reset + magenta + WIF_Key_Output.decode() + reset)
    print (green + "Bitcoin Public Key (P2PKH) : " + reset + magenta + Public_Key_Output.decode() + reset)
    print ("==================================================================================")

if __name__ == "__main__":
    """ Main entry point of the program"""

    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print("Time to complete: " + str(end_time - start_time))
    print("==================================================================================")