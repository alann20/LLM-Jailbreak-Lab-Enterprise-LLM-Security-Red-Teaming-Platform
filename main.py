import json
import os

# Import the Pydantic model used to represent
# individual jailbreak attack test cases.
from app.models import AttackCase

# Import the LLM client responsible for executing
# the attack prompt against the configured model provider.
from app.runner import LLMClient

# Import the security evaluator responsible for analyzing
# the LLM response and determining whether the attack passed or failed.
from app.evaluator import evaluate


# Path to the JSON file containing the attack test cases.
DATASET = "attacks/dataset.json"

# Path where the evaluation results will be stored.
RESULTS = "results/results.json"


def load_attacks():
    """
    Load jailbreak attack cases from the JSON dataset.

    Returns:
        list[AttackCase]:
            A list of validated AttackCase objects.
    """

    # Open the attack dataset using UTF-8 encoding.
    with open(
        DATASET,
        "r",
        encoding="utf-8"
    ) as file:

        # Deserialize the JSON file into Python objects.
        data = json.load(file)

    # Convert each JSON object into an AttackCase model.
    #
    # AttackCase(**item) validates the structure
    # of every attack test case before execution.
    return [
        AttackCase(**item)
        for item in data
    ]


def main():
    """
    Execute the LLM jailbreak security test campaign.

    The workflow is:

        1. Create results directory
        2. Load attack cases
        3. Initialize LLM client
        4. Execute each attack
        5. Evaluate the LLM response
        6. Store the evaluation results
        7. Generate a JSON security report
    """

    # Create the results directory if it does not already exist.
    #
    # exist_ok=True prevents an exception if the directory
    # is already present.
    os.makedirs(
        "results",
        exist_ok=True
    )

    # Load all jailbreak attack scenarios
    # from the attack dataset.
    attacks = load_attacks()

    # Initialize the LLM client.
    #
    # The actual provider can be configured through
    # the MODEL_PROVIDER environment variable.
    #
    # Examples:
    #   MODEL_PROVIDER=mock
    #   MODEL_PROVIDER=openai
    client = LLMClient()

    # List that will contain the final evaluation results.
    results = []

    # Iterate through every attack scenario
    # defined in the attack library.
    for attack in attacks:

        # Display the current attack being executed.
        #
        # Example:
        # Running JB-001 [instruction_override]
        print(
            f"Running {attack.id} "
            f"[{attack.category}]"
        )

        # Send the attack prompt to the configured LLM provider.
        #
        # The provider could be:
        # - OpenAI
        # - Mock LLM
        # - Local LLM
        # - Other supported providers
        response = client.execute(
            attack.prompt
        )

        # Evaluate the model response.
        #
        # The evaluator determines whether the model
        # resisted the jailbreak attempt and calculates
        # the associated security risk.
        result = evaluate(
            attack,
            response
        )

        # Convert the Pydantic evaluation object
        # into a standard Python dictionary and
        # append it to the results collection.
        results.append(
            result.model_dump()
        )

        # Determine the test status.
        #
        # PASS means the security control resisted
        # the attack according to the evaluator.
        #
        # FAIL means the attack was considered successful
        # or the expected security behavior was not observed.
        status = (
            "PASS"
            if result.passed
            else "FAIL"
        )

        # Display the result of the current test.
        #
        # Example:
        # JB-001: PASS
        print(
            f"{attack.id}: {status}"
        )

    # Open the output file where the complete
    # security evaluation results will be stored.
    with open(
        RESULTS,
        "w",
        encoding="utf-8"
    ) as file:

        # Serialize the evaluation results as formatted JSON.
        #
        # indent=2 makes the report human-readable.
        #
        # ensure_ascii=False preserves Unicode characters.
        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    # Inform the user where the security report was generated.
    print(
        f"\nResults saved to {RESULTS}"
    )


# Python entry point.
#
# This condition ensures that main() is executed
# only when this file is run directly:
#
#     python main.py
#
# It will not automatically execute when main.py
# is imported by another Python module.
if __name__ == "__main__":
    main()