from src.preprocessing.text_preprocessing import clean_text


def test_clean_text_normalizes_case_punctuation_and_whitespace():
    assert clean_text("  THE quick, brown fox!  ") == "the quick brown fox"


def test_clean_text_removes_standalone_numbers():
    assert clean_text("Invoice 123 total 45 USD") == "invoice total usd"


def test_clean_text_accepts_empty_text():
    assert clean_text("   ") == ""
