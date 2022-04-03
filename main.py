#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import exit
from re import search
from hashlib import md5
from os.path import exists, getsize
from progress.bar import IncrementalBar

hash_chunk_size = 65536
hash_pattern = r"[a-zA-Z0-9]{32,}" # Паттерн поиска хэш-суммы


def check_hash_file(fn):
    if not exists(fn):
        if search(hash_pattern, fn).group() is not None:
            return fn
        print(" ! Hash sum not found")
        return False
    with open(fn, "r") as f:
        fdata = f.read()
        found_hash = search(hash_pattern, fdata).group()
        if found_hash is not None:
            # print(" found_hash:", found_hash)
            return found_hash
        print(" ! Hash sum not found")
        return False


def generate_md5(fn):
    if not exists(fn):
        print(" ! File not found")
        return False
    hash_md5 = md5()
    with open(fn, "rb") as f:
        bar = IncrementalBar(" Generating hash sum...", max=int(getsize(fn) / hash_chunk_size), suffix='%(percent)d%%')
        for chunk in iter(lambda: f.read(hash_chunk_size), b""):
            hash_md5.update(chunk)
            bar.next()
        bar.finish()
    return hash_md5.hexdigest()


def main():
    file1 = str(input("\n Input first file: "))
    file2 = str(input(" Input hash sum (or file): "))
    selected_mode = bool(int(input(" Select compare mode (0 or 1)\n 0 - hash sum; 1 - second file path: ")))
    # print(" selected_mode:", selected_mode)
    if (file1 != "") and (file2 != ""):
        if (selected_mode is False and exists(file2) and not file2.endswith(".txt")) or (selected_mode is True and not exists(file2)):
        # if (not exists(file2) and selected_mode is True):
            print(" ! Selected invalid mode")
            main()
        print("\n Equals?:", generate_md5(file1) == (check_hash_file(file2) if selected_mode is False else generate_md5(file2)), "\n")
    main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if input("\n Stop comparing? (y/n): ").lower() == "y":
            exit()
