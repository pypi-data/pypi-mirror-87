from unittest import TestCase, mock, main
from aws.iam import *
from po.pretty_object import PrettyObject

po = PrettyObject()


class TestIam(TestCase):

    def test_list_roles(self):
        roles = list_roles('/aws')
        print(f'roles[{len(roles)}]')

        for role in roles:
            path: str = role.get('Path')
            self.assertTrue(path.startswith('/aws'))

        roles = list_roles('/')

        for role in roles:
            path: str = role.get('Path')
            self.assertTrue(path.startswith('/'))

        role_name = get_role_name(roles[-1])

        role = get_role(role_name)
        self.assertIsNotNone(role)
        self.assertEqual(role_name, get_role_name(role))

        role = get_role('bogus')
        self.assertIsNone(role)

    def test_list_profiles(self):
        profiles = list_profiles()
        self.assertIsNotNone(profiles)

        profile_name = get_profile_name(profiles[-1])
        profile = get_profile(profile_name)

        self.assertIsNotNone(profile)
        self.assertEqual(profile_name, get_profile_name(profile))

        profile = get_profile('bogus')
        self.assertIsNone(profile)


if __name__ == "__main__":
    main()