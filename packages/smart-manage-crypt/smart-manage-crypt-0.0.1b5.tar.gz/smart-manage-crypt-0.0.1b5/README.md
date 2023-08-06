# CryptLib

Advanced Encryption Standard (AES) used in CFB mode with 128-bit block size and
initialization vector (IV) with 16-bytes long.
---
Encrypt and decrypt methods used with string (which want to encrypt 
or decrypt), key (which sha256 hash function passed to AES constructor)
and salt (Initialization vector (IV) with 16-bytes long). 
---
Salt can not to passed in methods or Crypt class, but in this way 
salt initialized by default value.
## Encrypt string (helper)
Method which u can call without using Crypt class.
```
from crypt import encrypt

enc_string = encrypt(str_to_encrypt="test", secret="secret_key", salt="abcdefghijklmnop")
```
Value in enc_string from this test will be: '-_-0qlMQ=='
## Decrypt string (helper)
Method which u can call without using Crypt class.
```
from crypt import decrypt

dec_string = decrypt(str_to_decrypt="-_-0qlMQ==", secret="secret_key", salt="abcdefghijklmnop")
```
Value in dec_string from this test will be: 'test'

## How use Crypt class
To initialize object you need passed salt to Crypt constructor. 
```
from crypt import Crypt

crypt = Crypt(salt="testtesttesttest")
```
You can use methods encrypt and decrypt by passing str data and key.
```
enc_string = crypt.encrypt(str_to_enc="test", str_key="secret_key")
dec_string = crypt.decrypt(enc_str=enc_string, str_key="secret_key")
```
Also you can change passed salt to Crypt constructor 
to default salt or random generated salt by using methods 
set_default_salt or set_random_salt.
```
cur_salt = crypt.set_default_salt()
cur_salt = crypt.set_random_salt()
```