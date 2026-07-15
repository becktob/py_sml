# SML in pure python
* ...because there doesn't seem to be a fully featured lib out there?!
* ...because I like this level of data parsing.

## Spec:
Offical [BSI spec](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR03109/TR-03109-1_Anlage_Feinspezifikation_Drahtgebundene_LMN-Schnittstelle_Teilb.html)

[OBIS codes](https://www.promotic.eu/en/pmdoc/Subsystems/Comm/PmDrivers/IEC62056_OBIS.htm)

## Example datasets from others:
https://www.stefan-weigert.de/php_loader/sml.php
https://www.schatenseite.de/2016/05/30/smart-message-language-stromzahler-auslesen/comment-page-1/

## Hardware

So, I found this code - and the hardware. But the receiver was unplugged, with no documentation...

Un the head, I can take off the lid and find:
brown :VCC
white: GND
green: TX
yellow: RX

https://pinout.xyz/
04: 5V
06: GND
08: UART0 TX
10: UART0 RX

On a Pi Zero, need to enable serial port with `raspi-config` (not enabling shell on Serial, though)
