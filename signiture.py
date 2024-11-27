import random
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding
from datetime import datetime, timedelta

expiration_date=365

def exec(csr_pem, root_cert_pem, root_key_pem):

    csr_data = exchange_type_to_byte(csr_pem)
    root_cert_data = exchange_type_to_byte(root_cert_pem)
    root_key_data = exchange_type_to_byte(root_key_pem)
    
    print(csr_data)
    print(root_cert_data)
    print(root_key_data)

    csr = x509.load_pem_x509_csr(csr_data)
    root_cert = x509.load_pem_x509_certificate(root_cert_data)
    root_key = load_pem_private_key(root_key_data,password=None)

    # Verify the CSR signature (optional, to ensure it's valid)
    if not csr.is_signature_valid:
        raise ValueError("Invalid CSR signature")

    serial_number = random.randint(1, 2**64 - 1)


    signed_cert = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(root_cert.subject)
        .public_key(csr.public_key())
        .serial_number(serial_number)
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=expiration_date))
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True,
        )
        .sign(private_key=root_key, algorithm=hashes.SHA256())
    )
    print("Signiture Completed!")

    signed_cert_pem = signed_cert.public_bytes(Encoding.PEM)

    return signed_cert_pem, serial_number


def exchange_type_to_byte(item):
    print(type(item))
    if type(item) is str:
        return item.encode("utf-8")
    else:
        return item