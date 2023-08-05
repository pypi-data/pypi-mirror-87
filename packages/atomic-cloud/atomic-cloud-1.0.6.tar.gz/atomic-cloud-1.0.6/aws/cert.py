from aws.region import get_acm
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes

import datetime

def generate_self_signed_cert(site_name: str, country: str, state: str, locality: str, organization: str, valid_for_days: int = 30):
    """
      Generates a self signed certificate. Returned in the format:
      {
          'public': '[the public cert bytes (PEM)]',
          'private': '[the private rsa key (PEM)]'
      }

      :param site_name: the website name/url the cert is for
      :param country: the country you're in
      :param state: the state/province/prefecture/etc you're in
      :param locality: the city/town/region you're in
      :param organization: the organization the site belongs to
      :param valid_for_days: the number of days the cert is valid for (default 30)

      :return: a new certificate's public and private information
    """
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
        x509.NameAttribute(NameOID.COMMON_NAME, site_name),
    ])
    cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=valid_for_days)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName('localhost')]), critical=False
        ).sign(
            key, hashes.SHA256()
        )

    return {
      'public': cert.public_bytes(encoding=serialization.Encoding.PEM),
      'private': key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
    }


def get_certs():
    """
    :return: list of certificates issued in the region, each with the keys 'CertificateArn' and 'DomainName'
    """
    return get_acm().list_certificates(CertificateStatuses = ['ISSUED']).get('CertificateSummaryList')

def get_cert_arn(domain):
    """
    Returns the ARN of a certificate with the specified domain. If there is no cert, it returns false.

    :param domain: The domain name of the ACM cert you're looking for
    :return: False if there is no cert with the specified ARN, the ARN of that cert if it does.
    """
    certs = get_certs()
    for c in certs:
        if c['DomainName'] == domain:
            return c['CertificateArn']
    return False


def delete_cert(domain):
    """
    Deletes a cert with the domain name `domain`

    :param domain: The domain name of the ACM cert to delete
    :return: True if it was deleted, False if it wasn't found
    """
    certs = get_certs()
    for c in certs:
        if c['DomainName'] == domain:
            get_acm().delete_certificate(CertificateArn = c['CertificateArn'])
            return True
    
    return False
            

def import_cert(name, certificate, private_key, tags = {}):
    """
    Imports a cert from the cert and private key. Useful for importing self-signed certs as well as non-AWS signed keys.

    :param name: the name to use for the acm cert object. usually the domain of the cert w/o wildcards
    :param certificate: PEM encoded cert bytes
    :param private_key: PEM encoded private key that the cert was created with
    :param tags: dict containing tags for the acm cert object
    """
    tags['Name'] = name
    aws_tags = [ {'Key': k, 'Value': tags[k]} for k in tags ]

    return get_acm().import_certificate(Certificate = certificate, PrivateKey = private_key, Tags = aws_tags).get('CertificateArn', False)
    
def generate_and_import_self_signed(name: str, site_name: str, country: str, state: str, locality: str, organization: str, valid_for_days: int = 30, tags = {}):
    """
    Generates and imports a self signed cert.

    :param name: the name to use for the acm cert object. usually the domain of the cert w/o wildcards
    :param site_name: the website name/url the cert is for
    :param country: the country you're in
    :param state: the state/province/prefecture/etc you're in
    :param locality: the city/town/region you're in
    :param organization: the organization the site belongs to
    :param valid_for_days: the number of days the cert is valid for (default 30)
    :param tags: dict containing tags for the acm cert object
    """
    sscert = generate_self_signed_cert(site_name, country, state, locality, organization, valid_for_days)
    return import_cert(name, sscert.get('public', 'N/A'), sscert.get('private', 'N/A'), tags)
