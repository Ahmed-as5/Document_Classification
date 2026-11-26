import pytest

# Adjust the function name to match the real code
from src.preprocessing.text_preprocessing import clean_text


def test_returns_string():
    assert isinstance(clean_text("Hello   WORLD!!"), str)


def test_normal_text_not_emptied():
    assert clean_text("Invoice payment is due").strip()


@pytest.mark.parametrize("text", ["", "   "])
def test_empty_text(text):
    assert clean_text(text).strip() == ""


def test_symbols_do_not_crash():
    assert isinstance(clean_text("@#$%^&*()\n\t"), str)
