# crypt2file

save/load a file with encryption/decryption

## install

```shell
pip install crypt2file
```

## usage

```python
import crypt2file as c

# encrypt msg to a file
c.msgToEncryptedFile(input('type password:'),'passwd.txt')

# decrypt the file
print(c.encryptedFileToMsg('passwd.txt'))
```
