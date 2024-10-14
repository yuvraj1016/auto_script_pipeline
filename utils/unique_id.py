import hashlib

def generate_unique_id(url):
    return hashlib.md5(url.encode()).hexdigest()