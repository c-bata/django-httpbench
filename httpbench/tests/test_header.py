from django.test import TestCase, override_settings

from httpbench.header import (
    get_username_header_key,
    get_username_wsgi_env_key,
)


class HeaderTest(TestCase):
    def test_get_username_header_key(self):
        actual = get_username_header_key()
        expected = "X-USERNAME"
        self.assertEqual(actual, expected)

    def test_get_username_wsgi_env_key(self):
        actual = get_username_wsgi_env_key()
        expected = "HTTP_X_USERNAME"
        self.assertEqual(actual, expected)

    @override_settings(HTTP_BENCH_USERNAME_KEY='FOO-BAR')
    def test_get_username_header_key_with_settings(self):
        actual = get_username_header_key()
        expected = "FOO-BAR"
        self.assertEqual(actual, expected)

    @override_settings(HTTP_BENCH_USERNAME_KEY='FOO-BAR')
    def test_get_username_wsgi_env_key_with_settings(self):
        actual = get_username_wsgi_env_key()
        expected = "HTTP_FOO_BAR"
        self.assertEqual(actual, expected)
