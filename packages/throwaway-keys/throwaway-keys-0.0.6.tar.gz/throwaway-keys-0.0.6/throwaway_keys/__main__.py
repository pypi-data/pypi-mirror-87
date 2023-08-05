# Modules
import random
import hashlib

import datetime
from sys import argv

try:
    from termcolor import colored
except ImportError:

    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "cyan": "\033[36m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "reset": "\033[0m"
    }

    def colored(text, color):
        return colors[color] + text + colors["reset"]

# Exceptions
class InvalidRounds(Exception):
    pass

class InvalidLength(Exception):
    pass

# Argument functions
def use(lib):

    if "--use-" + lib in argv:

        return True

    return False

def get_rounds():

    for arg in argv:

        if arg.startswith("--rounds="):

            rounds = arg.split("=", 1)[1]
            try:
            
                return int(rounds)

            except:
                
                raise InvalidRounds("'{}' was not recognized as a valid integer.".format(rounds))

    return 3

def get_length():

    for arg in argv:

        if arg.startswith("--length="):

            length = arg.split("=", 1)[1]
            try:
            
                return int(length)

            except:
                
                raise InvalidLength("'{}' was not recognized as a valid integer.".format(rounds))

    return 75

# Initialization
generator = hashlib.sha256
unsafe = [hashlib.md5, hashlib.sha1]

rounds = get_rounds()

# Generators
generators = {
    # taken from https://docs.python.org/3.9/library/hashlib.html
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
    "shake128": hashlib.shake_128,
    "shake256": hashlib.shake_256,
    "sha3-224": hashlib.sha3_224,
    "sha3-256": hashlib.sha3_256,
    "sha3-384": hashlib.sha3_384,
    "sha3-512": hashlib.sha3_512,
    "blake2b": hashlib.blake2b,
    "blake2s": hashlib.blake2s
}

# Help command
if "-h" in argv or "--help" in argv:

    print("The", colored("Throwaway Key", "yellow"), "Project")
    print("=========================")

    print()
    print("usage: python3 -m throwaway_keys [options]")
    print("available hashing algorithms:")

    print(" ", "".join(_ + ", " for _ in generators)[:-2])

    print()
    print("to use a custom generator: --use-<generator_name>")
    print("to setup custom rounds: --rounds=<integer>")
    print("to setup custom length: --length=<integer> (only applicable with some generators)")

    exit()

length = get_length()
generator = hashlib.sha512
for gen in generators:

    if use(gen):

        generator = generators[gen]

# Begin generation
def generate_base(generator):

    if generator in unsafe:

        print(colored("Warning: you are using an unsafe or crackable generator ({}); consider changing.".format(generator.__name__), "red"))
        print()

    num = str(random.randint(100 * 100 * 100, 999 * 100 * 100))
    hash = generator(num.encode("UTF-8"))

    try:
        return hash.hexdigest(length = length)
    except:
        if length != 75:
            print(colored("Notice: the generator you are using ({}) does not support custom length.".format(generator.__name__), "yellow"))
            print()

        return hash.hexdigest()

def make_hash(key, generator):

    try:
        return generator(key.encode("UTF-8")).hexdigest(length = length)
    except:
        return generator(key.encode("UTF-8")).hexdigest()

begin = datetime.datetime.now()

start = generate_base(generator)
key = start

for _ in range(1, rounds + 1):

    key = make_hash(key, generator)

finish = round((datetime.datetime.now() - begin).total_seconds(), 2)

print("End result: '{}'".format(key))
print("Finished in: {} seconds".format(finish))
print("Generator: {}".format(generator.__name__))
