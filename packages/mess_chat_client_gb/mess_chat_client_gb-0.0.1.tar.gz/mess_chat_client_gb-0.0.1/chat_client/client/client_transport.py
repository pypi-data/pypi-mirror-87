"""
The module contains a class and methods describing the network communication
between the client and the server.
"""

import binascii
import hashlib
import hmac
import os
import socket
import sys
import time
import logging
import json
import threading

from PyQt5.QtCore import pyqtSignal, QObject

BASEDIR = os.getcwd()
sys.path.append(BASEDIR)

from common.config import system, methods, codes
from common.utils import get_message, send_message
from common.log import client_log_config

socket_lock = threading.Lock()


class ClientTransport(threading.Thread, QObject):
    """
    A network transport between client and server.
    """

    new_message = pyqtSignal(str)
    connection_lost = pyqtSignal()

    def __init__(
            self, address=None, port=None, username=None, password=None, database=None, crypt=None
    ) -> None:
        threading.Thread.__init__(self)
        QObject.__init__(self)

        self._logger = logging.getLogger('client')

        self.database = database
        self.username = username
        self.password = password
        self.session_crypt = crypt
        self.address = address if address else system.IP_ADDR_SRV
        self.port = port if port else int(system.IP_PORT)

        self.status = "Yep, I am here!"

        self._transport = None
        self.connection_init()

        # Updating the tables of known users and contacts
        try:
            self.known_user_list_update()
            self.contacts_list_update()
        except OSError as err:
            if err.errno:
                self._logger.critical(f'Connection lost! Error: {err}')
                raise Exception(f'Connection lost! Error: {err}')
        except json.JSONDecodeError as err:
            self._logger.critical(f'Connection lost! Error: {err}')
            raise Exception(f'Connection lost! Error: {err}')

        # The flag - True if the transport is running.
        self.running = True

    def connection_init(self) -> None:
        """
        Creating a connection to the server and
         starting the client authentication procedure on the server.
        :return: None
        """
        self._transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        for i in range(5):
            self._logger.info(f'Connection attempt {i + 1}')
            try:
                self._transport.connect((self.address, self.port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)

        if not connected:
            self._logger.critical('Server unreachable!')
            raise Exception('Server unreachable!')

        self._logger.debug('Connection created')

        try:
            with socket_lock:
                request = self.create_authenticate_1_request()
                send_message(sock=self._transport, message=request)
                self._logger.info(f'Sent authenticate_1_request for {self.username}: {request}')
                response = get_message(self._transport)
                self._logger.info(f'Received response for authenticate_1_request: {response}')
                if response.get('response_code') == codes.c511_NETWORK_AUTHENTICATION_REQUIRED:
                    random_str = response.get('message')
                    request = self.create_authenticate_2_request(random_str=random_str)
                    send_message(
                        sock=self._transport,
                        message=request
                    )
                    self._logger.info(f'Sent authenticate_2_request for {self.username}: {request}')
                    response = get_message(self._transport)
                    self._logger.info(f'Received response for authenticate_2_request: {response}')
                    if response.get('response_code') == codes.c202_ACCEPTED:
                        self._logger.info('Server connection established.')
                        return

                self._logger.critical(f'Authentication error: {response.get("message")}')
                raise Exception(f'Authentication error: {response.get("message")}')

        except (OSError, json.JSONDecodeError) as err:
            self._logger.critical(f'Server connection lost! Error: {err}')
            raise Exception(f'Server connection lost! Error: {err}')

    def _make_password_hash(self) -> bytes:
        """
        Generate a hash of the client's password and
         return the byte representation of the hash
        :return: A byte representation of the hash
        """
        password_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        password_hash = hashlib.pbkdf2_hmac('sha512', password_bytes, salt, 10000)
        return binascii.hexlify(password_hash)

    def create_presence_request(self) -> dict:
        """
        Creation of presence messages for sending to the server.
         A presence message example:
         {
            "action": "presence",
            "time": <unix timestamp>,
            "type": "status",
            "user": {
                "username": "C0deMaver1ck",
                "status": "Yep, I am here!"
            }
         }

        :return: A request message to the server.
        """
        return {
            "action": methods.PRESENCE,
            "time": int(time.time()),
            "type": "status",
            "user": {
                "username": self.username,
                "status": self.status
            }
        }

    def create_authenticate_1_request(self) -> dict:
        """
        Creation of authenticate stage 1 messages for sending to the server.
         Message example:
         {
                "action": "authenticate_1",
                "time": <unix timestamp>,
                "username":  "C0deMaver1ck",
         }

        :return: A request message to the server.
        """

        return {
            "action": methods.AUTHENTICATE_1,
            "time": int(time.time()),
            "username": self.username,
        }

    def create_authenticate_2_request(self, random_str: str) -> dict:
        """
        Creation of authenticate stage 2 messages for sending to the server.
         Message example:
         {
                "action": "authenticate_2",
                "time": <unix timestamp>,
                "username":  "C0deMaver1ck",
                "message" <digest>
         }

        :return: A request message to the server.
        """
        random_bytes_str = random_str.encode('utf-8')
        passwd_hash_string = self._make_password_hash()
        hash_ = hmac.new(passwd_hash_string, random_bytes_str, 'MD5')
        digest = hash_.digest()
        session_key = (digest * 2)
        self.session_crypt = self.session_crypt(key_string=session_key)

        return {
            "action": methods.AUTHENTICATE_2,
            "time": int(time.time()),
            "username": self.username,
            "message": binascii.b2a_base64(digest).decode('ascii')
        }

    @staticmethod
    def _check_response_fields(message: dict, fields: tuple) -> bool:
        """
        Checking for required fields in a message

        :param message: A message from the server.
        :param fields: A tuple of required fields
        :return: True if all of the fields are exists, else False.
        """
        for field in fields:
            if field not in message.keys():
                return False
        return True

    def process_server_ans(self, response) -> None:
        """
        Determining the type of response received from the server.
         If this is a message - use an incoming message processing way.
        :param response: A message from the server.
        :return: None
        """
        self._logger.debug(f'Received response: {response}')

        if self._check_response_fields(response, ("time",)):
            if response.get("action") == methods.MSG:
                if self._check_response_fields(response, ("to", "from", "message")):
                    if response.get("to") == self.username:

                        # Message decrypting
                        message = response.get("message")
                        d_message = self.session_crypt.decrypt(message)

                        self.database.save_message_history(
                            contact=response.get("from"),
                            direction='in',
                            message=d_message
                        )
                        self.new_message.emit(response.get("from"))

        else:
            raise Exception('Wrong message fields!')

    def contacts_list_update(self) -> None:
        """
        Update contact list from the server.

        :return: None
        """
        self._logger.debug(f'Getting contact list to {self.username}')
        req = {
            "action": methods.GET_CONTACTS,
            "time": int(time.time()),
            "username": self.username,
        }
        self._logger.debug(f'Request prepared {req}')
        with socket_lock:
            send_message(self._transport, req)
            ans = get_message(self._transport)

        self._logger.debug(f'Answer {ans}')

        if ans.get("response_code") == 202:
            for contact in ans.get("message"):
                self.database.add_contact(contact=contact)
        else:
            self._logger.error('Impossible to get contact list.')

    def known_user_list_update(self) -> None:
        """
        Update known user list from the server.

        :return: None
        """
        self._logger.debug(f'Getting known user list to {self.username}')
        req = {
            "action": methods.GET_KNOWN_USERS,
            "time": int(time.time()),
            "username": self.username,
        }

        self._logger.debug(f'Request prepared {req}')
        with socket_lock:
            send_message(sock=self._transport, message=req)
            ans = get_message(sock=self._transport)

        self._logger.debug(f'Answer {ans}')

        if ans.get("response_code") == 202:
            self.database.add_known_users(ans.get("message"))
        else:
            self._logger.error('Impossible to get known user list.')

    def add_contact(self, contact: str) -> None:
        """
        Creating a request for adding a contact, send this request to the server
         and parse the server's response.
        :param contact: A contact username.
        :return: None
        """
        self._logger.debug(f'Adding contact {contact}')
        req = {
            "action": methods.ADD_CONTACT,
            "time": int(time.time()),
            "username": self.username,
            "contact": contact
        }
        with socket_lock:
            send_message(self._transport, req)
            self.process_server_ans(get_message(self._transport))

    def remove_contact(self, contact: str) -> None:
        """
        Creating a request for delete a contact, send this request to the server
         and parse the server's response.
        :param contact: A contact username.
        :return: None
        """
        self._logger.debug(f'Deleting contact {contact}')
        req = {
            "action": methods.DEL_CONTACT,
            "time": int(time.time()),
            "username": self.username,
            "contact": contact
        }
        with socket_lock:
            send_message(self._transport, req)

            self.process_server_ans(get_message(self._transport))

    def transport_shutdown(self) -> None:
        """
        Close the network connection to the server.

        :return: None
        """
        self.running = False
        message = {
            "action": methods.QUIT,
            "time": int(time.time()),
            "username": self.username,
        }
        with socket_lock:
            try:
                send_message(self._transport, message)
            except OSError:
                pass
        self._logger.debug('Transport closing.')
        time.sleep(0.5)

    def send_message(self, to: str, message) -> None:
        """
        Send text message to remote recipient via the server.

        :param to: А username of massage far end recipient.
        :param message: A message body
        :return: None
        """

        # Encrypting messages
        e_message = self.session_crypt.encrypt(message)

        message_dict = {
            "action": methods.MSG,
            "time": int(time.time()),
            "to": to,
            "from": self.username,
            "encoding": system.ENCODING,
            "message": e_message
        }
        self._logger.debug(f'Made message: {message_dict}')

        # You must wait until the socket is released to send a message
        with socket_lock:
            send_message(self._transport, message_dict)
            self.process_server_ans(get_message(self._transport))
            self._logger.info(f'Message sent to {to}')

    def run(self) -> None:
        """
        The main loop of working with the network.

        :return: None
        """
        self._logger.debug('Transport run.')
        while self.running:
            time.sleep(1)
            with socket_lock:
                try:
                    self._transport.settimeout(0.5)
                    message = get_message(self._transport)

                except OSError as err:
                    if err.errno:
                        self._logger.critical(f'Connection lost!')
                        self.running = False
                        self.connection_lost.emit()

                # Problems with connection
                except (
                        ConnectionError, ConnectionAbortedError,
                        ConnectionResetError, json.JSONDecodeError, TypeError
                ):
                    self._logger.debug(f'Connection lost!.')
                    self.running = False
                    self.connection_lost.emit()

                # If the message is received, then we call the handler function.
                else:
                    self._logger.debug(f'Got message: {message}')
                    self.process_server_ans(message)

                finally:
                    self._transport.settimeout(5)
