from typing import Iterator, List


# https://www.schatenseite.de/2016/05/30/smart-message-language-stromzahler-auslesen/comment-page-1/
data_schatenseite = b''\
b'\x1B\x1B\x1B\x1B\x01\x01\x01\x01\x76\x05\x01\xD3\xD7\xBA\x62\x00\x62\x00\x72\x63\x01\x01\x76\x01\x01\x05'\
b'\x00\x9B\xF2\x94\x0B\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x01\x01\x63\xB3\x78\x00\x76\x05\x01\xD3\xD7'\
b'\xBB\x62\x00\x62\x00\x72\x63\x07\x01\x77\x01\x0B\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x01\x00\x62'\
b'\x0A\xFF\xFF\x72\x62\x01\x65\x01\x8A\x4D\x15\x77\x77\x07\x81\x81\xC7\x82\x03\xFF\x01\x01\x01\x01\x04\x49'\
b'\x53\x4B\x01\x77\x07\x01\x00\x00\x00\x09\xFF\x01\x01\x01\x01\x0B\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07'\
b'\x01\x77\x07\x01\x00\x01\x08\x00\xFF\x65\x00\x00\x01\x82\x01\x62\x1E\x52\xFF\x59\x07\x07\x07\x07\x07\x07'\
b'\x07\x07\x01\x77\x07\x01\x00\x01\x08\x01\xFF\x01\x01\x62\x1E\x52\xFF\x59\x07\x07\x07\x07\x07\x07\x07\x07'\
b'\x01\x77\x07\x01\x00\x01\x08\x02\xFF\x01\x01\x62\x1E\x52\xFF\x59\x07\x07\x07\x07\x07\x07\x07\x07\x01\x77'\
b'\x07\x01\x00\x10\x07\x00\xFF\x01\x01\x62\x1B\x52\x00\x55\x07\x07\x07\x07\x01\x77\x07\x81\x81\xC7\x82\x05'\
b'\xFF\x01\x01\x01\x01\x83\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07'\
b'\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07'\
b'\x07\x07\x07\x01\x01\x01\x63\xC6\x12\x00\x76\x05\x01\xD3\xD7\xBC\x62\x00\x62\x00\x72\x63\x02\x01\x71\x01'\
b'\x63\xEE\x1A\x00\x1B\x1B\x1B\x1B\x1A\x00\xF3\xC7'

TYPE_LIST = 0b0111
TYPE_OCT_STRING = 0b0000
def parse_word(word: List[int]) -> str:
    tl = word[0]

    if tl == 0:
        return f"End of Message."

    type = (tl & 0b0111_0000) >> 4

    length = tl & 0b0000_1111


    if type == TYPE_LIST:
        return f"List: {length=}"

    if type == TYPE_OCT_STRING:
        return f"{hex_string(word)}: Oct_Str: {length=}, {len(word)}"

    return f'{hex_string(word)}: foo'


def unpack_SML_binary(message: Iterator[int]):
    # 6 SML binary encoding, direkt gepackte Kodierung (p41)

    while True:
        tl, type, length = read_type_length(message)

        if type == TYPE_LIST:
            print(f"{tl:02x}: Enter List len={length=}")
            nested_iter = unpack_SML_binary(message)  # advances same iterator
            yield [next(nested_iter) for _ in range(length)]
            continue

        current_word = [tl] + [next(message) for _ in range(length-1)]
        print(f"current_word: {hex_string(current_word)}")
        yield parse_word(current_word)


def read_type_length(message):
    tl = next(message)
    multi_byte_length = tl & 0b1000_0000
    if multi_byte_length:
        raise NotImplementedError("TODO: handle multi-byte TLs")
    type = (tl & 0b0111_0000) >> 4
    length = tl & 0b0000_1111
    return tl, type, length


def hex_string(current_word):
    return ' '.join(f'{b:02x}' for b in current_word)


def parse_SML(data: bytes):
    ESCAPE = b'\x1b' * 4
    BEGINN_EINER_NACHRICHT = b'\x01' * 4

    start = data.find(ESCAPE) + 4  # todo: handle ESCAPE_ESCAPE, which encodes ESCAPE (p68.155.1)

    escaped_property = data[start:start + 4]
    print(f"{escaped_property=}")

    if escaped_property == BEGINN_EINER_NACHRICHT:
        # length = data[start + 4:].find(ESCAPE + b'\1a')

        message = data[start + 4:]

        words = unpack_SML_binary(bytearray(message).__iter__())

        return words

    remaining_data = data[start + 4:]
    if remaining_data:
        return parse_SML(remaining_data)


if __name__ == '__main__':
    #for data in (data0, data1, data2):
    #    print(parse_SML(data))

    for word in parse_SML(data_schatenseite):
        print(word)
