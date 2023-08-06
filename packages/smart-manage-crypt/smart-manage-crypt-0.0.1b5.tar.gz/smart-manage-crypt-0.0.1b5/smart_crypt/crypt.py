from .utils import random_salt
from typing import Callable
from hashlib import sha256
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from typing import Optional

__all__ = ('Crypt', 'encrypt', 'decrypt')


class Crypt(object):
    @property
    def default_salt(self) -> str:
        return 'SlTKeYOpHygTYkP3'

    @property
    def salt(self) -> str:
        return self.__salt

    def __init__(self, salt: Optional[str] = None):
        self.__salt = salt if salt else self.default_salt
        self.enc_dec_method = 'utf-8'

    def set_random_salt(self) -> str:
        self.__salt = random_salt()
        return self.__salt

    def set_default_salt(self) -> str:
        self.__salt = self.default_salt
        return self.__salt

    def _try_crypt(
        self, method: Callable[[str, str], str], string: str, key: str
    ) -> str:
        """Wrap encrypt/decrypt method in try except

            Args:
                method (function): method to wrap in try except
                string (str): string to encode or decode
                key (str): your key.

            Returns:
                str: encrypted or decrypted string
        """
        try:
            return method(string, key)
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Encryption Error: SALT must be 16 characters long')
            elif (
                value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long'
            ):
                raise ValueError(
                    'Encryption Error: Encryption key must be either 16, 24, or 32 characters long'
                )
            else:
                raise ValueError(value_error)

    def __get_aes_obj(self, key: str) -> AES.AESCipher:
        return AES.new(sha256(key.encode()).digest(), AES.MODE_CFB, self.__salt)

    def _encrypt(self, str_to_enc: str, secret: str) -> str:
        """Encrypt string

            Args:
                str_to_enc (str): default string
                secret (Optional[str], optional): secret token

            Returns:
                str: encrypted string
            """
        aes_obj = self.__get_aes_obj(secret)
        hx_enc = aes_obj.encrypt(str_to_enc)
        str_enc = b64encode(hx_enc).decode(self.enc_dec_method)
        return str_enc.replace('/', '-_-')

    def _decrypt(self, enc_str: str, secret: str) -> str:
        """Encrypt string

            Args:
                enc_str (str): default string
                secret (Optional[str], optional): secret token

            Returns:
                str: encrypted string
            """
        enc_str = enc_str.replace('-_-', '/')
        aes_obj = self.__get_aes_obj(secret)
        str_tmp = b64decode(enc_str.encode(self.enc_dec_method))
        str_dec = aes_obj.decrypt(str_tmp)
        return str_dec.decode(self.enc_dec_method)

    def encrypt(self, str_to_enc: str, str_key: str):
        """Call encrypt method wrapped by try except
        Args:
            str_to_enc (str): string to encrypt
            str_key (str): your key for encrypt

        Returns:
            str: encrypted string
        """
        return self._try_crypt(self._encrypt, str_to_enc, str_key)

    def decrypt(self, enc_str: str, str_key: str):
        """Call decrypt method wrapped by try except
        Args:
            enc_str (str): string to decrypt
            str_key (str): your key for decrypt

        Returns:
            str: decrypted string
        """
        return self._try_crypt(self._decrypt, enc_str, str_key)


def encrypt(str_to_encrypt: str, secret: str, salt: Optional[str] = None) -> str:
    """Encrypt string

    Args:
        str_to_encrypt (str): default string
        secret (Optional[str], optional): secret token
        salt (Optional[str], optional): your salt. Defaults to None.

    Returns:
        str: encrypted string
    """
    c = Crypt(salt)
    return c.encrypt(str_to_enc=str_to_encrypt, str_key=secret)


def decrypt(str_to_decrypt: str, secret: str, salt: Optional[str] = None) -> str:
    """Decrypt string

    Args:
        str_to_decrypt: encrypted string
        secret (Optional[str], optional): secret token
        salt (Optional[str], optional): your salt. Defaults to None.

    Returns:
        str: decrypted string
    """
    c = Crypt(salt)
    return c.decrypt(enc_str=str_to_decrypt, str_key=secret)
