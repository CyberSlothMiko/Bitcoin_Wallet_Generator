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

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wallets", help = "Example: -w 5 (Generates 5 Wallets)", type=int, required = False, default = "1")
    parser.add_argument("-ft", "--filetype", help = "Example: -ft fancy_txt (Generates fancy_txt output file)", required = False, choices=['fancy_txt','priv_pub_nl','priv_nl','pub_nl','priv_pub_csv','priv_csv','pub_csv','priv_pub_csv_seperate','priv_pub_nl_seperate'])

    args = parser.parse_args()

    main(args.wallets, args.filetype)

def main(wallets,filetype):
    """ Main Entry Point of the Script """

    global NewWallets
    NewWallets = 0

    global wallet_counter
    wallet_counter = wallets

    while NewWallets < wallets:
        generate_wallet(filetype)
        NewWallets += 1
    
    if filetype == None:
        print ("==================================================================================")

def generate_wallet(filetype):
    """ Handles all wallet Generation & Output """

    generate_keypair()
    generate_publickey()
    generate_privatekey()
    generate_output(filetype)

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
    
def generate_output(filetype):
    """ Handles all output for the Script """

    match filetype:
        case "fancy_txt":
            print("fancy_txt")
            filename = "fancy_txt.txt"
            generate_fancy_txt(filename)

        case "priv_pub_nl":
            print("priv_pub_nl")
            filename = "priv_pub_nl.txt"
            generate_priv_pub_nl(filename)

        case "priv_nl":
            print("priv_nl")
            filename = "priv_nl.txt"
            generate_priv_nl(filename)

        case "pub_nl":
            print("pub_nl")
            filename = "pub_nl.txt"
            generate_pub_nl(filename)

        case "priv_pub_csv":
            print("priv_pub_csv")
            filename = "priv_pub_csv.csv"
            generate_priv_pub_csv(filename)

        case "priv_csv":
            print("priv_csv")
            filename = "priv_csv.csv"
            generate_priv_csv(filename)

        case "pub_csv":
            print("pub_csv")
            filename = "pub_csv.csv"
            generate_pub_csv(filename)

        case "pub_csv":
            print("pub_csv")
            filename = "pub_csv.csv"
            generate_pub_csv(filename)

        case "priv_pub_csv_seperate":
            print("priv_pub_csv_seperate")
            filename = "priv_seperate.csv"
            filename_pub = "pub_seperate.csv"
            priv_pub_csv_seperate(filename,filename_pub)

        case "priv_pub_nl_seperate":
            print("priv_pub_nl_seperate")
            filename = "priv_seperate.txt"
            filename_pub = "pub_seperate.txt"
            priv_pub_nl_seperate(filename,filename_pub)

        case _:
            print ("==================================================================================")
            print (green + "Bitcoin Private Key (WIF)  : " + reset + magenta + WIF_Key_Output.decode() + reset)
            print (green + "Bitcoin Public Key (P2PKH) : " + reset + magenta + Public_Key_Output.decode() + reset)

def generate_fancy_txt(filename):

    last_line = ""

    if os.path.isfile(filename):
        with open(filename, 'rb') as output_file:
            try:
                output_file.seek(-2, os.SEEK_END)
                while output_file.read(1) != b'\n':
                    output_file.seek(-2, os.SEEK_CUR)
            except OSError:
                output_file.seek(0)
            last_line = output_file.readline().decode()
    if last_line == "==================================================================================":
        with open(filename, 'a') as output_file:
            output_file.write("\n")
            output_file.write("Bitcoin Private Key (WIF)  : " + WIF_Key_Output.decode() + "\n")
            output_file.write("Bitcoin Public Key (P2PKH) : " + WIF_Key_Output.decode() + "\n")
    else:
        with open(filename, 'a') as output_file:
            output_file.write("==================================================================================\n")
            output_file.write("Bitcoin Private Key (WIF)  : " + WIF_Key_Output.decode() + "\n")
            output_file.write("Bitcoin Public Key (P2PKH) : " + WIF_Key_Output.decode() + "\n")

    if NewWallets == wallet_counter-1:
        with open(filename, 'a') as output_file:
            output_file.write("==================================================================================")

def generate_priv_pub_nl(filename):
    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + "\n")
        output_file.write(Public_Key_Output.decode() + "\n")

def generate_priv_nl(filename):
    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + "\n")

def generate_pub_nl(filename):
    with open(filename, 'a') as output_file:
        output_file.write(Public_Key_Output.decode() + "\n")

def generate_priv_pub_csv(filename):
    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + ",")
        output_file.write(Public_Key_Output.decode() + ",\n")

def generate_priv_csv(filename):
    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + ",\n")

def generate_pub_csv(filename):
    with open(filename, 'a') as output_file:
        output_file.write(Public_Key_Output.decode() + ",\n")

def priv_pub_nl_seperate(filename,filename_pub):
    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + "\n")
    with open(filename_pub, 'a') as output_file:
        output_file.write(Public_Key_Output.decode() + "\n")

def priv_pub_csv_seperate(filename,filename_pub):
    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + "\n")
    with open(filename_pub, 'a') as output_file:
        output_file.write(Public_Key_Output.decode() + "\n")

if __name__ == "__main__":
    """ Main entry point of the program"""

    argcheck()