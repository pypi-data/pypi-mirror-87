# ============================================================================
# This file is part of Pwman3.
#
# Pwman3 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2
# as published by the Free Software Foundation;
#
# Pwman3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pwman3; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ============================================================================
# Copyright (C) 2012 Oz N Tiram <oz.tiram@gmail.com>
# ============================================================================

import base64
import binascii
import ctypes
import datetime
import os
import random
import string
import sys
import time

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from pwman.util.callback import Callback


def encode_AES(cipher, clear_text):
    if not isinstance(clear_text, bytes):
        clear_text = clear_text.encode()
    return base64.b64encode(cipher.encrypt(clear_text))


def decode_AES(cipher, encoded_text):
    if not isinstance(encoded_text, bytes):
        encoded_text = encoded_text.encode()

    encoded_text = base64.b64decode(encoded_text)
    return cipher.decrypt(encoded_text).rstrip()


def generate_password(pass_len=8, uppercase=True, lowercase=True, digits=True,
                      special_chars=True):
    allowed = ''
    if lowercase:
        allowed = allowed + string.ascii_lowercase
    if uppercase:
        allowed = allowed + string.ascii_uppercase
    if digits:
        allowed = allowed + string.digits
    if special_chars:
        allowed = allowed + string.punctuation

    password = ''.join(random.SystemRandom().choice(allowed)
                       for _ in range(pass_len))
    return password


def zerome(string):
    """
    securely erase strings ...
    for windows: ctypes.cdll.msvcrt.memset
    """
    bufsize = len(string) + 1
    offset = sys.getsizeof(string) - bufsize
    ctypes.memset(id(string) + offset, 0, bufsize)


class CryptoException(Exception):
    pass


def get_digest(password, salt):
    """
    Get a digest based on clear text password
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=5000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def get_cipher(password, salt):
    """
    Create a chiper object from a hashed password
    """
    dig = get_digest(password, salt)
    return Fernet(dig)


def prepare_data(text, block_size):
    """
    prepare data before encryption so the lenght matches the expected
    lenght by the algorithm.
    """
    num_blocks = len(text)//block_size + 1
    newdatasize = block_size*num_blocks
    return text.ljust(newdatasize)


class CryptoEngine(object):
    _instance = None
    _callback = None

    @classmethod
    def get(cls, timeout=-1):
        if CryptoEngine._instance:
            return CryptoEngine._instance

        CryptoEngine._instance = CryptoEngine(timeout=timeout)
        return CryptoEngine._instance

    def __init__(self, salt=None, digest=None, algorithm='AES',
                 timeout=-1, reader=None):
        """
        Initialise the Cryptographic Engine
        """
        self._algo = algorithm
        self._digest = digest if digest else None
        self._salt = salt if salt else None
        self._timeout = timeout
        self._expires_at = -1
        self._cipher = None
        self._reader = reader
        self._callback = None
        self._getsecret = None  # This is set in callback.setter

    def authenticate(self, password):
        """
        salt and digest are stored in a file or a database
        """
        dig = get_digest(password, self._salt)
        if binascii.hexlify(dig) == self._digest or dig == self._digest:
            self._cipher = get_cipher(password, self._salt)
            if self._timeout > 0:
                self._expires_at = int(time.time()) + self._timeout
            return True
        return False

    def _auth(self):
        """
        Read password from the user, if the password is correct,
        finish the execution an return the password and salt which
        are read from the file.
        """
        salt = self._salt
        tries = 0
        while tries < 5:
            passwd = self._getsecret("Please type in your master password")
            if not isinstance(passwd, bytes):
                passwd = passwd.encode()
            if self.authenticate(passwd):
                return passwd, salt

            print("You entered a wrong password...")
            tries += 1
        raise CryptoException("You entered wrong password 5 times..")

    def encrypt(self, text):
        if not self._is_authenticated():
            p, s = self._auth()
            cipher = get_cipher(p, s)
            self._cipher = cipher
            del(p)

        return encode_AES(self._cipher, text)

    def decrypt(self, cipher_text):
        if not self._is_authenticated():
            p, s = self._auth()
            cipher = get_cipher(p, s)
            self._cipher = cipher
            del(p)

        return decode_AES(self._cipher, cipher_text)

    def forget(self):
        """
        discard cipher
        """
        self._cipher = None
        self._expires_at = -1

    def _is_authenticated(self):
        if self._is_timedout():
            return False
        if not self._digest and not self._salt:
            self._create_password()
        if self._cipher is not None:
            return True
        return False

    def _is_timedout(self):
        if self._timeout < 0:
            return False
        now = int(time.time())
        if now > self._expires_at:
            self._cipher = None
            return True
        # reset the time
        self._expires_at = int(time.time()) + self._timeout
        return False

    def lock_info(self):
        if self._expires_at < 0:
            return datetime.MAXYEAR

        self._expires_at = int(time.time()) + self._timeout
        return datetime.datetime.fromtimestamp(self._expires_at)

    def changepassword(self, reader=input):
        if self._callback is None:
            raise CryptoException("No callback class has been specified")

        # if you change the password of the database you have to Change
        # all the cipher texts in the databse!!!
        self._keycrypted = self._create_password()
        self.set_salt_digest(self._keycrypted)
        return self._keycrypted

    @property
    def callback(self):
        """
        return call back function
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        if isinstance(callback, Callback):
            self._callback = callback
            self._getsecret = callback.getsecret
        else:
            raise Exception("callback must be an instance of Callback!")

    def _create_password(self):
        """
        Create a secret password as a hash and the salt used for this hash.
        Change reader to manipulate how input is given.
        """
        salt = base64.b64encode(os.urandom(32))
        passwd = self._getsecret("Please type in the master password")
        if not isinstance(passwd, bytes):
            passwd = passwd.encode()
        key = get_digest(passwd, salt)
        hpk = salt+'$6$'.encode('utf8')+binascii.hexlify(key)
        self._digest = key
        self._salt = salt
        self._cipher = get_cipher(passwd, salt)
        return hpk.decode('utf-8')

    def set_salt_digest(self, key):
        self._salt, self._digest = (i.encode('utf-8') for i in key.split('$6$'))  # noqa

    def get_salt_digest(self):
        return self._salt.decode() + u'$6$' + self._digest.decode()
