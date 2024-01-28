import hashlib


def generate_short_url(original_url):
    hash_object = hashlib.md5(original_url.encode())
    short_url = hash_object.hexdigest()[:8]
    return short_url
