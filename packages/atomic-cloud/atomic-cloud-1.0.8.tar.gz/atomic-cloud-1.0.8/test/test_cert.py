from unittest import TestCase

from aws.cert import generate_self_signed_cert, import_cert, delete_cert, generate_and_import_self_signed, get_certs, get_cert_arn
from aws.region import get_acm
import os


class TestCertificateManager(TestCase):

    def test_self_signed(self):
        c = generate_self_signed_cert('test.simoncomputing.com', 'US', 'Virginia', 'Alexandria', 'SimonComputing', 2)
        self.assertIsNotNone(c['private'])
        self.assertIsNotNone(c['public'])


    def test_import_self_signed(self):
        try:
            c = generate_self_signed_cert('unittest1234.simoncomputing.com', 'US', 'Virginia', 'Alexandria', 'SimonComputing', 2)
            arn = import_cert('unittest1234.simoncomputing.com', c['public'], c['private'], {'lol': 'tag'})
            check_exists = get_cert_arn('unittest1234.simoncomputing.com')
            if not check_exists:
                self.fail('cert does not exist!')
            tags = get_acm().list_tags_for_certificate(CertificateArn = arn).get('Tags', [])
            for tag in tags:
              if tag.get('Key') == 'lol':
                self.assertEqual('tag', tag.get('Value'))
              elif tag.get('Key') == 'Name':
                self.assertEqual('unittest1234.simoncomputing.com', tag.get('Value'))
              else:
                self.fail('cert missing tags!')
        except:
            self.fail('cert not imported!')
        finally:
            delete_cert('unittest1234.simoncomputing.com')

    def test_gen_import_self_signed(self):
        try:
            arn = generate_and_import_self_signed('unittest1234.simoncomputing.com', 'unittest1234.simoncomputing.com', 'US', 'Virginia', 'Alexandria', 'SimonComputing', 2)
            get_acm().get_certificate(CertificateArn = arn)
        except:
            self.fail('cert not imported!')
        finally:
            delete_cert('unittest1234.simoncomputing.com')

    def test_get_certs(self):
        try:
            pre_list = get_certs()
            found = False
            for cert in pre_list:
                if cert['DomainName'] == 'unittest1234.simoncomputing.com':
                    found = True
            self.assertFalse(found)
            c = generate_self_signed_cert('unittest1234.simoncomputing.com', 'US', 'Virginia', 'Alexandria', 'SimonComputing', 2)
            import_cert('unittest1234.simoncomputing.com', c['public'], c['private'])
            post_list = get_certs()
            found = False
            for cert in post_list:
                if cert['DomainName'] == 'unittest1234.simoncomputing.com':
                    found = True
            self.assertTrue(found)
        finally:
            delete_cert('unittest1234.simoncomputing.com')

    def test_delete_cert(self):
        try:
            c = generate_self_signed_cert('unittest1234.simoncomputing.com', 'US', 'Virginia', 'Alexandria', 'SimonComputing', 2)
            import_cert('unittest1234.simoncomputing.com', c['public'], c['private'])
            pre_list = get_certs()
            found = False
            for cert in pre_list:
                if cert['DomainName'] == 'unittest1234.simoncomputing.com':
                    found = True
            self.assertTrue(found)
            delete_cert('unittest1234.simoncomputing.com')
            post_list = get_certs()
            found = False
            for cert in post_list:
                if cert['DomainName'] == 'unittest1234.simoncomputing.com':
                    found = True
            self.assertFalse(found)
        finally:
            delete_cert('unittest1234.simoncomputing.com')
            

    def test_delete_bad_cert(self):
        self.assertFalse(delete_cert('THISCERTDOESNOTEXIST'))

    def test_get_bad_cert_arn(self):
        self.assertFalse(get_cert_arn('THISCERTDOESNOTEXIST'))