__title__ = 'crypt2file'
__license__ = 'MIT'
__author__ = 'Kyunghoon (aloecandy@gmail.com)'
__version__ = '0.1.4'

from cryptography.fernet import Fernet
import os
from sys import platform
if "linux" in platform:
    key_path=os.path.join(os.environ['HOME'],".local/secret.key")
elif "darwin" in platform:
    key_path=".secret.key"
elif "win" in platform:
    key_path=os.path.join(os.environ['USERPROFILE'],"secret.key")
else:
    key_path=".secret.key"
f=None

def init():
    global f
    try:
        print('crypt2file: trying to get existing key...')
        key=open(key_path, "rb").read()
        print('crypt2file: success')
    except:
        print('crypt2file: failed')
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        print('crypt2file: created a new key')
    f = Fernet(key)

def encrypt(msg):
    return f.encrypt(msg.encode('utf-8'))
def decrypt(encrypted_msg):
    return f.decrypt(encrypted_msg).decode('utf-8')

def msgToEncryptedFile(msg,fileName):
    with open(fileName,'wb') as file:
        file.write(encrypt(msg))
    return msg
def encryptedFileToMsg(fileName):
    try:
        msg = decrypt(open(fileName,'rb').read())
    except:
        print('crypt2file: cannot open {}'.format(fileName))
        msg = msgToEncryptedFile(input('crypt2file: creating the file. type msg:'),fileName)
    return msg


init()
if __name__ == "__main__":
    # encrypt msg to a file
    msgToEncryptedFile(input('type password:'),'passwd.txt')

    # decrypt the file
    print(encryptedFileToMsg('passwd.txt'))