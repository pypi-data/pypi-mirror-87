import http
import logging
import socket
from http import client

import wakeonlan

PORT = 49200
""" Port of the remote service. Actually the device and port could be resolved by a SSDP
but the port seems to be static nowadays."""

SERVICE_PATH = "services/rcr/control/RCRService"
SOAP_ACTION = "urn:metz.de:service:RCRService:1#SendKeyCode"

SEND_KEY_XML = """<?xml version="1.0" encoding="utf-8"?>
 <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
   <s:Body>
     <u:SendKeyCode xmlns:u="urn:metz.de:service:RCRService:1">
       <KeyCode>{}</KeyCode>
       <DestinationDevice>0</DestinationDevice>
       <ButtonHold>0</ButtonHold>
     </u:SendKeyCode>
   </s:Body>
 </s:Envelope>"""

KEY_CODE_POWER = 11
KEY_CODE_CH_UP = 46
KEY_CODE_CH_DOWN = 47
KEY_CODE_VOLUME_UP = 27
KEY_CODE_VOLUME_DOWN = 28
KEY_CODE_MUTE = 35
KEY_CODE_OK = 39


class TvRemoteCommandException(Exception):
    """TC remote command failed"""
    pass


class MetzRemote:
    """Remote access class for Metz television.
    """

    def __init__(self, ip, debug=False):
        """Constructor

        :param ip: The IP address of the television. The IP could be resolved by SSDP, but in case multiple
        televisions are in the network this would be not unique.
        """
        self.ip = ip
        if debug:
            # TODO
            pass

    @staticmethod
    def power_on(mac: str):
        """Powers one the television by a Wake-On-LAN packet using the MAC address.
        The must be enable in the TV settings.
        :param mac The MAC address
        :return: None
        """
        wakeonlan.send_magic_packet(mac)

    def __send__(self, key_code: int):
        xml = SEND_KEY_XML.format(key_code)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5000)
            s.connect((self.ip, PORT))
            command = 'POST /' + SERVICE_PATH + " HTTP/1.1" + '\r\n' \
                      + "Host: {}:{}".format(self.ip, PORT) + "\r\n" \
                      + "SOAPAction: \"{}\"".format(SOAP_ACTION) + "\r\n" \
                      + 'Content-Type: text/xml; charset="utf-8"' + "\r\n" \
                      + 'Content-Length: {}'.format(len(xml)) + "\r\n" \
                      + 'Connection: close' + "\r\n" \
                      + "\r\n" + xml
            s.sendall(command.encode())
            resp = s.recv(1024).decode("utf-8")
            if '200 OK' not in resp:
                raise TvRemoteCommandException()

    def volume_up(self):
        """Turns up the volume.

        :return: None
        """
        self.__send__(KEY_CODE_VOLUME_UP)

    def volume_down(self):
        """Turns down the volume.

        :return: None
        """
        self.__send__(KEY_CODE_VOLUME_DOWN)

    def mute(self):
        """Mute.

        :return: None
        """
        self.__send__(KEY_CODE_MUTE)

    def unmute(self):
        """Unmute.

        :return: None
        """
        self.__send__(KEY_CODE_MUTE)

    def ch_up(self):
        """Channel up.

        :return: None
        """
        self.__send__(KEY_CODE_CH_UP)

    def ch_down(self):
        """Channel down.

        :return: None
        """
        self.__send__(KEY_CODE_CH_DOWN)

    def power(self):
        """Power.

        :return: None
        """
        self.__send__(KEY_CODE_POWER)

    def ok(self):
        """Sends OK.

        :return: None
        """
        self.__send__(KEY_CODE_OK)

    def channel(self, channel: int):
        """Sends a channel number.

        :return: None
        """
        self.__send__(channel)

    def control(self, code: int):
        """Sends a generic code.

        :return: None
        """
        self.__send__(code)
