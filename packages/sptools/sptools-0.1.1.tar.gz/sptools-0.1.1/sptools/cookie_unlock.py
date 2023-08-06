import sqlite3
import urllib3
import os
import json
import ctypes
import ctypes.wintypes
import sys
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from pathlib import Path
import browsercookie
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DATA_BLOB(ctypes.Structure):
	_fields_ = [('cbData', ctypes.wintypes.DWORD),
                ('pbData', ctypes.POINTER(ctypes.c_char))]

def dpapi_decrypt(encrypted):
    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result


def aes_decrypt(encrypted_txt):
    with open(os.path.join(os.environ['LOCALAPPDATA'],
                           r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
        jsn = json.loads(str(f.readline()))
    encoded_key = jsn["os_crypt"]["encrypted_key"]
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = dpapi_decrypt(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = Cipher(
        algorithms.AES(key),
        None,
        backend=default_backend()
    )
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_txt[15:])

# def aes_decrypt(encrypted_txt):
#     with open(os.path.join(os.environ['LOCALAPPDATA'],
#                            r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
#         jsn = json.loads(str(f.readline()))
#     encoded_key = jsn["os_crypt"]["encrypted_key"]
#     encrypted_key = base64.b64decode(encoded_key.encode())
#     encrypted_key = encrypted_key[5:]
#     key = dpapi_decrypt(encrypted_key)
#     nonce = encrypted_txt
#     cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
#     cipher.mode = modes.GCM(nonce)
#     decryptor = cipher.decryptor()
#     return decryptor.update(encrypted_txt[15:])


def unix_decrypt(encrypted):
    if sys.platform.startswith('linux'):
        password = 'peanuts'
        iterations = 1
    else:
        raise NotImplementedError

    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2

    salt = 'saltysalt'
    iv = ' ' * 16
    length = 16
    key = PBKDF2(password, salt, length, iterations)
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    decrypted = cipher.decrypt(encrypted[3:])
    return decrypted[:-ord(decrypted[-1])]


def chrome_decrypt(encrypted_txt):
    if sys.platform == 'win32':
        try:
            if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                decrypted_txt = dpapi_decrypt(encrypted_txt)
                return decrypted_txt.decode()
            elif encrypted_txt[:3] == b'v10':
                decrypted_txt = aes_decrypt(encrypted_txt)
                return decrypted_txt[:-16].decode()
        except WindowsError:
            return None
    else:
        try:
            return unix_decrypt(encrypted_txt)
        except NotImplementedError:
            return None

class Container:
    def __init__(self, domain, path, value, name):
        self.domain = domain
        self.path = path
        self.value = value
        self.name = name


def get_cookies_from_chrome(filename=None):
    if not filename:
        cookie_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\Cookies')
        if not os.path.exists(cookie_path):
            raise ValueError('Chrome浏览器的cookie不在默认路径下，请手动设置cookie_path')
    else:
        cookie_path = Path(filename)
        if not os.path.exists(cookie_path):
            raise ValueError('输入的cookie_path不存在')
    sql = f'SELECT name,host_key,path,  encrypted_value as value FROM cookies'
    con = sqlite3.connect(cookie_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql)
    cookie = []
    cur.execute(sql)
    for row in cur:
       if row['value'] is not None:
        name = row['name']
        value = chrome_decrypt(row['value'])
        domain = row['host_key']
        path = row['path']
        container = Container(domain, path, value, name)
        cookie.append(container)
    cur.close()
    return cookie


def get_cookies_from_ChromeCore(filename=None):
    if not filename:
        cookie_path = os.path.join(os.environ['LOCALAPPDATA'], r'ChromeCore\User Data\Default\Cookies')
        if not os.path.exists(cookie_path):
            raise ValueError('Chrome浏览器的cookie不在默认路径下，请手动设置cookie_path')
    else:
        cookie_path = Path(filename)
        if not os.path.exists(filename):
            raise ValueError('输入的cookie_path不存在')
    cookie = browsercookie.Chrome([cookie_path]).load()
    return cookie


def get_cookies_from_Friefox(filename=None):
    if not filename:
        files = os.path.join(os.environ['APPDATA'], r'Mozilla\Firefox\Profiles')
        if not os.path.exists(files):
            raise ValueError('Friefox浏览器的Profiles不在默认路径下，请手动设置cookie_path')
        for file in os.listdir(files):
            file_name = os.path.join(files, file)
            if 'cookies.sqlite' in os.listdir(file_name):
                cookie_path = os.path.join(file_name, r'cookies.sqlite')
                break
        if 'cookie_path' not in dir():
            raise ValueError('在默认路径下无法找到Friefox的cookie,请手动设置cookie_path')
    else:
        cookie_path = Path(filename)
        if not os.path.exists(cookie_path):
            raise ValueError('输入的cookie_path不存在')
    cookie = browsercookie.Firefox([cookie_path]).load()
    return cookie

if __name__ == "__main__":

    # d = get_cookies_from_Friefox(filename=r"C:\Users\jwh\AppData\Roaming\Mozilla\Firefox\Profiles\8ksfov82.default-release\cookies.sqlite")
    # c = get_cookies_from_chrome(filename=r"C:\Users\jwh\AppData\Local\ChromeCore\User Data\Default\Cookies")
    # e = get_cookies_from_ChromeCore(filename=r"C:\Users\jwh\AppData\Local\ChromeCore\User Data\Default\Cookies")
    d = get_cookies_from_Friefox()
    c = get_cookies_from_chrome()
    e = get_cookies_from_ChromeCore()
    for coo in d:
        if coo.domain == '.iwencai.com':
            print(coo.value)
    for coo in c:
        if coo.domain == '.iwencai.com':
            print(coo.value)
    for coo in e:
        if coo.domain == '.iwencai.com':
            print(coo.value)
    a = 1