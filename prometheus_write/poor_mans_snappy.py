def protobuf_varint(i: int) -> bytes:
    result = b''
    while i != 0:
        this_byte = i & 0b0111_1111
        i >>= 7
        if i != 0:
            # continuation byte
            this_byte += 0b1000_0000
        result += this_byte.to_bytes(1, 'little')

    return result


def poor_mans_snappy_compress(input_data: bytes):
    length_bytes = protobuf_varint(len(input_data))

    # literal: type 0 -> lower bits of next byte are zero.
    # max length for one literal block is 4 bytes
    max_length_literal_block = 2 ** (4 * 8) - 1
    assert len(input_data) < max_length_literal_block

    length_to_encode = len(input_data)-1
    if length_to_encode >> 6 == 0:
        # len fits into six bits
        header = (length_to_encode << 2).to_bytes(1, 'little')

    return length_bytes + header + input_data
