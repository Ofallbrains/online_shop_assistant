
from agent import ask_agent
import json
from pathlib import Path

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric
)
from deepeval.models import AnthropicModel

from tools import load_products

evaluation_cases = [
    {
        "input": "What is the price of P002?",
        "expected": "Correctly reports 15,000 RWF."
    },
    {
        "input": "Find the laptop",
        "expected": "Returns the laptop's catalogue details."
    },
    {
        "input": "What is the price of P999?",
        "expected": "Clearly reports that the product does not exist."
    }
]

for case in evaluation_cases:
    actual_response = ask_agent(case["input"])

    case["actual"] = actual_response

    print("\nInput:", case["input"])
    print("Expected:", case["expected"])
    print("Actual:", case["actual"])


products = load_products()

catalogue_context = [
    (
        f'{p["id"]}: {p["name"]}; '
        f'{p["description"]}; Price: {p["price"]:,} RWF'
    )
    for p in products
]

test_cases = [
    LLMTestCase(
        input=case["input"],
        actual_output=case["actual"],
        expected_output=case["expected"],
        retrieval_context=catalogue_context
    )
    for case in evaluation_cases
]

judge_model = AnthropicModel(
    model="claude-haiku-4-5",
)

metrics = [
    AnswerRelevancyMetric(
        threshold=0.7,
        include_reason=True,
        model=judge_model
    ),
    FaithfulnessMetric(
        threshold=0.7,
        include_reason=True,
        model=judge_model
    )
]

evaluate(
    test_cases=test_cases,
    metrics=metrics
)

Path("evaluation_results.json").write_text(
    json.dumps(evaluation_cases, indent=2),
    encoding="utf-8"
)
