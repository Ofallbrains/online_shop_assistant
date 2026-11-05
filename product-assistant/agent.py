from tools import check_price, search_product
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

SYSTEM_PROMPT = """
You are a helpful product assistant for an online shop.

Rules:
1. For every product request, call search_product first.
2. If the user asks for a price and search_product finds a product,
   always call check_price using the exact product ID returned by search_product.
3. Do not ask for brand or model details when the catalogue already contains
   an exact matching product.
4. Never invent product names, IDs, descriptions, or prices.
5. Use only information returned by the tools.
6. If no product is found, clearly say so.
7. Keep responses concise and professional.
"""

load_dotenv()

model = ChatAnthropic(model="claude-haiku-4-5")


agent = create_agent(
    model=model,
    tools=[search_product, check_price],
    system_prompt=SYSTEM_PROMPT,
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Find the keyboard and tell me its price."
        }
    ]
})

print(response["messages"][-1].content)