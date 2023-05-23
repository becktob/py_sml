import logging

from SML_binary import parse_binary_SML_message_from_stream
from SML_message import SmlMessage
from others_data import data_schatenseite, data_weigert

if __name__ == '__main__':
    # for data in (data0, data1, data2):
    #    print(parse_SML(data))
    # logging.basicConfig(level=logging.INFO)
    logging.info("Starting...")

    print("schatenseite:")
    for message_tokens in parse_binary_SML_message_from_stream(data_schatenseite):
        print(message_tokens)
        print(SmlMessage.parse_from_tokens(message_tokens).message_body)
        print("---")
        logging.info("---")

    print("weigert:")
    for message_tokens in parse_binary_SML_message_from_stream(data_weigert):
        print(message_tokens)
        print(SmlMessage.parse_from_tokens(message_tokens).message_body)
        print("---")
        logging.info("---")

    print("my data:")
    import my_data  # not in repo, in case it contains private info?

    for message_tokens in parse_binary_SML_message_from_stream(my_data.data0):
        print(message_tokens)
        message = SmlMessage.parse_from_tokens(message_tokens)
        if message:
            print(message.message_body)

        print("---")
        logging.info("---")
