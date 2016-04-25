import binascii
from Crypto.Cipher import AES
from Crypto.Util import Counter

def decrypt(key, ciphertext, mode):
    key = binascii.unhexlify(key)
    ciphertext = binascii.unhexlify(ciphertext)
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    #ciphertext = padding(ciphertext)
    encobj = getAES(key, mode, iv)
    plaintext = encobj.decrypt(ciphertext)
    print("\n", key, iv)
    print(ciphertext)
    print(plaintext)

def getAES(key, mode, iv, counter=None):
    if mode == AES.MODE_CBC:
        encobj = AES.new(key, mode, iv)
    elif mode == AES.MODE_CTR:
        if counter is None:
            counter = Counter.new(128)
        encobj = AES.new(key, mode, counter=counter)
    return encobj

def padding(data):
    length = 16 - (len(data) % 16)
    data += bytes([length])*length
    return data

# Basic CBC mode encryption needs padding.
key = '140b41b22a29beb4061bda66b6747e14'
ciphertext = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
decrypt(key, ciphertext, AES.MODE_CBC)

# Our implementation uses rand. IV
ciphertext = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'
decrypt(key, ciphertext, AES.MODE_CBC)

#does not work answer is CTR mode lets you build a stream cipher from a block cipher.
key = '36f18357be4dbd77f050515c73fcf9f2'
ciphertext = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'
decrypt(key, ciphertext, AES.MODE_CTR)

#does not work answer is Always avoid the two time pad!
ciphertext = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'
decrypt(key, ciphertext, AES.MODE_CTR)

