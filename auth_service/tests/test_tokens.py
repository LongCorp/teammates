import pytest
from jwt import DecodeError
import unittest.mock as mock

from src.models.models import UserModel
from src.entities.tokens import RefreshToken, AccessToken


class TestRefreshToken:
    def test_creation_from_user(self):
        user = UserModel(
            nickname="test_user",
            public_id=123,
            auth_id="a6224487-004e-4fda-9dc7-f9117a2d9bae",
            email="test_user@email.com",
            description="test_user description",
        )

        token = RefreshToken.from_user(user, 86400)

        assert isinstance(token, RefreshToken)

    def test_creation_from_secret_id(self):
        secret_id = "a6224487-004e-4fda-9dc7-f9117a2d9bae"

        token = RefreshToken.from_auth_id(secret_id, 86400)
        assert isinstance(token, RefreshToken)

    def test_get_secret_id(self):
        secret_id = "a6224487-004e-4fda-9dc7-f9117a2d9bae"
        token = RefreshToken.from_auth_id(secret_id, 86400)

        assert token.get_auth_id() == secret_id

    def test_raise_decode_error(self):
        with pytest.raises(DecodeError):
            RefreshToken("wrong_token")

    @mock.patch("jwt.decode")
    def test_raise_type_error(self, mock_decode):
        mock_decode.decode.return_value = {
            "type": "wrong_token_type"
        }

        with pytest.raises(TypeError):
            RefreshToken("wrong_token")


class TestAccessToken:

    def test_creation_from_refresh_token(self):
        secret_id = "a6224487-004e-4fda-9dc7-f9117a2d9bae"

        refresh_token = RefreshToken.from_auth_id(secret_id, 86400)

        access_token = AccessToken.from_refresh_token(refresh_token, 3600)

        assert isinstance(access_token, AccessToken)

    def test_get_secret_id(self):
        secret_id = "a6224487-004e-4fda-9dc7-f9117a2d9bae"
        refresh_token = RefreshToken.from_auth_id(secret_id, 86400)
        access_token = AccessToken.from_refresh_token(refresh_token, 3600)
        assert access_token.get_auth_id() == secret_id

    def test_raise_decode_error(self):
        with pytest.raises(DecodeError):
            AccessToken("wrong_token")

    @mock.patch("jwt.decode")
    def test_raise_type_error(self, mock_decode):
        mock_decode.decode.return_value = {
            "type": "wrong_token_type"
        }

        with pytest.raises(TypeError):
            AccessToken("wrong_token")
