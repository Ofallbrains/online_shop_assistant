
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PRODUCTS_FILE = Path(__file__).with_name("products.json")


def load_products():
    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Product catalogue file was not found: %s", PRODUCTS_FILE)
        raise
    except json.JSONDecodeError:
        logging.error("Product catalogue contains invalid JSON.")
        raise

def search_product(query: str) -> str:
    try:
        products = load_products()
        query = query.strip().lower()

        matches = [
            product for product in products
            if query in product["id"].lower()
            or query in product["name"].lower()
            or query in product["description"].lower()
        ]

        logger.info(
            "search_product query=%s matches=%d",
            query, len(matches)
        )

        if not matches:
            return "Product not found."

        return json.dumps(matches, ensure_ascii=False)

    except Exception:
        logger.exception("Product search failed")
        return "Unable to search products right now."


def check_price(product_id: str) -> str:
    try:
        products = load_products()
        product_id = product_id.strip().upper()

        product = next(
            (
                item for item in products
                if item["id"].upper() == product_id
            ),
            None
        )

        if product is None:
            logger.warning(
                "Unknown product ID: %s", product_id
            )
            return (
                f"Product {product_id} not found. "
                "No price is available."
            )

        logger.info("Price checked for %s", product_id)

        return (
            f'{product["name"]} (ID {product["id"]}) '
            f'costs {product["price"]:,} RWF.'
        )

    except Exception:
        logger.exception("Price check failed")
        return "Unable to check the price right now."