
import pytest
from tools import search_product, check_price
from unittest.mock import patch
from tools import load_products


def test_load_products_missing_file():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            load_products()

def test_search_existing_product():
    result = search_product("Laptop")
    assert "P001" in result
    assert "Laptop" in result


def test_search_product_case_insensitive():
    result = search_product("laptop")
    assert "P001" in result


def test_check_price_existing_product():
    result = check_price("P002")
    assert "15,000 RWF" in result


def test_check_price_invalid_product():
    result = check_price("P999")
    assert "not found" in result.lower()
    assert "no price" in result.lower()

def test_check_price_with_lowercase_id():
    result = check_price("p002")
    assert "15,000 RWF" in result