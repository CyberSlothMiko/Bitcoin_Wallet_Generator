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

    filename1 = None
    filename2 = None

    if filetype:
        match filetype:
            case "fancy_txt":
                filename1 = green + "Output saved to : " + magenta + "fancy_txt.txt"
            case "priv_pub_nl":
                filename1 = green + "Output saved to : " + magenta + "priv_pub_nl.txt"
            case "priv_nl":
                filename1 = green + "Output saved to : " + magenta + "priv_nl.txt"
            case "pub_nl":
                filename1 = green + "Output saved to : " + magenta + "pub_nl.txt"
            case "priv_pub_csv":
                filename1 = green + "Output saved to : " + magenta + "priv_pub_csv.csv"
            case "priv_csv":
                filename1 = green + "Output saved to : " + magenta + "priv_csv.csv"
            case "pub_csv":
                filename1 = green + "Output saved to : " + magenta + "pub_csv.csv"
            case "priv_pub_csv_seperate":
                filename1 = green + "Private Key output saved to : " + magenta + "priv_seperate.csv\n"
                filename2 = green + "Public  Key output saved to : " + magenta + "pub_seperate.csv"
            case "priv_pub_nl_seperate":
                filename1 = green + "Private Key output saved to : " + magenta + "priv_seperate.txt\n"
                filename2 = green + "Public  Key output saved to : " + magenta + "pub_seperate.txt"
            case _:
                print ("Impossible!")
    
    if filename1 and not filename2:
        print(filename1)
    if filename1 and filename2:
        print (filename1 + filename2)

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
    """ Handles output options for the Script """

    match filetype:
        case "fancy_txt":
            filename = "fancy_txt.txt"
            generate_fancy_txt(filename)
        case "priv_pub_nl":
            filename = "priv_pub_nl.txt"
            delimiter = ""
            generate_priv_and_pub_csv_or_nl(filename,delimiter)
        case "priv_pub_csv":
            filename = "priv_pub_csv.csv"
            delimiter = ","
            generate_priv_and_pub_csv_or_nl(filename,delimiter)
        case "priv_nl":
            filename = "priv_nl.txt"
            data = WIF_Key_Output.decode()
            delimiter = ""
            generate_priv_or_pub_csv_nl(filename,data,delimiter)
        case "pub_nl":
            filename = "pub_nl.txt"
            data = Public_Key_Output.decode()
            delimiter = ""
            generate_priv_or_pub_csv_nl(filename,data,delimiter)
        case "priv_csv":
            filename = "priv_csv.csv"
            data = WIF_Key_Output.decode()
            delimiter = ","
            generate_priv_or_pub_csv_nl(filename,data,delimiter)
        case "pub_csv":
            filename = "pub_csv.csv"
            data = Public_Key_Output.decode()
            delimiter = ","
            generate_priv_or_pub_csv_nl(filename,data,delimiter)
        case "priv_pub_csv_seperate":
            filename = "priv_seperate.csv"
            filename_pub = "pub_seperate.csv"
            delimiter = ","
            generate_priv_and_pub_csv_nl_seperate(filename,filename_pub,delimiter)
        case "priv_pub_nl_seperate":
            filename = "priv_seperate.txt"
            filename_pub = "pub_seperate.txt"
            delimiter = ""
            generate_priv_and_pub_csv_nl_seperate(filename,filename_pub,delimiter)
        case _:
            print ("==================================================================================")
            print (green + "Bitcoin Private Key (WIF)  : " + magenta + WIF_Key_Output.decode() + reset)
            print (green + "Bitcoin Public Key (P2PKH) : " + magenta + Public_Key_Output.decode() + reset)

def generate_fancy_txt(filename):
    """ Outputs in the "fancy_txt" format """

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

def generate_priv_and_pub_csv_or_nl(filename,delimiter):
    """ Outputs in the "generate_priv_pub_nl" format """

    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + delimiter + "\n")
        output_file.write(Public_Key_Output.decode() + delimiter + "\n")

def generate_priv_or_pub_csv_nl(filename,data,delimiter):
    """ Outputs in the "pub/priv_csv" format """

    with open(filename, 'a') as output_file:
        output_file.write(data + delimiter + "\n")

def generate_priv_and_pub_csv_nl_seperate(filename,filename_pub,delimiter):
    """ Outputs in the "priv_pub_seperate" format """

    with open(filename, 'a') as output_file:
        output_file.write(WIF_Key_Output.decode() + delimiter + "\n")
    with open(filename_pub, 'a') as output_file:
        output_file.write(Public_Key_Output.decode() + delimiter + "\n")

if __name__ == "__main__":
    """ Main entry point of the program"""

    argcheck()