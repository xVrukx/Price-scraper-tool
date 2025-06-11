# conftest.py
import pytest

@pytest.fixture
def test1_keyword():
    return "iphone"
@pytest.fixture
def test2_keyword():
    return "140000"