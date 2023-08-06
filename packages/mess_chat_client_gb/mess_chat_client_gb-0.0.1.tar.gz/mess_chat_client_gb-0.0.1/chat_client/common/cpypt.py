"""
A module of encrypt and decrypt chat message.
"""

import binascii
import os
import sys

from Cryptodome.Cipher import AES

BASEDIR = os.path.split(os.getcwd())[0]
sys.path.append(BASEDIR)

from common.config import system


class ChatCrypting:
    """
    Encrypt and decrypt chat message class.
    """

    def __init__(self, key_string: bytes) -> None:
        self._key_string = key_string

    @staticmethod
    def _padding_text(text: bytes) -> bytes:
        """
        Filling the text up to length multiple of 16

        :param text: A bytestring of text
        :return: A padded bytestring
        """

        pad_len = (16 - len(text) % 16) % 16
        return text + b' ' * pad_len

    def encrypt(self, text: str) -> str:
        """
        Encrypting text

        :param text: The encrypted text to encryption
        :return: The encrypted text
        """
        padded_text = self._padding_text(text.encode(system.ENCODING))
        cipher = AES.new(self._key_string, AES.MODE_CBC)
        ciphertext = cipher.iv + cipher.encrypt(padded_text)
        return binascii.b2a_base64(ciphertext).decode('ascii')

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypting text

        :param ciphertext: An encrypted text
        :return: The clear text
        """
        ciphertext = binascii.a2b_base64(ciphertext)
        cipher = AES.new(self._key_string, AES.MODE_CBC, iv=ciphertext[:16])
        text = cipher.decrypt(ciphertext[16:])
        return text.decode(system.ENCODING).strip()


if __name__ == "__main__":
    plaintext = 'The rain in Spain'
    key = b'Super Secret Key'

    crypt = ChatCrypting(key_string=key)
    encrypted_text = crypt.encrypt(plaintext)
    print(encrypted_text)
    decrypted_text = crypt.decrypt(encrypted_text)
    print(decrypted_text)
    print(decrypted_text == plaintext.strip())
