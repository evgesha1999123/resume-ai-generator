import base64

def decode_base64_to_utf8(content: str) -> str:
    decoded_bytes = base64.b64decode(content)
    return decoded_bytes.decode("utf-8", errors="replace")