import requests
import base64

# Look for test string and change it
# Global config
TOKEN = "changeme-vault-token"
VAULT_ADDR="http://127.0.0.1:8200"
VAULT_HEADER={"X-VAULT-TOKEN": TOKEN}  # Remember to update this Vault Token

r = requests.post(
    VAULT_ADDR + "/v1/sys/mounts/transit",
    json={"type":"transit"},
    headers=VAULT_HEADER
)

# Create a key
r = requests.post(
    VAULT_ADDR + "/v1/transit/keys/my_test_key",
    json={"type":"aes256-gcm96"},
    headers=VAULT_HEADER
)

if 204 == r.status_code:  # The key was generated
    plain_text = "Hello test!"
    print("Text to encrypt: " + plain_text)
    # Encrypt
    plain_text_b64 = base64.b64encode(bytes(plain_text, "utf-8")).decode()
    r = requests.post(
            VAULT_ADDR + "/v1/transit/encrypt/my_test_key",
            json={"plaintext": plain_text_b64},
            headers=VAULT_HEADER
        )

    if 200 == r.status_code:  # Encryption OK
        ciphertext = r.json()["data"]["ciphertext"]
        print("Encrypted text: " + ciphertext)
        # Decrypt
        r = requests.post(
                VAULT_ADDR + "/v1/transit/decrypt/my_test_key",
                json={"ciphertext": ciphertext},
                headers=VAULT_HEADER
            )

        if 200 == r.status_code:  # Decryption OK
            print("Decrypted text: " + base64.b64decode(r.json()["data"]["plaintext"]).decode())
