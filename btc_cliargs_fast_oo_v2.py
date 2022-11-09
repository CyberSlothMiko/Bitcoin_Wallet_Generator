#!/usr/bin/env python3

from secp256k1 import PrivateKey
import hashlib
import base58
import argparse
import os
import datetime


VersionByte = "00"
WIFByte = "80"
reset = "\u001b[0m"
green = "\u001b[32m"
magenta = "\u001b[35m"

SECP256K1_key_list = [[],[]]
Output_key_list =[[],[]]

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

    generate_wallet(filetype)

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
    wallet = 0

    while wallet < wallet_counter:
        NewKeyPair = PrivateKey()
        SECP256K1_key_list[0].append(NewKeyPair.serialize())
        SECP256K1_key_list[1].append((NewKeyPair.pubkey.serialize()))
        wallet += 1

def generate_publickey():
    """ Generates Public Key based on SECP256K1 Key-Pair """

    pubkey_counter = 0
    pubkey = ""

    while pubkey_counter < wallet_counter:

        pubkey = SECP256K1_key_list[1][pubkey_counter]
        
        pubkey_ripmd160hashed = hashlib.new('ripemd160',hashlib.sha256(pubkey).digest()).hexdigest()
        Public_Key_Output = base58.b58encode(bytes.fromhex(VersionByte + pubkey_ripmd160hashed + hashlib.sha256(hashlib.sha256(bytes.fromhex(VersionByte + pubkey_ripmd160hashed)).digest()).hexdigest()[0:8])).decode()    

        Output_key_list[1].append(Public_Key_Output)

        pubkey_counter += 1

def generate_privatekey():
    """ Generates Private Key based on SECP256K1 Key-Pair """

    privkey_counter = 0
    privkey = ""

    while privkey_counter < wallet_counter:

        privkey = SECP256K1_key_list[0][privkey_counter]

        WIF_Key_Output = base58.b58encode(bytes.fromhex(WIFByte + privkey + hashlib.sha256(hashlib.sha256(bytes.fromhex(WIFByte + privkey)).digest()).hexdigest()[0:8])).decode()
    
        Output_key_list[0].append(WIF_Key_Output)

        privkey_counter += 1
  
def generate_output(filetype):
    """ Handles output options for the Script """

    output_counter = 0

    match filetype:
        case "fancy_txt":
            filename = "fancy_txt.txt"
            generate_fancy_txt(filename)
        case "priv_pub_nl":
            generate_priv_and_pub_csv_or_nl("priv_pub_nl.txt","")
        case "priv_pub_csv":
            generate_priv_and_pub_csv_or_nl("priv_pub_csv.csv",",")
        case "priv_nl":
            generate_priv_or_pub_csv_nl("priv_nl.txt","",filetype)
        case "pub_nl":
            generate_priv_or_pub_csv_nl("pub_nl.txt","",filetype)
        case "priv_csv":
            generate_priv_or_pub_csv_nl("priv_csv.csv",",",filetype)
        case "pub_csv":
            generate_priv_or_pub_csv_nl("pub_csv.csv",",",filetype)
        case "priv_pub_csv_seperate":
            generate_priv_and_pub_csv_nl_seperate("priv_seperate.csv","pub_seperate.csv",",")
        case "priv_pub_nl_seperate":
            generate_priv_and_pub_csv_nl_seperate("priv_seperate.txt","pub_seperate.txt","")
        case _:
            while output_counter < wallet_counter:
                print ("==================================================================================")
                print (green + "Bitcoin Private Key (WIF)  : " + magenta + Output_key_list[0][output_counter] + reset)
                print (green + "Bitcoin Public Key (P2PKH) : " + magenta + Output_key_list[1][output_counter] + reset)
                output_counter += 1

def generate_fancy_txt(filename):
    """ Outputs in the "fancy_txt" format """

    last_line = ""
    output_counter = 0

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
            output_file.write("Bitcoin Private Key (WIF)  : " + Output_key_list[0][output_counter] + "\n")
            output_file.write("Bitcoin Public Key (P2PKH) : " + Output_key_list[1][output_counter]  + "\n")
            output_counter += 1
        with open(filename, 'a') as output_file:
            while output_counter < wallet_counter:
                output_file.write("==================================================================================\n")
                output_file.write("Bitcoin Private Key (WIF)  : " + Output_key_list[0][output_counter] + "\n")
                output_file.write("Bitcoin Public Key (P2PKH) : " + Output_key_list[1][output_counter]  + "\n")
                output_counter += 1
    else:
        with open(filename, 'a') as output_file:
                while output_counter < wallet_counter:
                    output_file.write("==================================================================================\n")
                    output_file.write("Bitcoin Private Key (WIF)  : " + Output_key_list[0][output_counter]  + "\n")
                    output_file.write("Bitcoin Public Key (P2PKH) : " + Output_key_list[1][output_counter]  + "\n")

                    output_counter += 1

    with open(filename, 'a') as output_file:
        output_file.write("==================================================================================")
            
def generate_priv_and_pub_csv_or_nl(filename,delimiter):
    """ Outputs in the "generate_priv_pub_nl" format """

    output_counter = 0

    with open(filename, 'a') as output_file:
        while output_counter < wallet_counter:
            output_file.write(Output_key_list[0][output_counter] + delimiter + "\n")
            output_file.write(Output_key_list[1][output_counter] + delimiter + "\n")
            output_counter += 1

def generate_priv_or_pub_csv_nl(filename,delimiter,filetype):
    """ Outputs in the "pub/priv_csv" format """

    output_counter = 0

    if filetype == "priv_nl" or filetype == "priv_csv":
        with open(filename, 'a') as output_file:
                while output_counter < wallet_counter:
                    output_file.write(Output_key_list[0][output_counter] + delimiter + "\n")
                    output_counter += 1
    if filetype == "pub_nl" or filetype == "pub_csv":
        with open(filename, 'a') as output_file:
                while output_counter < wallet_counter:
                    output_file.write(Output_key_list[1][output_counter] + delimiter + "\n")
                    output_counter += 1

def generate_priv_and_pub_csv_nl_seperate(filename,filename_pub,delimiter):
    """ Outputs in the "priv_pub_seperate" format """

    output_counter1 = 0
    output_counter2 = 0

    with open(filename, 'a') as output_file:
        while output_counter1 < wallet_counter:
            output_file.write(Output_key_list[0][output_counter1] + delimiter + "\n")
            output_counter1 += 1
    
    with open(filename_pub, 'a') as output_file:
        while output_counter2 < wallet_counter:
            output_file.write(Output_key_list[1][output_counter2] + delimiter + "\n")
            output_counter2 += 1

if __name__ == "__main__":
    """ Main entry point of the program"""
    start_time = datetime.datetime.now()
    argcheck()
    end_time = datetime.datetime.now()
    print(end_time - start_time)