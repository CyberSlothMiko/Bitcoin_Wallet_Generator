#!/usr/bin/env python3

from secp256k1 import PrivateKey
import hashlib
import base58
import argparse
import os

VersionByte = "00"
WIFByte = "80"
reset = "\u001b[0m"
green = "\u001b[32m"
magenta = "\u001b[35m"

def argcheck():
    """ Checks CLI Arguments """

    parser = argparse.ArgumentParser(description = "Generate Bitcoin P2PKH Wallets.")
    parser.add_argument("-w", "--wallets", help = "Example: -w 5 (Generates 5 Wallets)", type=int, required = False, default = "1")
    parser.add_argument("-o", "--output", help = "Example: -o example.txt (Stores Wallets in example.txt)", required = False)
    parser.add_argument("-ft", "--filetype", help = "Example: -ft fancy_txt (Generates fancy_txt output file)", required = False, choices=['fancy_txt','priv_pub_nl','priv_nl','pub_nl','priv_pub_csv','priv_csv','pub_csv'])

    argument = parser.parse_args()

    main(argument.wallets, argument.output)

def main(wallets,output):
    """ Main Entry Point of the Script """

    global NewWallets
    NewWallets = 0
    while NewWallets < wallets:
        generate_wallet(wallets,output)
        NewWallets += 1
    
    if output == None:
        print ("==================================================================================")

def generate_wallet(wallets,output):
    """ Handles all wallet Generation & Output """

    generate_keypair()
    generate_publickey()
    generate_privatekey()
    generate_output(wallets,output)

def generate_keypair():
    """ Generates a new SECP256K1 Key-Pair """

    global NewKeyPair
    NewKeyPair = PrivateKey()

def generate_publickey():
    """ Generates Public Key based on SECP256K1 Key-Pair """

    global Public_Key_Output
    pubkey_ripmd160hashed = hashlib.new('ripemd160',hashlib.sha256(NewKeyPair.pubkey.serialize()).digest()).hexdigest()
    Public_Key_Output = base58.b58encode(bytes.fromhex(VersionByte + pubkey_ripmd160hashed + hashlib.sha256(hashlib.sha256(bytes.fromhex(VersionByte + pubkey_ripmd160hashed)).digest()).hexdigest()[0:8]))

def generate_privatekey():
    """ Generates Private Key based on SECP256K1 Key-Pair """

    global WIF_Key_Output
    WIF_Key_Output = base58.b58encode(bytes.fromhex(WIFByte + NewKeyPair.serialize() + hashlib.sha256(hashlib.sha256(bytes.fromhex(WIFByte + NewKeyPair.serialize())).digest()).hexdigest()[0:8]))

def generate_output(wallets,output):
    """ Handles all output for the Script """

    if not output:
        print ("==================================================================================")
        print (green + "Bitcoin Private Key (WIF)  : " + reset + magenta + WIF_Key_Output.decode() + reset)
        print (green + "Bitcoin Public Key (P2PKH) : " + reset + magenta + Public_Key_Output.decode() + reset)

    if output:

        last_line = ""

        if os.path.isfile(output):
            with open(output, 'rb') as f:
                try:  # catch OSError in case of a one line file 
                    f.seek(-2, os.SEEK_END)
                    while f.read(1) != b'\n':
                        f.seek(-2, os.SEEK_CUR)
                except OSError:
                    f.seek(0)
                last_line = f.readline().decode()
        if last_line == "==================================================================================":
            with open(output, 'a') as output_file:
                output_file.write("\n")
                output_file.write("Bitcoin Private Key (WIF)  : " + WIF_Key_Output.decode() + "\n")
                output_file.write("Bitcoin Public Key (P2PKH) : " + WIF_Key_Output.decode() + "\n")
        else:
            with open(output, 'a') as output_file:
                output_file.write("==================================================================================\n")
                output_file.write("Bitcoin Private Key (WIF)  : " + WIF_Key_Output.decode() + "\n")
                output_file.write("Bitcoin Public Key (P2PKH) : " + WIF_Key_Output.decode() + "\n")

        if NewWallets == wallets-1:
            with open(output, 'a') as output_file:
                output_file.write("==================================================================================")

if __name__ == "__main__":
    """ Main entry point of the program"""

    argcheck()