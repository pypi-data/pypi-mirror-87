import hashlib
def md5(text):
    return hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()
def sha256(text):
    return hashlib.new("sha256", text.encode(encoding='UTF-8')).digest()
def sha1(text):
    return hashlib.new("sha1", text.encode(encoding='UTF-8')).digest()
