import logging
import warnings
from typing import List, Union, Iterator

TYPE_OCT_STRING = 0b0000
TYPE_BOOL = 0b0100
TYPE_INT = 0b0101
TYPE_UINT = 0b0110
TYPE_LIST = 0b0111
TYPE_ESCAPE = 0b0001
TYPE_PADDING = 0


def parse_word(word: List[int]) -> Union[str, int]:
    tl = word[0]

    if tl == 0:
        logging.info("End of SML message")
        return "End of SML message."  # confusing: not the same as "End of transport message" 1b1b1b1b_1a??????

    type = (tl & 0b0111_0000) >> 4
    length = tl & 0b0000_1111

    # see (130), Tab.4:
    if type == TYPE_OCT_STRING:
        return parse_octet_string(length, word)
    if type == TYPE_BOOL:
        return parse_bool(word)
    if type == TYPE_INT:
        return parse_int(word)
    if type == TYPE_UINT:
        return parse_unsigned(word)
    if type == TYPE_LIST:
        return parse_list(length)

    if type == TYPE_PADDING:
        raise NotImplementedError("This is probably a padding byte - not handled yet.")

    warnings.warn(f"Unexpected {type=}")
    logging.error(f"Unexpected {type=}")
    return f'{hex_string(word)}: UNKNOWN TYPE'


def parse_octet_string(length, word):
    value_bytes = word[-length:]
    return "".join([chr(b) for b in value_bytes])


def parse_bool(word):
    logging.warning(f"Bool not implemented: {word}")
    return word[0]


def parse_int(word):
    # 6.2.2 (136)
    value_bytes = bytes(word[1:])
    value = int.from_bytes(value_bytes, byteorder='big', signed=True)
    return value


def parse_unsigned(word):
    # 6.2.2 (136)
    value_bytes = bytes(word[1:])
    value = int.from_bytes(value_bytes, byteorder='big', signed=False)
    return value


def parse_list(length):
    return f"List: {length=}"


def unpack_binary_SML_message(message: Iterator[int]):
    """
    Parse a single SML message from input that starts at the beginning of an SML message
    """

    while True:
        tl, type, length = read_type_length(message)

        if type == TYPE_ESCAPE:
            if length[0] == 0x1a:
                logging.info(
                    "End of Message (transport level)")  # confusing: not the same as "End of SML message" (tl=0x00)
                break

        if type == TYPE_LIST:
            logging.info(f"{tl}: Enter list len={length=}")
            nested_iter = unpack_binary_SML_message(message)  # advances same iterator
            list_content = [next(nested_iter) for _ in range(length)]
            logging.info(f"End of list len={length=}, {list_content=}")
            yield list_content
        else:
            current_word = tl + [next(message) for _ in range(length - len(tl))]
            logging.debug(f"current_word: {hex_string(current_word)}")
            yield parse_word(current_word)


def read_type_length(message):
    this_byte = next(message)
    type = (this_byte & 0b0111_0000) >> 4  # type is always in first byte
    length = this_byte & 0b0000_1111
    tl = [this_byte]

    if type == TYPE_ESCAPE:  # TODO: move this outward, intercept at same level as "beginng of message"
        rest_of_special_property = [next(message) for _ in range(3)]
        special_property = tl + rest_of_special_property
        if all(b == 0x1b for b in special_property):
            logging.debug("Escape sequence for special property detected")
            special_content = [next(message) for _ in range(4)]
            return special_property, TYPE_ESCAPE, special_content  # TODO misusing "length" return value for content
        else:
            raise RuntimeError(f"Invalid/Incomplete escape sequence {special_property}")

    if this_byte & 0b1000_0000:
        # cf TR03109, (131)
        this_byte = next(message)
        tl.append(this_byte)
        length_bits_in_this_byte = this_byte & 0b0111_1111
        length = (length << 4) + length_bits_in_this_byte  # TODO: shift by 7 for following bytes? Or 4 for all bytes?
        if this_byte & 0b1000_0000:
            raise NotImplementedError("TODO: handle multi-byte TLs > 2")

    return tl, type, length


def hex_string(current_word):
    return ' '.join(f'{b:02x}' for b in current_word)


def parse_binary_SML_message_from_stream(data: bytes):
    """
    Handles section 6 of TR-03109-Anlage-IV, parsing binary type-length-value format to tokens.
    * "Octet String" -> python str
    * "Boolean" -> TODO
    * "Integer", "Unsigned" -> python int
    * "List of..." -> python [ ]
    """

    ESCAPE = b'\x1b' * 4
    BEGINN_EINER_NACHRICHT = b'\x01' * 4

    start = data.find(ESCAPE) + 4  # todo: handle ESCAPE_ESCAPE, which encodes ESCAPE (p68.155.1)

    escaped_property = data[start:start + 4]
    logging.info(f"{escaped_property=}")

    if escaped_property == BEGINN_EINER_NACHRICHT:
        # length = data[start + 4:].find(ESCAPE + b'\1a')

        message = data[start + 4:]

        words = unpack_binary_SML_message(bytearray(message).__iter__())

        return words

    remaining_data = data[start + 4:]
    if remaining_data:
        return parse_binary_SML_message_from_stream(remaining_data)
