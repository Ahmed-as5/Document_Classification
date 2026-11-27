import nltk
import pytest

from src.preprocessing.text_preprocessing import _load_nltk_resources, clean_text


def test_clean_text_normalizes_case_punctuation_and_whitespace():
    assert clean_text("  THE quick, brown fox!  ") == "the quick brown fox"


def test_clean_text_removes_standalone_numbers():
    assert clean_text("Invoice 123 total 45 USD") == "invoice total usd"


def test_clean_text_accepts_empty_text():
    assert clean_text("   ") == ""


def test_missing_nltk_data_fails_without_downloading(monkeypatch):
    def missing_resource(_):
        raise LookupError("not found")

    def unexpected_download(*args, **kwargs):
        pytest.fail("NLTK resources must not be downloaded at runtime")

    monkeypatch.setattr(nltk.data, "find", missing_resource)
    monkeypatch.setattr(nltk, "download", unexpected_download)

    with pytest.raises(RuntimeError, match="Provision it from a trusted source"):
        _load_nltk_resources()
