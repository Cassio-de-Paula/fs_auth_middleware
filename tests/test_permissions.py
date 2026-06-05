import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        SECRET_KEY="test-secret",
        DEFAULT_CHARSET="utf-8",
        INSTALLED_APPS=[],
        USE_TZ=True,
    )
    django.setup()

from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, SimpleTestCase, override_settings
from rest_framework.response import Response
from unittest.mock import patch

from fs_auth_middleware.decorators import has_permissions
from fs_auth_middleware.utils import (
    get_access_token_from_request,
    get_refresh_token_from_request,
)


class CookieSettingsTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(FS_AUTH_ACCESS_TOKEN="custom_access_token")
    def test_get_access_token_from_configured_cookie_name(self):
        request = self.factory.get(
            "/",
            HTTP_COOKIE="access_token=old-value; custom_access_token=access-value",
        )

        self.assertEqual(get_access_token_from_request(request), "access-value")

    @override_settings(FS_AUTH_REFRESH_TOKEN="custom_refresh_token")
    def test_get_refresh_token_from_configured_cookie_name(self):
        request = self.factory.get(
            "/",
            HTTP_COOKIE="refresh_token=old-value; custom_refresh_token=refresh-value",
        )

        self.assertEqual(get_refresh_token_from_request(request), "refresh-value")

    def test_missing_access_token_setting_raises_improperly_configured(self):
        request = self.factory.get("/")

        with self.assertRaisesMessage(ImproperlyConfigured, "FS_AUTH_ACCESS_TOKEN"):
            get_access_token_from_request(request)

    @override_settings(
        FS_AUTH_ACCESS_TOKEN="custom_access_token",
        FS_AUTH_REFRESH_TOKEN="custom_refresh_token",
    )
    def test_inactive_user_deletes_configured_cookies(self):
        @has_permissions(["app.view_model"])
        def view(request):
            return Response({"ok": True})

        request = self.factory.get(
            "/",
            HTTP_COOKIE=(
                "custom_access_token=access-value; "
                "custom_refresh_token=refresh-value"
            ),
        )

        with patch(
            "fs_auth_middleware.decorators.decode_access_token",
            return_value={"user_id": "1", "permissions": ["app.view_model"]},
        ), patch(
            "fs_auth_middleware.decorators.validate_user_is_active",
            return_value=False,
        ):
            response = view(request)

        self.assertIn("custom_access_token", response.cookies)
        self.assertIn("custom_refresh_token", response.cookies)
        self.assertNotIn("access_token", response.cookies)
        self.assertNotIn("refresh_token", response.cookies)
        self.assertEqual(response.cookies["custom_refresh_token"]["path"], "/session/")
