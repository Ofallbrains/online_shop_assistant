from agent import agent
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from deepeval.models import AnthropicModel

load_dotenv()

evaluation_model = AnthropicModel(model="claude-haiku-4-5")

EVALUATION_CASES = [
    {
        "input": "What is the price of P002?",
        "expected_behavior": "Correctly reports 15,000 RWF",
        "improvement": "Ensure the agent calls check_price with P002.",
    },
    {
        "input": "Find the laptop",
        "expected_behavior": "Returns the laptop catalogue details",
         "improvement": "Always call search_product instead of asking for unnecessary details.",
    },
    {
        "input": "What is the price of P999?",
        "expected_behavior": "Clearly reports that the product does not exist",
        "improvement": "Clearly explain that P999 is not in the catalogue.",
    },
]

def run_agent(user_input: str) -> str:
    return agent.invoke({
         "messages": [
            {
                "role": "user",
                "content": user_input,
            }
        ]
    })
    
    
def get_final_response(result) -> str:
    return result["messages"][-1].content


def get_tool_context(result) -> list[str]:
    context = []

    for message in result["messages"]:
        if getattr(message, "type", None) == "tool":
            context.append(str(message.content))

    return context


test_cases = []

for case in EVALUATION_CASES:
    result = run_agent(case["input"])
    actual_response = get_final_response(result)
    tool_context = get_tool_context(result)

    print("=" * 70)
    print(f"Input: {case['input']}")
    print(f"Actual response: {actual_response}")
    print(f"Tool context: {tool_context}")

    test_cases.append(
        LLMTestCase(
            input=case["input"],
            actual_output=actual_response,
            expected_output=case["expected_behavior"],
            retrieval_context=tool_context,
        )
    )


metrics = [
    AnswerRelevancyMetric(
        threshold=0.7,
        include_reason=True,
        model=evaluation_model,
    ),
    FaithfulnessMetric(
        threshold=0.7,
        include_reason=True,
        model=evaluation_model,
    ),
]

results = evaluate(
    test_cases=test_cases,
    metrics=metrics,
)

print("\nEvaluation completed.")
print(results)