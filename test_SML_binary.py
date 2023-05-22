from unittest import TestCase

from SML_binary import TYPE_OCT_STRING, TYPE_LIST, TYPE_ESCAPE, parse_word, read_type_length


class Test(TestCase):
    def test_read_type_length__octet_5(self):
        schaten_line4 = b'\x05\x01\xD3\xD7\xBA'
        tl, type, length = read_type_length(schaten_line4.__iter__())

        self.assertEquals(type, TYPE_OCT_STRING)
        self.assertEquals(length, len(schaten_line4))

    def test_read_type_length__list_6(self):
        raw = b'\x76'
        tl, type, length = read_type_length(raw.__iter__())

        self.assertEquals(type, TYPE_LIST)
        self.assertEquals(length, 6)

    def test_read_type_length__multibyte_length(self):
        schaten_line86 = b'\x83\x02\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
        tl, type, length = read_type_length(schaten_line86.__iter__())

        self.assertEquals(type, TYPE_OCT_STRING)
        self.assertEquals(length, len(schaten_line86))
        self.assertEquals([0x83, 0x02], tl)

    def test_read_type_length__handle_escape(self):
        schaten_end = b'\x1b\x1b\x1b\x1b\x1a\x00\xf3\xc7'
        tl, type, length = read_type_length(schaten_end.__iter__())

        self.assertEquals(type, TYPE_ESCAPE)


class TestParseWord(TestCase):
    def test_parse_int8(self):
        self.assertEquals(-17, parse_word([0x52, 256 - 17]))

    def test_parse_int64(self):
        word = [0x59, 0x01, 0, 0, 0, 0, 0, 0, 0x03]
        self.assertEquals(2 ** 56 + 3, parse_word(word))

    def test_parse_unsigned8(self):
        self.assertEquals(234, parse_word([0x62, 234]))

    def test_parse_unsigned64(self):
        word = [0x69, 0x01, 0, 0, 0, 0, 0, 0, 0x07]
        self.assertEquals(2 ** 56 + 7, parse_word(word))
