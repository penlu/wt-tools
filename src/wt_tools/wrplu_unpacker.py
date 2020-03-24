import os.path
import argparse
import struct
from formats.wrplu_parser2 import wrplu_file
from construct.lib import hexdump

user_ids = [
    1268615,
    89342533,
    79046826,
    29208131,
    79352157,
    85379334,
    6560125,
    32826394,
    1599435,
    58975523,
    27054480,
    39313408,
    2952024,
    1781463,
    37103716,
    40065379,
    40117111,
    32801487,
    82463262,
    20231797,
    46384206,
    47279441,
    49366077,
    39646155,
    44128513,
    54035997,
]

def print_user_chunks(parsed):
    user_bytes = [struct.pack("<I", i) for i in user_ids]
    yes_chunks = []
    for chunk in parsed.chunks:
        for b in user_bytes:
            off = chunk.data.find(b)
            if off != -1:
                yes_chunks += [(off, chunk)]
    for (off, chunk) in yes_chunks:
        print(off)
        print(hexdump(chunk.data, 32))

def print_lens(parsed):
    for chunk in parsed.chunks:
        print(chunk.chunk_size)

def print_first_byte(parsed):
    for i, chunk in enumerate(parsed.chunks[:1180]):
        if len(chunk.data) == 0:
            #print("ZERO")
            pass
        else:
            #print(chunk.data[0])
            if not (chunk.data[0] in [2, 3, 4, 10, 11, 12]):
                print(i)
                print(chunk.chunk_size)
                print(hexdump(chunk.data, 32))

def unpack(data, filename):
    parsed = wrplu_file.parse(data)
    #print("DONE")
    #print(len(parsed.chunks))
    return parsed

def main():
    parser = argparse.ArgumentParser(description="Unpacks wrplu")
    parser.add_argument('filename', help="unpack from")
    parse_result = parser.parse_args()

    filename = parse_result.filename
    if not filename.endswith(".wrplu"):
        print("wrong file extension")
        exit(1)

    with open(filename, 'rb') as f:
        data = f.read()

    parsed = unpack(data, filename)
    #find_users(parsed)
    #print_lens(parsed)
    print_first_byte(parsed)
    #print(parsed.chunks[1164].chunk_params)
    #print(hexdump(parsed.chunks[1164].data, 32))
    #for i in range(1165):
    #    if parsed.chunks[i].chunk_params.unknown:
    #        print(hexdump(parsed.chunks[i].data, 32))
    return parsed

if __name__ == '__main__':
    parsed = main()
