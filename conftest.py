import pytest
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings

# User Fixtures

@pytest.fixture(scope='class')
def store_administrators_group():
    group_name = settings.STORE_ADMINISTRATORS_GROUP
    group = Group.objects.create(name=group_name)

    return group


@pytest.fixture(scope='class')
def store_administrator(request, store_administrators_group):
    user = User.objects.create(username="store_admin",
                               email="store_admin@example.com",
                               password="test1234",
                               is_active=True,
                               is_staff=False)
    user.groups.add(store_administrators_group)
    user = User.objects.get(username="store_admin")
    request.cls.store_administrator = user


@pytest.fixture(scope='class')
def regular_user(request):
    user = User.objects.create(username="regularuser",
                               email="regularuser@example.com",
                               password="test1234",
                               is_active=True,
                               is_staff=False)
    request.cls.regular_user = user


@pytest.fixture(scope='class')
def member_of_staff(request):
    user = User.objects.create(username="staffuser",
                               email="staffuser@example.com",
                               password="test1234",
                               is_active=True,
                               is_staff=True)
    request.cls.member_of_staff = user