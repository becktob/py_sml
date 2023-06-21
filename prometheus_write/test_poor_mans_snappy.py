from unittest import TestCase

from poor_mans_snappy import protobuf_varint


class Test(TestCase):
    def test_prtobuf_varint_returns_bytes(self):
        self.assertIsInstance(protobuf_varint(3), bytes)

    def test_protobuf_varint_short(self):
        self.assertEquals(0b0011.to_bytes(1, 'little'), protobuf_varint(0b0011))

    def test_protobuf_varint_multi(self):
        self.assertEquals(0b000_0110_1000_0001.to_bytes(2, 'little'), protobuf_varint(0b11_0000_0001))

    def test_protbuf_varint_multi_from_spec(self):
        # https://protobuf.dev/programming-guides/encoding/#varints
        self.assertEquals(b'\x96\x01', protobuf_varint(150))
