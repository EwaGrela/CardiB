import pytest

from cardb import CarDB


@pytest.fixture
def cardb():
    return CarDB()
