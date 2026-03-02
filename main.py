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

# decrypt the input based on key, return the decoded text 
def decode(cipher:str,key:str) -> str:
    inv = str.maketrans(key, ALPH)  # cipher -> plain
    return cipher.lower().translate(inv)

def parse_txt(msg:str) -> str:
    parsed_msg = "".join([char for char in msg if char not in string.punctuation and char not in string.whitespace and char not in string.digits])
    return parsed_msg.lower()

# parsing text into n-grams, return a list of string
def ngram_parser(msg,n) -> list[str]:
    return [msg[i:i+n] for i in range(len(msg) - (n-1))]
    # len(msg) - (n-1)) - determines the valid starting index point 

# return score of decoded plaintext based on how many plaintext matches trigrams
def trigram_prob(msg) -> int:
    UNSEEN = -8.0 
    lower_formated_msg = msg.lower()
    parsed_msg_arr :list[str] = ngram_parser(lower_formated_msg,3)
    ngram_dict :dict[str,int] = TRI 

    score: int = 0
    for text in parsed_msg_arr:
        if text in ngram_dict:
            score += math.log10(ngram_dict[text])
        else:
            score -= UNSEEN #for ngram that is not inlcuded in the trigram list
    return score

# generator function that return a slightly different version of the original key, aim to swap out the least commons bigrams
def get_neighbour_key(msg,key):
    # set removes duplicate, the key have BI look up dictionary, return rare bigrams as small numbers or 0
    bigrams = sorted(set(ngram_parser(msg,2)), key=lambda bg: BI.get(bg, 0))[:30]


    # run for loop on bigrams i.e [X,Z] -> c1=X,c2=Z 
    for c1,c2 in bigrams:
        for a in random.choice(ALPH): #random shuffle alphabet to avoid bias
            if c1 == c2 and BI.get(a+a,0) > BI.get(c1+c2,0): #for case i.e EE and EE > XZ
                yield key_swap(key, a, c1)
            else:
                if BI.get(a+c2, 0) > BI.get(c1+c2, 0): #for case i.e IN > ZN
                    yield key_swap(key, a, c1)

                if BI.get(c1+a, 0) > BI.get(c1+c2, 0): #for case i.e ON > OJ
                    yield key_swap(key, a, c2)

    # after exhaust 30 least common bigrams, make random swaps in hope of any improvement
    while True:
        yield key_swap(key, random.choice(ALPH),random.choice(ALPH)) 
        

# generates neighbour that slightly deviate from original key, to look for improvement in score, return key once finished iterating the steps
def steepest_ascent(e_msg, key, steps):

    tmp_key = key
    val = trigram_prob(decode(e_msg,tmp_key))
    neighbors = get_neighbour_key(decode(e_msg,tmp_key), tmp_key)

    for i in range(steps):
        neighbor_key = next(neighbors) # the neighbour key
        neighbor_val = trigram_prob(decode(e_msg, neighbor_key))

        if neighbor_val > val:
            val = neighbor_val 
            tmp_key = neighbor_key 
            neighbors = get_neighbour_key(decode(e_msg,tmp_key), tmp_key)

    return tmp_key 



# return the best possible key, include restarts to improve algorithm decoding accuracy
def steepest_ascent_restarts(e_msg: str, steps: int, restarts: int = 50):
    best_key = None
    best_val = 0.0

    for r in range(restarts):
        start_key = key_gen()
        k = steepest_ascent(e_msg, start_key, steps)
        v = trigram_prob(decode(e_msg, k))

        if v > best_val:
            best_val = v
            best_key = k
            print(f"[restart {r+1}/{restarts}] new best score = {best_val:.2f}")

    return best_key, best_val

def check_key(key):
    bool_output = False
    done = []
    for char in key.lower():
      if char in ALPH and char not in done:
        done.append(char)
      else:
        return False
    if len(key) == 26:
        bool_output = True 
    return bool_output

def read_file(fname):
    raw_text = ""
    with open(fname, "r") as file:
        for line in file:
            if line and line != None:
                raw_text += line
            else:
                continue
    return raw_text 


def write_file(raw_txt, fname):
    with open(fname, "w") as file:
        file.write(raw_txt)

def file_exist(fname):
    try:
        with open(fname, "r", encoding="utf-8"):
            return True
    except OSError:
        return False

def option_a(filepath, key, o):
    plain_txt = read_file(filepath).lower() # make sure to make all lower
    cipher_txt = encode(plain_txt,key).upper()
    write_file(cipher_txt,o)
    print(f"Key: {key}")
    print("Successfully executed - exiting out")

def option_b(filepath, o):
    cipher_txt = read_file(filepath).lower() # make sure to make all lower
    parsed_cipher_text = parse_txt(cipher_txt)
    key, val = steepest_ascent_restarts(parsed_cipher_text, 2500, 80)
    plain_txt = decode(cipher_txt,key)
    write_file(plain_txt,o)

    print(f"Best key: {key} with best score: {val}")
    print("Successfully executed - exiting out")

def option_c(filepath, key, o):
    cipher_txt = read_file(filepath).lower() # make sure to make all lower
    plain_txt = decode(cipher_txt,key)
    write_file(plain_txt,o)
    print("Successfully executed - exiting out")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode/decodes plain text through monoalphabetic subsitution method")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encode",action="store_true", help="Encodes the message")
    group.add_argument("-d", "--decode",action="store_true", help="Decodes the message")

    parser.add_argument("-k", "--key", type=str, help="Key for the decryption/encryption")
    parser.add_argument("filepath", help="Filepath of input file")
    parser.add_argument("-o", help="Filepath of output file" ,required=True)

    args = parser.parse_args()

    # flag -e file.txt -o file2.txt
    if (args.encode and (args.key == None) and args.filepath and args.o):
        key = key_gen() # generate a random key for user
        if file_exist(args.filepath):
            option_a(args.filepath, key, args.o)
        else:
            print("File doesn't exist")


    # flag -e -k "AJKDSJKHBNCJK" file.txt -o file2.txt
    elif (args.encode and args.key and args.filepath and args.o):
        if (check_key(args.key)):
            if file_exist(args.filepath):
                option_a(args.filepath, args.key, args.o)
            else:
                print("File doesn't exist")
        else:
            print("Invalid key. Exiting out of program")

    # flag -d file.txt -o file2.txt
    elif (args.decode and (args.key == None) and args.filepath and args.o):
        if file_exist(args.filepath):
            option_b(args.filepath,args.o)
        else:
            print("File doesn't exist")


    # flag -d -k "AJKDSJKHBNCJK" file.txt -o file2.txt
    elif (args.decode and args.key and args.filepath and args.o):
        if (check_key(args.key)):
            if file_exist(args.filepath):
                option_c(args.filepath,args.key, args.o)
            else:
                print("File doesn't exist")
        else:
            print("Invalid key. Exiting out of program")