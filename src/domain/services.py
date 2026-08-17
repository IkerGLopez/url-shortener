import hashlib
import base64

def generate_alias(url: str) -> str:
    hash_bytes = hashlib.sha256(url.encode('utf-8')).digest()
    base64_code = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')
    clean_code = base64_code.rstrip('=')
    final_alias = clean_code[:6]

    return final_alias