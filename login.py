import requests
import json
from typing import Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64


USERNAME="cheav.samnang"
PWD="YTkxMTE5NTNAQUFBQUEqKioqKioK"
BASE_URL="https://api-los.ababank.com/api"
TOKEN_URL=f"{BASE_URL}/login/token"
LOGIN_URL=f"{BASE_URL}/login"


def encrypt(payload: Any, key: str, iv: str) -> str:
    """
    Encrypt payload using AES-CBC with PKCS#7 padding.

    Args:
        payload: Dict/list/string to encrypt.
        key: AES key as a hexadecimal string.
        iv: IV as a hexadecimal string.

    Returns:
        Hexadecimal ciphertext string.
    """

    # Convert hex key/IV to bytes
    try:
        key_bytes = bytes.fromhex(key)
        iv_bytes = bytes.fromhex(iv)
    except ValueError as exc:
        raise ValueError("Key and IV must be valid hexadecimal strings") from exc

    # Validate AES key length
    if len(key_bytes) not in (16, 24, 32):
        raise ValueError(
            f"Invalid AES key length: {len(key_bytes)} bytes. "
            "Expected 16, 24, or 32 bytes."
        )

    # AES block size / IV must always be 16 bytes
    if len(iv_bytes) != AES.block_size:
        raise ValueError(
            f"Invalid IV length: {len(iv_bytes)} bytes. "
            "Expected 16 bytes."
        )

    # Convert payload to UTF-8 bytes
    if isinstance(payload, str):
        plaintext = payload.encode("utf-8")
    else:
        plaintext = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")

    # AES-CBC + PKCS#7 padding
    cipher = AES.new(
        key_bytes,
        AES.MODE_CBC,
        iv_bytes,
    )

    encrypted = cipher.encrypt(
        pad(plaintext, AES.block_size)
    )

    # Node.js Buffer(...).toString('hex') equivalent
    return encrypted.hex()


def login():
    try:
        response = requests.get(
            TOKEN_URL,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        token = data["token"]
        key, iv = token.split("hh")
        payload = {
            "username": USERNAME,
            "password": base64.b64decode(PWD).decode("utf-8").replace("\n", "")
        }

        encrypted_payload = encrypt(payload, key, iv)
        req_body = {
            "token": token,
            "payload": encrypted_payload
        }

        token_response = requests.post(
            LOGIN_URL,
            json=req_body,
            headers={"Content-Type": "application/json"},
            timeout=60
        )

        token_response.raise_for_status()

        return token_response.json()["token"]

    except requests.RequestException as e:
        return str(e)

if __name__ == "__main__":
    token = login()

    print(token)