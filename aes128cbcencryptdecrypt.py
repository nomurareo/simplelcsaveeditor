from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA1


PASSWORD = 'lcslime14a5'


def encrypt(data, password=PASSWORD):
    IV = get_random_bytes(16)
    key = PBKDF2(password, IV, dkLen=16, count=100, hmac_hash_module=SHA1)
    cipher = AES.new(key, AES.MODE_CBC, IV)

    data_bytes = data.encode('utf-8')
    encrypted_data = IV + cipher.encrypt(pad(data_bytes, AES.block_size))
    
    return encrypted_data


def decrypt(data, password=PASSWORD):
    IV = data[:16]
    data_to_decrypt = data[16:]

    key = PBKDF2(password, IV, dkLen=16, count=100, hmac_hash_module=SHA1)

    cipher = AES.new(key, AES.MODE_CBC, IV)
    decrypted_data = cipher.decrypt(data_to_decrypt)
    unpadded_data = unpad(decrypted_data, AES.block_size)

    return unpadded_data.decode('utf-8', errors='ignore')


if __name__ == '__main__':
    #========================================================
    # Example decryption usage:
    # encrypted_data = open('LCSaveFile3', 'rb').read()
    # decrypted_result = decrypt(encrypted_data)

    # file = open('LCSaveFile3', 'wt')
    # file.write(decrypted_result)
    # file.close()
    #========================================================

    #========================================================
    # Example encryption usage:
    # unencrypted_data = open('LCSaveFile3', 'rt').read()
    # encrypted_result = encrypt(unencrypted_data)

    # file = open('LCSaveFile3', 'wb')
    # file.write(encrypted_result)
    # file.close()
    #========================================================

    # if __name__ == '__main__':
    #     main()
    pass
