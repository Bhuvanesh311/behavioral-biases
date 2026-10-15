import pytest
from django.db import IntegrityError
from apps.accounts.models import User

pytestmark = pytest.mark.django_db


def test_default_role_is_investor():
    u = User.objects.create_user("a", "a@x.com", "pass12345")
    assert u.role == User.Role.INVESTOR


def test_email_must_be_unique():
    User.objects.create_user("a", "a@x.com", "pass12345")
    with pytest.raises(IntegrityError):
        User.objects.create_user("b", "a@x.com", "pass12345")


def test_timestamps_set_and_updated():
    u = User.objects.create_user("a", "a@x.com", "pass12345")
    assert u.created_at and u.updated_at
    old = u.updated_at
    u.role = User.Role.ADVISOR
    u.save()
    u.refresh_from_db()
    assert u.updated_at > old


def test_str_returns_email():
    u = User.objects.create_user("a", "a@x.com", "pass12345")
    assert str(u) == "a@x.com"