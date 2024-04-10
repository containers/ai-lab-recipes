import os
import pytest


@pytest.fixture()
def url():
    return os.environ["MODEL_ENDPOINT"]
