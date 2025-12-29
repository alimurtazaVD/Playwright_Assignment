import pytest


@pytest.fixture(scope="function")
def context():
    """Context fixture to share data between steps"""
    return {}

