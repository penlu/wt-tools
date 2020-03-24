from construct import *

chunk = Struct(
    #"chunk_start" / Probe(),
    "chunk_params" / BitStruct(
        "is_one_byte" / Flag, # is length field 1 or 2 bytes
        "unknown" / Flag,
        "chunk_size" / IfThenElse(
            this.is_one_byte,
            BitsInteger(6),
            BitsInteger(14)
        ),
    ),
    "chunk_size" / Computed(this.chunk_params.chunk_size),
    "data" / Bytes(this.chunk_size),
    #Probe(this.chunk_size, show_stream=False),
)

wrplu_file = Struct(
    "chunks" / GreedyRange(chunk),
)
