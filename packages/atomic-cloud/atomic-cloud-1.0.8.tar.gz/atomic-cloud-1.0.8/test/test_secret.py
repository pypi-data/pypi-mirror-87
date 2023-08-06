import unittest
from aws import secret, region
import warnings
import json

# NOTE: Don't run this test multiple times in quick succession.
#       Even though the test secrets are perma-deleted afterwards,
#       it usually takes a minute for them to disappear completely.

class TestSecret(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)
        
        cls.STRING_SECRET = secret.create_secret(
            name='unit-test-string-secret',
            description='Test string secret for Atomic Cloud unit tests',
            string='string-secret')

        cls.JSON_SECRET = secret.create_secret(
            name='unit-test-json-secret',
            description='Test JSON secret for Atomic Cloud unit tests',
            kvp={'secret-key': 'secret-value'})

        cls.BINARY_SECRET = secret.create_secret(
            name='unit-test-binary-secret',
            description='Test binarysecret for Atomic Cloud unit tests',
            binary=b'binary-secret')


    @classmethod
    def tearDownClass(cls):
        secret.delete_secret(cls.STRING_SECRET['Name'], perma_delete=True)
        secret.delete_secret(cls.JSON_SECRET['Name'], perma_delete=True)
        secret.delete_secret(cls.BINARY_SECRET['Name'], perma_delete=True)


    ###########################################################################
    # Get Secret Value
    ###########################################################################
    
    def test_get_secret_value_string(self):
        secret_name = self.STRING_SECRET['Name']
        created_secret = self.STRING_SECRET['SecretString']

        retrieved_secret = secret.get_secret_value(secret_name)
        self.assertEqual(retrieved_secret, created_secret)


    def test_get_secret_value_json(self):
        secret_name = self.JSON_SECRET['Name']
        created_secret = self.JSON_SECRET['SecretString']

        retrieved_secret = secret.get_secret_value(secret_name)
        self.assertEqual(created_secret, retrieved_secret)

        created_secret_dict = json.loads(created_secret)
        created_secret_key = next(k for k in created_secret_dict)
        created_secret_value = created_secret_dict[created_secret_key]

        retrieved_secret_value = secret.get_secret_value(secret_name, created_secret_key)
        self.assertEqual(retrieved_secret_value, created_secret_value)


    def test_get_secret_value_binary(self):
        secret_name = self.BINARY_SECRET['Name']
        created_secret = self.BINARY_SECRET['SecretBinary']

        retrieved_secret = secret.get_secret_value(secret_name)
        self.assertEqual(retrieved_secret, created_secret)


    def test_get_secret_value_bogus_name(self):
        result = secret.get_secret_value('bogus')
        self.assertIsNone(result)


    def test_get_secret_value_bogus_key(self):
        result = secret.get_secret_value(self.JSON_SECRET, 'bogus')
        self.assertIsNone(result)


    def test_update_secret_string(self):
        secret_name = self.STRING_SECRET['Name']
        original_value = self.STRING_SECRET['SecretString']

        new_value = 'new-string-secret'
        secret.update_secret(secret_name, string=new_value)

        self.assertEqual(secret.get_secret_value(secret_name), new_value)
        secret.update_secret(secret_name, string=original_value)


    ###########################################################################
    # Create Secret
    ###########################################################################

    def test_create_secret_with_tags(self):
        try:
            string_secret = secret.create_secret(
                name='unit-test-string-secret-with-tags',
                string='string-secret',
                tags={'type': 'string'})['Name']

            binary_secret = secret.create_secret(
                name='unit-test-binary-secret-with-tags',
                binary=b'binary-secret',
                tags={'type': 'binary'})['Name']

            tag_found = lambda tags, k, v: any(pair for pair in tags if pair['Key'] == k and pair['Value'] == v)

            string_secret_tags = region.get_secret().describe_secret(SecretId=string_secret)['Tags']
            self.assertTrue(tag_found(string_secret_tags, 'type', 'string'))

            binary_secret_tags = region.get_secret().describe_secret(SecretId=binary_secret)['Tags']
            self.assertTrue(tag_found(binary_secret_tags, 'type', 'binary'))
        finally:
            secret.delete_secret(string_secret, perma_delete=True)
            secret.delete_secret(binary_secret, perma_delete=True)


    def test_create_secret_multiple_types(self):
        with self.assertRaises(Exception):
            secret.create_secret('toomanytypes', string='string', binary=b'binary')


    ###########################################################################
    # Update Secret
    ###########################################################################

    def test_update_secret_json(self):
        secret_name = self.JSON_SECRET['Name']
        original_value = self.JSON_SECRET['SecretString']
        original_kvp = json.loads(original_value)
        
        new_kvp = {'new-key': 'new-value'}
        secret.update_secret(secret_name, kvp=new_kvp, overwriteJson=False)

        combined_kvp = original_kvp.copy()
        combined_kvp.update(new_kvp)
        retrieved_kvp = json.loads(secret.get_secret_value(secret_name))
        self.assertEqual(retrieved_kvp, combined_kvp)

        secret.update_secret(secret_name, kvp=original_kvp, overwriteJson=True)
        self.assertEqual(secret.get_secret_value(secret_name), original_value)


    def test_update_secret_binary(self):
        secret_name = self.BINARY_SECRET['Name']
        original_value = self.BINARY_SECRET['SecretBinary']

        new_value = b'new-binary-secret'
        secret.update_secret(secret_name, binary=new_value)

        self.assertEqual(secret.get_secret_value(secret_name), new_value)
        secret.update_secret(secret_name, binary=original_value)


    def test_update_secret_multiple_types(self):
        with self.assertRaises(Exception):
            secret.update_secret('toomanytypes', string='string', binary=b'binary')


    ###########################################################################
    # Delete Secret
    ###########################################################################

    def test_delete_secret_nonexistent(self):
        result = secret.delete_secret('bogus')
        self.assertFalse(result)


    def test_delete_secret_recovery_and_perma(self):
        with self.assertRaises(Exception):
            secret.delete_secret('bogus', recovery_window=7, perma_delete=True)


    def test_delete_secret_with_recovery(self):
        try:
            string_secret = secret.create_secret(
                name='unit-test-string-secret-delete-with-recovery',
                string='string-secret')['Name']

            secret.delete_secret(string_secret)
            found = secret.get_secret_value(string_secret)
            self.assertIsNone(found)

            region.get_secret().restore_secret(SecretId=string_secret)
            found = secret.get_secret_value(string_secret)
            self.assertIsNotNone(found)
        finally:
            secret.delete_secret(string_secret, perma_delete=True)


    ###########################################################################
    # Wait for Secret
    ###########################################################################

    def test_wait_for_secret_timeout(self):
        with self.assertRaises(TimeoutError):
            secret.wait_for_secret(self.STRING_SECRET['Name'], 'bogus', timeout=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)