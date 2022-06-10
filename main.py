#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import exit
from re import search
from hashlib import md5
from os.path import isfile, getsize
from progress.bar import IncrementalBar

hash_chunk_size = 65536
hash_pattern = r"[a-zA-Z0-9]{32,}" # Паттерн поиска хэш-суммы


def read_hash_from_file(fn):
    with open(fn, "r") as f:
        fdata = f.read()
        found_hash = search(hash_pattern, fdata).group()
        if found_hash is not None:
            # print(" found_hash:", found_hash)
            return found_hash
        print(" ! Hash sum not found")
        return False


def generate_md5(fn):
    hash_md5 = md5()
    with open(fn, "rb") as f:
        bar = IncrementalBar(" Generating hash sum...", max=int(getsize(fn) / hash_chunk_size), suffix='%(percent)d%%')
        for chunk in iter(lambda: f.read(hash_chunk_size), b""):
            hash_md5.update(chunk)
            bar.next()
        bar.finish()
    return hash_md5.hexdigest()


def ask_input(message):
    result = input(message)
    if not isfile(result):
        ask_input(message)
    return result


def main():
    src_file = ask_input("\n Input file: ")
    hash_input = input(" Input hash sum (or file): ")
    if (hash_input != ""):
        src_file_result = generate_md5(src_file)
        hash_input_result = False
        if isfile(hash_input):
            if hash_input.endswith(".md5"):
                hash_input_result = read_hash_from_file(hash_input)
            else:
                hash_input_result = generate_md5(hash_input)
        else:
            if search(hash_pattern, hash_input).group() is not None:
                hash_input_result = hash_input
        print("\n Equals?:", (src_file_result == hash_input_result), "\n")
    main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
