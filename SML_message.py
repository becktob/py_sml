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
    @classmethod
    def parse_from_tokens(cls, body_tokens: List):
        pass


class SmlListEntry:
    # BSI TR-03109-Anlage IV, 5.1.15 (OO)

    # https://www.promotic.eu/en/pmdoc/Subsystems/Comm/PmDrivers/IEC62056_OBIS.htm
    obis_codes = {"16.7.0": "Sum active instantaneous power (A+ - A-) [kW]",
                  "36.7.0": "Sum active instantaneous power (A+ - A-) in phase L1 [kW]",
                  "56.7.0": "Sum active instantaneous power (A+ - A-) in phase L2 [kW]",
                  "76.7.0": "Sum active instantaneous power (A+ - A-) in phase L3 [kW]",
                  "31.7.0": "Instantaneous current (I) in phase L1 [A]",
                  "51.7.0": "Instantaneous current (I) in phase L2 [A]",
                  "71.7.0": "Instantaneous current (I) in phase L3 [A]",
                  "32.7.0": "Instantaneous voltage (U) in phase L1 [V]",
                  "52.7.0": "Instantaneous voltage (U) in phase L2 [V]",
                  "72.7.0": "Instantaneous voltage (U) in phase L3 [V]",
                  "14.7.0": "Frequency [Hz]"}

    def __init__(self):
        self.obj_name: str = None
        self.status = None  # type?
        self.val_time = None  # type?
        self.unit = None  # type?
        self.scaler: int = None  # type?
        self.value = None  # type?
        self.value_sigature = None  # type?

    @classmethod
    def parse_from_tokens(cls, entry_tokens: List):
        if len(entry_tokens) != 7:
            logging.warning(f"Cannot parse SmlListEntry, expecting length 7 but got {len(entry_tokens)}")
            return None

        entry = SmlListEntry()
        entry.obj_name, entry.status, entry.val_time, entry.unit, entry.scaler, entry.value, entry.value_sigature = entry_tokens

        entry.obj_name = [ord(c) for c in entry.obj_name]
        entry.obj_name = ".".join(map(str, entry.obj_name[3:6]))  # can't find this anywhere, but seems the way it is :/
        if entry.obj_name in cls.obis_codes.keys():
            entry.obj_name = cls.obis_codes.get(entry.obj_name)

        print(entry.__dict__)
        return entry


class SmlGetListRes:
    # BSI TR-03109-Anlage IV, 5.1.15 (MM)
    def __init__(self):
        self.client_id: str = None
        self.server_id: str = None
        self.list_name: str = None
        self.act_sensor_time = None  # type?
        self.val_list: List = None
        self.list_signature = None  # type?
        self.act_gateway_time = None  # type?

    @classmethod
    def parse_from_tokens(cls, body_tokens: List):
        if len(body_tokens) != 7:
            logging.warning(f"Cannot parse SmlGetListRes, expecting length 7 but got {len(body_tokens)}")
            return None

        res = SmlGetListRes()
        res.client_id = body_tokens[0]
        res.server_id = body_tokens[1]
        res.list_name = body_tokens[2]
        res.act_sensor_time = body_tokens[3]
        res.val_list = [SmlListEntry.parse_from_tokens(l) for l in body_tokens[4]]
        res.list_signature = body_tokens[5]
        res.act_gateway_time = body_tokens[6]
        return res


class SmlOpenResponse:
    @classmethod
    def parse_from_tokens(cls, body_tokens: List):
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

        return BodyType.parse_from_tokens(body_tokens[1])
