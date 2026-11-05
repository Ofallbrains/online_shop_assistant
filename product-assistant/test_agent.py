import pytest
import tools
from tools import search_product, check_price


def test_search_existing_product():
    result = search_product.invoke("Laptop")
    assert "Laptop" in result
    assert "P001" in result


def test_check_price_p002():
    result = check_price.invoke("P002")
    assert "15,000 RWF" in result


def test_unknown_product_price():
    result = check_price.invoke("P999")
    assert "not found" in result.lower()


def test_search_handles_tool_exception(monkeypatch):
    def failing_load_products():
        raise OSError("Catalogue unavailable")

    monkeypatch.setattr(tools, "load_products", failing_load_products)
    result = search_product.invoke("Laptop")
    assert "unavailable" in result.lower()