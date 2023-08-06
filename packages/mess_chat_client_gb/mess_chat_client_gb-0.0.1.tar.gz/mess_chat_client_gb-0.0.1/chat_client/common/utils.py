"""
A module of Chat utilities.
"""

import dis
import json

from .config import system


def get_message(sock) -> dict:
    """
    Getting a message from a client

    :param sock: A socket
    :return: Decoded message
    """
    data = sock.recv(system.MAX_PACKAGE_LENGTH)
    # print(f'get_message -> :{data} ')
    if isinstance(data, bytes):
        data = data.decode(system.ENCODING)
        data = json.loads(data)
        return data
    raise ValueError


def send_message(sock, message: dict) -> None:
    """
    Sending a message to a socket

    :param sock: A socket
    :param message: A message in dict format
    :return: None
    """

    js_message = json.dumps(message, ensure_ascii=False)
    encoded_message = js_message.encode(system.ENCODING)
    sock.send(encoded_message)


class ValidPort:
    """
    A descriptor which checks TCP port
    """

    def __get__(self, instance, owner):
        return instance.__dict__[self.my_attr]

    def __set__(self, instance, value):
        if 1024 < value < 65535:
            instance.__dict__[self.my_attr] = value
        else:
            raise ValueError(
                f'The port number must be int, between 1024 and 65535. Your port: {value}'
            )

    def __set_name__(self, owner, my_attr):
        self.my_attr = my_attr


class ServerChecker(type):
    """
    A metaclass which check of Servers's' class
    """

    ignored_methods = ['__module__', '__qualname__', '__doc__']
    server_specific_commands = ['socket', 'select']
    client_specific_commands = ['connect']
    use_TCP = False

    def __init__(self, clsname, bases, clsdict):
        methods = []
        for method in clsdict:
            if method in self.ignored_methods:
                continue
            try:
                instructions = dis.get_instructions(clsdict[method])
                for i in instructions:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    if i.opname == 'LOAD_ATTR':
                        if i.argval == 'AF_INET':
                            self.use_TCP = True
            except TypeError:
                pass

        counter = 0
        for method in methods:
            if method in self.client_specific_commands:
                raise TypeError('В классе обнаружено использование запрещённого метода')
            elif method in self.server_specific_commands:
                counter += 1

        if counter < len(self.server_specific_commands):
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')

        if not self.use_TCP:
            raise TypeError('Не используется соке для работы по TCP.')

        super().__init__(clsname, bases, clsdict)


class ClientChecker(type):
    """
    A metaclass which check of Client's' class
    """

    ignored_methods = ['__module__', '__qualname__', '__doc__']
    server_specific_commands = ['accept', 'listen']
    client_specific_commands = ['get_message', 'send_message']
    use_TCP = False

    def __init__(self, clsname, bases, clsdict):
        methods = []
        for method in clsdict:
            if method in self.ignored_methods:
                continue
            try:
                instructions = dis.get_instructions(clsdict[method])
                for i in instructions:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    if i.opname == 'LOAD_ATTR':
                        if i.argval == 'AF_INET':
                            self.use_TCP = True
            except TypeError:
                pass

        counter = 0
        for method in methods:
            if method in self.server_specific_commands:
                raise TypeError('В классе обнаружено использование запрещённого метода')
            elif method in self.client_specific_commands:
                counter += 1

        if counter < len(self.client_specific_commands):
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')

        if not self.use_TCP:
            raise TypeError('Не используется соке для работы по TCP.')

        super().__init__(clsname, bases, clsdict)
