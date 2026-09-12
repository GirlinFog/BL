import subprocess

def generate_rsa_keys(private_key_file="private.pem",
                      public_key_file="public.pem",
                      bits=2048):

    subprocess.run([
        "openssl", "genpkey",
        "-algorithm", "RSA",
        "-pkeyopt", f"rsa_keygen_bits:{bits}",
        "-out", private_key_file
    ], check=True)

    subprocess.run([
        "openssl", "pkey",
        "-in", private_key_file,
        "-pubout",
        "-out", public_key_file
    ], check=True)

    with open(public_key_file, "r") as f:
        public_key_content = f.read()

    print("Key generated Successfully")
    print(f"Private key saved in: {private_key_file}")
    print(f"Public key saved in: {public_key_file}")
    print("Public key (PEM format):\n")
    print(public_key_content)


generate_rsa_keys()