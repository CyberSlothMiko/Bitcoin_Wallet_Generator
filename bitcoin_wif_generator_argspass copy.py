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
    parser.add_argument("-ft", "--filetype", help = "Example: -ft fancy_txt (Generates fancy_txt output file)", required = False, choices=['fancy_txt','priv_pub_nl','priv_nl','pub_nl','priv_pub_csv','priv_csv','pub_csv'])
    parser.add_argument("-fn", "--filename", help = "Example: -fn example.txt (Generates example.txt output file)", required = False)

    args = parser.parse_args()
    print(args)

    main(args.wallets, args.filetype, args.filename)

def main(wallets,filetype,filename):
    """ Main Entry Point of the Script """

    global NewWallets
    NewWallets = 0
    while NewWallets < wallets:
        generate_wallet(wallets,filetype,filename)
        NewWallets += 1
    
    if filetype == None:
        print ("==================================================================================")

def generate_wallet(wallets,filetype,filename):
    """ Handles all wallet Generation & Output """

    generate_keypair()
    generate_publickey()
    generate_privatekey()
    generate_output(wallets,filetype,filename)

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

def generate_output(wallets,filetype,filename):
    """ Handles all output for the Script """

# no filename, no filetype (Print to Console)
    if not filename and not filetype :
        print ("==================================================================================")
        print (green + "Bitcoin Private Key (WIF)  : " + reset + magenta + WIF_Key_Output.decode() + reset)
        print (green + "Bitcoin Public Key (P2PKH) : " + reset + magenta + Public_Key_Output.decode() + reset)

# No filename, filetype = "fancy_txt" (Save to Output.txt)
    if not filename and filetype == "fancy_txt" or filetype == "priv_pub_nl" or filetype == "priv_nl" or filetype == "pub_nl" or filetype == "priv_pub_csv" or filetype == "priv_csv" or filetype == "pub_csv":

        last_line = ""

        match filetype:
            case "fancy_txt":
                print("fancy_txt")
                filename = "output.txt"
                generate_fancytext(wallets,filetype,filename)

            case "priv_pub_nl":
                print("priv_pub_nl")
                filename = "output.txt"
                generate_priv_pub_nl(wallets,filetype,filename)

            case "priv_nl":
                print("priv_nl")
                filename = "output.txt"
                generate_priv_nl(wallets,filetype,filename)

            case "pub_nl":
                print("pub_nl")
                filename = "output.txt"
                generate_pub_nl(wallets,filetype,filename)

            case "priv_pub_csv":
                print("priv_pub_csv")
                filename = "output.csv"
                generate_priv_pub_csv(wallets,filetype,filename)

            case "priv_csv":
                print("priv_csv")
                filename = "output.csv"
                generate_priv_csv(wallets,filetype,filename)

            case "pub_csv":
                print("pub_csv")
                filename = "output.csv"
                generate_pub_csv(wallets,filetype,filename)
            
            case _:
                print("default fancy_txt")
                filename = "output.txt"
                generate_fancytext(wallets,filetype,filename)

def generate_fancytext(wallets,filetype,filename):

        last_line = ""

        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                try:  # catch OSError in case of a one line file 
                    f.seek(-2, os.SEEK_END)
                    while f.read(1) != b'\n':
                        f.seek(-2, os.SEEK_CUR)
                except OSError:
                    f.seek(0)
                last_line = f.readline().decode()

        if last_line == "==================================================================================":
            with open(filename, 'a') as output_file:
                output_file.write("\n")
                output_file.write("Bitcoin Private Key (WIF)  : " + WIF_Key_Output.decode() + "\n")
                output_file.write("Bitcoin Public Key (P2PKH) : " + Public_Key_Output.decode() + "\n")
        else:
            with open(filename, 'a') as output_file:
                output_file.write("==================================================================================\n")
                output_file.write("Bitcoin Private Key (WIF)  : " + WIF_Key_Output.decode() + "\n")
                output_file.write("Bitcoin Public Key (P2PKH) : " + Public_Key_Output.decode() + "\n")

        if NewWallets == wallets-1:
            with open(filename, 'a') as output_file:
                output_file.write("==================================================================================")

def generate_priv_pub_nl(wallets,filetype,filename):
    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + "\n")
        output_file.write(Public_Key_Output.decode() + "\n")

def generate_priv_nl(wallets,filetype,filename):
    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + "\n")

def generate_pub_nl(wallets,filetype,filename):
    with open(filename, 'a') as output_file:
        output_file.write(Public_Key_Output.decode() + "\n")

def generate_priv_pub_csv(wallets,filetype,filename):
    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + ",")
        output_file.write(Public_Key_Output.decode() + ",")

def generate_priv_csv(wallets,filetype,filename):
    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + ",")

def generate_pub_csv(wallets,filetype,filename):
    with open(filename, 'a') as output_file:
        output_file.write(Public_Key_Output.decode() + ",")

if __name__ == "__main__":
    """ Main entry point of the program"""

    argcheck()