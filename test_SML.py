from unittest import TestCase

from SML import read_type_length, TYPE_OCT_STRING, TYPE_LIST


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