from construct import *

chunk = Struct(
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

wrplu_file = Struct(
    "chunks" / GreedyRange(chunk2),
)
