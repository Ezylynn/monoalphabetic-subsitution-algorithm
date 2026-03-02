import random, math
import argparse 
import string


def load_ngram_file(fname) -> dict:
    list: dict[str,int] = {}
    with open(fname, "r") as file:
        for line in file:
            line = line.strip()
            if line and line != None:
                temp = line.split()
                list.update({temp[0] : int(temp[1])})
            else:
                continue
    return list 

ALPH = "abcdefghijklmnopqrstuvwxyz"
TRI = load_ngram_file("count_3l.txt")
BI  = load_ngram_file("count_2l.txt")


# generate a random alphabetical key as a string
def key_gen()->str:
    shuffled = list(ALPH)
    random.shuffle(shuffled)
    return ''.join(shuffled)

# swap the key with the position of the char in the key, return the new key after swap
def key_swap(key,a,b):
    return key.translate(str.maketrans(a+b, b+a))

# encode the input based on the key, return the decoded text 
def encode(plain:str, key:str) -> str:
    return plain.translate(str.maketrans(ALPH,key))

# decrypt the input based on key, retur