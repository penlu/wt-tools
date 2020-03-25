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

chunk2 = Struct(
    #"chunk_start" / Probe(),
    # if true, then: length field is 1 byte and unknown should be False
    "header" / BitStruct(
        "onebyte" / Flag,
        "twobyte" / Flag,
        "threebyte" / If(lambda ctx: not (ctx.onebyte or ctx.twobyte), Flag),
        "length" / IfThenElse(
            this.onebyte,
            BitsInteger(6),
            IfThenElse(
                this.twobyte,
                BitsInteger(14),
                BitsInteger(21),
            ),
        ),
    ),
    "length" / Computed(this.header.length),
    "data" / Bytes(this.length),
    #Probe(this.length, show_stream=False),
)

wrplu_file2 = Struct(
    "chunks" / GreedyRange(chunk2),
)
