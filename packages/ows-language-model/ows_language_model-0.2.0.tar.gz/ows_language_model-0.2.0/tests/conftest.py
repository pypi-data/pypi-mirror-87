import pytest
import os

from ows_language_model.config import config

@pytest.fixture
def text_input_data():
    return 'This is a sentence'