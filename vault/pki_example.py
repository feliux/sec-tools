import requests

# Look for test string and change it
# Global config
TOKEN = "changeme-vault-token"
VAULT_ADDR="http://127.0.0.1:8200"
VAULT_HEADER={"X-VAULT-TOKEN": TOKEN}  # Remember to update this Vault Token

# Create root CA
r = requests.post(
    VAULT_ADDR + "/v1/sys/mounts/pki",
    json={"type":"pki"},
    headers=VAULT_HEADER
)
r = requests.post(
    VAULT_ADDR + "/v1/sys/mounts/pki/tune",
    json={"max_lease_ttl":"87600h"},
    headers=VAULT_HEADER
)
r = requests.post(
	VAULT_ADDR + "/v1/pki/root/generate/internal",
    json={"common_name":"test Root CA", "ttl":"87600h"},
    headers=VAULT_HEADER
)

print(r.json()["data"]["certificate"], file=open("ca.crt", "w"))

r = requests.post(
	VAULT_ADDR + "/v1/pki/config/urls",
    json={
		"issuing_certificates": VAULT_ADDR + "/v1/pki/ca",
        "crl_distribution_points": VAULT_ADDR + "/v1/pki/crl"},
    headers=VAULT_HEADER
)

# Create and sign Intermediate CA
r = requests.post(
	VAULT_ADDR + "/v1/sys/mounts/pki_int",
    json={"type":"pki"},
    headers=VAULT_HEADER
)
r = requests.post(
	VAULT_ADDR + "/v1/sys/mounts/pki_int/tune",
    json={"max_lease_ttl":"43800h"},
    headers=VAULT_HEADER
)
r = requests.post(
	VAULT_ADDR + "/v1/pki_int/intermediate/generate/internal",
    json={"common_name":"test Intermediate CA", "ttl":"43800h"},
    headers=VAULT_HEADER
)

csr = r.json()["data"]["csr"]

r = requests.post(
	VAULT_ADDR + "/v1/pki/root/sign-intermediate",
    json={"csr":csr,"format":"pem_bundle"},
    headers=VAULT_HEADER
)

intermediate_ca_cert = r.json()["data"]["certificate"]
print(intermediate_ca_cert, file=open("intermediate_ca.crt", "w"))

r = requests.post(
	VAULT_ADDR + "/v1/pki_int/intermediate/set-signed",
    json={"certificate": intermediate_ca_cert},
    headers=VAULT_HEADER
)

# Create a role
r = requests.post(
	VAULT_ADDR + "/v1/pki_int/roles/test-dot-es",
    json={"allowed_domains": "test.es", "allow_subdomains": True, "max_ttl": "720h"},
    headers=VAULT_HEADER
)

# Create a certificate (ssc.test.es)
r = requests.post(
	VAULT_ADDR + "/v1/pki_int/issue/test-dot-es",
    json={"common_name": "scc.test.es", "ttl": "24h"},
    headers=VAULT_HEADER
)

print(r.json()["data"]["certificate"], file=open("scc_test_es.crt", "w"))
print(r.json()["data"]["private_key"], file=open("scc_test_es.key", "w"))
