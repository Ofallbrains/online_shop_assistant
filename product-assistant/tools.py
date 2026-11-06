from langchain.tools import tool
import logging
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

logger = logging.getLogger(__name__)


PRODUCTS_FILE = Path(__file__).parent / "products.json"

def load_products():
    """Load products from products.json"""
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
@tool
def search_product(query: str) -> str:
    """this tool searches the product catalogue by product ID, name or description
    """
    logger.info("Tool call started | tool=search_product")
    try:
        products = load_products()
    except (OSError, json.JSONDecodeError) as error:
        logger.exception("Tool call failed | tool=search_product")
        return "Product catalogue is currently unavailable."
    query = query.strip().lower()
    
    matches = [
        product
        for product in products
        if (
            query in product["id"].lower() or query in product["name"].lower() or query in product["description"].lower()
        )
    ]
    if not matches: 
        return {"status": f"No product found matching '{query}'"}
    
    return matches

@tool
def check_price(product_id: str) -> str:
    """this tool checks the actual price of the product using its product ID"""
    logger.info("Tool call started | tool=check_price | product_id=%s", product_id)
    products = load_products()
    product_id = product_id.upper()
    for product in products:
        if product["id"] == product_id:
            return f"Price : {product['price']:,} RWF"
    
    return f"Product {product_id} not found in the catalogue"


# print(search_product.invoke("laptop"))
# print(check_price.invoke("P005"))