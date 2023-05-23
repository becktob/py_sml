import logging
from typing import List


class SmlMessage:

    def __int__(self):
        self.transaction_id = None
        self.group_no: int = None
        self.abort_on_error: int = None
        self.message_body: SmlMessageBody = None

    @staticmethod
    def parse_from_tokens(message_tokens: List):
        # TR-03109-Anlage-IV: 5. (22)
        if len(message_tokens) != 6:
            logging.warning(f"Cannot parse SmlMessage, expecting length 6 but got {len(message_tokens)}")
            return None

        msg = SmlMessage()
        msg.transaction_id = message_tokens[0]
        msg.group_no = message_tokens[1]
        msg.abort_on_error = message_tokens[2]
        msg.message_body = SmlMessageBody.parse_from_tokens(message_tokens[3])

        return msg


class SmlPublicCloseRes:
    pass


class SmlGetListRes:
    pass


class SmlOpenResponse:
    pass


class SmlMessageBody:
    # BSI TR-03109-Anlage IV, 5(C)
    body_types = {0x101: SmlOpenResponse,
                  0x201: SmlPublicCloseRes,
                  0x701: SmlGetListRes}

    def __int__(self):
        pass

    @classmethod
    def parse_from_tokens(cls, body_tokens: List):
        # TR-03109-Anlage-IV: 5. (C)
        if len(body_tokens) != 2:
            logging.warning(f"Cannot parse SmlMessageBody, expecting length 2 but got {len(body_tokens)}")
            return None

        type_code = body_tokens[0]

        if type_code not in cls.body_types.keys():
            logging.warning(f"Got unknown SmlMessageBody type 0x{type_code:02x} (see BSI TR-03109-Anlage IV, 5(C)")
            return None

        BodyType = cls.body_types.get(type_code)

        return BodyType()
