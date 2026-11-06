import logging
import time
import re
from logging_config import LOG_FILE
from tools import check_price, search_product
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic


logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are a helpful product assistant for an online shop.

Rules:
1. For product names or descriptions, use search_product. Use only verified catalogue information.
2. If the user asks for a price and search_product finds a product,
   always call check_price using the exact product ID returned by search_product.
3. Do not ask for brand or model details when the catalogue already contains
   an exact matching product.
4. Never invent product names, IDs, descriptions, or prices.
5. Use only information returned by the tools.
6. If no product is found, clearly say so.
7. Keep responses concise and professional.
8. Never return a price unless it came from the catalogue tool.
9. Never substitute another product ID.
"""

load_dotenv()

model = ChatAnthropic(model="claude-haiku-4-5")

agent = create_agent(
    model=model,
    tools=[search_product, check_price],
    system_prompt=SYSTEM_PROMPT,
)

PRODUCT_ID_PATTERN = re.compile(r"\bP\d{3}\b", re.IGNORECASE)

def run_agent(user_input: str) -> str:
    """Run the agent and log request, status and latency."""
    start_time = time.perf_counter()
    logger.info("Request started")
    
    try:
        product_id_match = PRODUCT_ID_PATTERN.search(user_input)
        
        if product_id_match:
            product_id = product_id_match.group(0).upper()
            result = check_price.invoke(product_id)

            logger.info(
                "Validated explicit product ID | product_id=%s",
                product_id,
            )
            
        else:
            response = agent.invoke({
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ]
            })
            result = response["messages"][-1].content
        latency = time.perf_counter() - start_time
        logger.info(
            "Request completed | success=true | latency=%.3fs",
            latency,
        )
        return result

    except Exception:
        latency = time.perf_counter() - start_time
        logger.exception(
            "Request completed | success=false | latency=%.3fs",
            latency,
        )
        raise   
           
    
# if __name__ == "__main__":
#     requests = [
#         "What is the price of P002?",
#         "Find the laptop",
#         "What is the price of P999?",
#         "Find the keyboard",
#         "What is the price of P004?",
#     ]

#     for request in requests:
#         print(f"\nRequest: {request}")
#         print(run_agent(request))