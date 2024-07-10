# For ChaCha20_Poly1305
# ===================================================================
#
# Copyright (c) 2018, Helder Eijs <helderijs@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ===================================================================
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

from base64 import b64encode
from base64 import b64decode

from json import dumps, loads

def fetchkey():
    return get_random_bytes(32)

def encrypt(data, key):
    header = b""
    
    cipher = ChaCha20_Poly1305.new(key=key)
    cipher.update(header)
    cipherdata, tag = cipher.encrypt_and_digest(data)

    j = {
        "nonce" : b64encode(cipher.nonce).decode("utf-8"),
        "header" : b64decode(header).decode("utf-8"),
        "cipherdata" : b64encode(cipherdata).decode("utf-8"),
        "tag" : b64encode(tag).decode("utf-8")
    }

    result = dumps(j)
    return result

def decrypt(data, key):
        data = loads(data)

        cipherdata = b64decode(data["cipherdata"])
        tag = b64decode(data["tag"])
        nonce = b64decode(data["nonce"])
        header = b64decode(data["header"])

        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        cipher.update(header)

        plain = cipher.decrypt_and_verify(cipherdata, tag)
        return plain