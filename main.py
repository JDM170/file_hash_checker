#!/usr/bin/python3
# -*- coding: utf-8 -*-

hash_chunk_size = 65536

from sys import exit
from hashlib import md5
from os.path import getsize
from progress.bar import IncrementalBar


def check_hash_file(fn):
    try:
        with open(fn, "r") as f:
            fdata = f.read()
            fdata = fdata.split(" *")
            return fdata[0]
    except FileNotFoundError:
        return fn


def check_file_exists(fn):
    try:
        open(fn, "rb").close()
        return True
    except FileNotFoundError:
        print(" ! File not found")
        return False
    except:
        print(" ! Unknown error")
        return False


def generate_md5(fn):
    if check_file_exists(fn):
        hash_md5 = md5()
        with open(fn, "rb") as f:
            bar = IncrementalBar(" Comparing...", max=int(getsize(fn) / hash_chunk_size), suffix='%(percent)d%%')
            for chunk in iter(lambda: f.read(hash_chunk_size), b""):
                hash_md5.update(chunk)
                bar.next()
            bar.finish()
        return hash_md5.hexdigest()
    return False


def input_files():
    file1 = str(input("\n Input first file: "))
    file2 = str(input(" Input hash sum: "))
    if (file1 != "") and (file2 != ""):
        print("\n Equals?:", generate_md5(file1) == check_hash_file(file2), "\n")
    input_files()


if __name__ == '__main__':
    try:
        input_files()
    except KeyboardInterrupt:
        if input("\n Stop comparing? (y/n): ").lower() == "y":
            exit()
        input_files()
