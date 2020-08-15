import argparse
import sys
import hashlib
import time

parser = argparse.ArgumentParser()

def read_from_file(file):
    with open(file, encoding="ISO-8859-1") as f:
        return f.read().strip()

def exit_with_help():
    parser.print_help()
    sys.exit(0)

def hash_function(hash):
    if len(hash) == 32:
        print("MD5 hash")
        def make_md5(s, encoding='utf-8'):
            return hashlib.md5(s.encode(encoding)).hexdigest()
        return make_md5
    elif len(hash) == 40:
        print("SHA1 hash")
        def make_sha1(s, encoding='utf-8'):
            return hashlib.sha1(s.encode(encoding)).hexdigest()
        return make_sha1
    else:
        print("Could not identify hash")
        sys.exit(0)

parser.add_argument("-w", help="password file")
parser.add_argument("-v", help="verbose output (shows all invalid passwords)",
        action="store_true")
group = parser.add_mutually_exclusive_group()
group.add_argument("-F", help="file containing the hash to crack")
group.add_argument("-f", help="hash text to crack")
args = parser.parse_args()

verbose = args.v

wordlist = args.w

hash = args.f if args.f else read_from_file(args.F) if args.F else exit_with_help()

hash_func = hash_function(hash)

start_time = time.time()

with open(wordlist, encoding="ISO-8859-1") as w:
    for line in w:
        current_password = line.strip()
        if verbose:
            print("Trying {}...".format(current_password))
        if hash_func(current_password) == hash:
            print("Password is {}".format(current_password))
            print("Cracked in {} seconds".format(time.time() - start_time))
            sys.exit(0)

print("Unable to crack hash")
