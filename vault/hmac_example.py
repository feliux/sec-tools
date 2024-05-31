import requests
import base64

# Look for test string and cange it
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
    VAULT_ADDR + "/v1/transit/keys/my_test_hmac_key",
    json={"type": "aes256-gcm96"},
    headers=VAULT_HEADER
)

if 204 == r.status_code:  # The key was generated
    plain_text="Hello HMAC test!"
    print("Text to calculate HMAC: " + plain_text)
    # HMAC
    plain_text_b64 = base64.b64encode(bytes(plain_text, "utf-8")).decode()
    r = requests.post(
            VAULT_ADDR + "/v1/transit/hmac/my_test_hmac_key/sha2-256",
            json={"input": plain_text_b64},
            headers=VAULT_HEADER
        )

    if 200 == r.status_code:  # HMAC OK
        hmac = r.json()["data"]["hmac"]
        print("HMAC value: " + hmac)
        # Verify
        r = requests.post(
                VAULT_ADDR + "/v1/transit/verify/my_test_hmac_key/sha2-256",
                json={"hmac": hmac, "input": plain_text_b64},
                headers=VAULT_HEADER
            )

        if 200 == r.status_code:  # Verification OK
            print("Verified value: " + str(r.json()["data"]["valid"]))
