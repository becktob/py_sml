import logging

from SML_binary import parse_binary_SML_message_from_stream
from others_data import data_schatenseite, data_weigert

if __name__ == '__main__':
    # for data in (data0, data1, data2):
    #    print(parse_SML(data))
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting...")

    print("schatenseite:")
    for message in parse_binary_SML_message_from_stream(data_schatenseite):
        print(message)
        print("---")
        logging.info("---")

    print("weigert:")
    for message in parse_binary_SML_message_from_stream(data_weigert):
        print(message)
        print("---")
        logging.info("---")

    print("my data:")
    import my_data  # not in repo, in case it contains private info?

    for message in parse_binary_SML_message_from_stream(my_data.data0):
        print(message)
        print("---")
        logging.info("---")
