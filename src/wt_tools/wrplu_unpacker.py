import os.path
import argparse
import struct
from formats.wrplu_parser2 import wrplu_file, wrplu_file2
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

# show chunks in which any "user ID" in above list appears
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

# dump chunk length
# nearly all are quite short
def print_lens(parsed):
    for chunk in parsed.chunks:
        print(chunk.chunk_size)

# dump chunk firstbyte
# noted: 4 and 12 appear to be far and away the most common firstbyte of data
# other values might be assumed to be due to wrong parse
def print_first_byte(parsed):
    for i, chunk in enumerate(parsed.chunks):
        if len(chunk.data) == 0:
            print("ZERO")
        else:
            print(chunk.data[0])

# print unusual values of first byte
def print_odd_chunks(parsed):
    for i, chunk in enumerate(parsed.chunks):
        if not (chunk.data[0] in [0, 2, 3, 4, 10, 11, 12]):
            print(i)
            print(chunk.chunk_size)
            print(hexdump(chunk.data, 32))

# noted: nearly all onebytes have "False" in unknown
def print_onebyte_meta(parsed):
    for i, chunk in enumerate(parsed.chunks):
        if chunk.chunk_params.is_one_byte:
            print(chunk.chunk_params.unknown, chunk.chunk_size)

# noted: nearly all twobytes have "True" in unknown
# unusual ones include ones that are wrong
def print_notonebyte_meta(parsed):
    for i, chunk in enumerate(parsed.chunks):
        if not chunk.chunk_params.is_one_byte:
            print(chunk.chunk_params.unknown, chunk.chunk_size)

# so, print onebytes with "True", and print twobytes with "False"
# noted: all the nonstandard chunks are misparsed
def print_nonstandard(parsed):
    for i, chunk in enumerate(parsed.chunks):
        if not (chunk.chunk_params.is_one_byte ^ chunk.chunk_params.unknown):
            print(i)
            print(chunk.chunk_size)
            print(hexdump(chunk.data, 32))

# just to see which ones have "unknown" flag set
def print_unknown_chunks(parsed):
    print(parsed.chunks[1164].chunk_params)
    print(hexdump(parsed.chunks[1164].data, 32))
    for i in range(1165):
        if parsed.chunks[i].chunk_params.unknown:
            print(hexdump(parsed.chunks[i].data, 32))

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

    parsed = wrplu_file2.parse(data)

    print(parsed.chunks[1166].header)
    print(hexdump(parsed.chunks[1166].data, 32))

    #find_users(parsed)
    #print_lens(parsed)
    #print_first_byte(parsed)
    #print_onebyte_meta(parsed)
    #print_notonebyte_meta(parsed)
    #print_nonstandard(parsed)
    #print_unknown_chunks(parsed)

    return parsed

if __name__ == '__main__':
    parsed = main()
