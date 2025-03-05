import uuid
from hashlib import sha256

import pytest
from pydantic import ValidationError

from src.models.models import RegisterModel, LoginModel, UserModel
from src.config import PASSWORD_SALT


def test_register_model_password_hashing():
    login = "test_login"
    password = "secure_password"
    model = RegisterModel(
        nickname=login,
        password=password,
        email="test@email.com"
    )

    expected_password = password + login + PASSWORD_SALT
    expected_password = sha256(expected_password.encode()).hexdigest()

    assert model.password == expected_password


def test_register_model_email_validation_error():
    login = "test_login"
    password = "secure_password"
    email = "test@wrong_email"

    with pytest.raises(ValidationError):
        RegisterModel(
            nickname=login,
            password=password,
            email=email
        )


def test_login_model_password_hashing():
    login = "test_login"
    password = "test_password"

    model = LoginModel(
        nickname=login,
        password=password,
    )

    expected_password = password + login + PASSWORD_SALT
    expected_password = sha256(expected_password.encode()).hexdigest()

    assert model.password == expected_password


def test_user_model_email_validation_error():
    nickname = "test_nickname"
    public_id = uuid.uuid4()
    auth_id = uuid.uuid4()
    email = "test@wrong_email"
    with pytest.raises(ValidationError):
        UserModel(
            nickname=nickname,
            public_id=public_id,
            auth_id=auth_id,
            email=email
        )
