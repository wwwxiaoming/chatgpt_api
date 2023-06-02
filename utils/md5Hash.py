import hashlib

def md5_hash(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    hashed = md5.hexdigest()
    return hashed