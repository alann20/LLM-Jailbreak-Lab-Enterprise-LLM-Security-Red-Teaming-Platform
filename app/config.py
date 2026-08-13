# Import the os module to work with:
# - Environment variables
# - File paths
# - Operating system-specific paths
import os


# Import load_dotenv to load configuration values
# from the project's .env file.
from dotenv import load_dotenv


# ============================================================
# PROJECT BASE DIRECTORY
# ============================================================

# Determine the absolute path of the current file.
#
# Example:
# C:\...\llm-jailbreak-lab\app\config.py
CURRENT_FILE = os.path.abspath(__file__)


# Move one directory up from the current file.
#
# Result:
# C:\...\llm-jailbreak-lab\app
APP_DIR = os.path.dirname(
    CURRENT_FILE
)


# Move one additional directory up.
#
# Result:
# C:\...\llm-jailbreak-lab
#
# This is the root directory of the project.
BASE_DIR = os.path.dirname(
    APP_DIR
)


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

# Build the absolute path to the .env file.
#
# Expected project structure:
#
# llm-jailbreak-lab/
# ├── .env
# ├── main.py
# └── app/
#     └── config.py
ENV_FILE = os.path.join(
    BASE_DIR,
    ".env"
)


# Load environment variables from the .env file.
#
# This allows the application to access configuration
# such as API keys and model settings without hardcoding
# sensitive values in the source code.
load_dotenv(
    ENV_FILE
)


# ============================================================
# OPENAI CONFIGURATION
# ============================================================

# Read the OpenAI API key from the environment.
#
# The API key should NEVER be hardcoded directly
# into the Python source code.
#
# Example .env:
#
# OPENAI_API_KEY=your_api_key_here
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)


# ============================================================
# MODEL CONFIGURATION
# ============================================================

# Define the target LLM model.
#
# The value can be changed through the .env file.
#
# Example:
#
# MODEL_NAME=gpt-4.1-mini
#
# If MODEL_NAME is not defined, the application
# uses gpt-4.1-mini as the default model.
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gpt-4.1-mini"
)


# ============================================================
# MODEL PROVIDER CONFIGURATION
# ============================================================

# Define which LLM provider will be used by the
# jailbreak testing framework.
#
# Supported providers in the current architecture:
#
# mock   -> Local simulated LLM response
# openai -> OpenAI API
#
# Default:
# mock
#
# This is useful because the security testing framework
# can be developed without consuming API credits.
MODEL_PROVIDER = os.getenv(
    "MODEL_PROVIDER",
    "mock"
)


# ============================================================
# TEST EXECUTION CONFIGURATION
# ============================================================

# Define the maximum number of attack cases
# that can be executed during a test campaign.
#
# Example:
#
# MAX_TESTS=50
#
# If MAX_TESTS is not defined, the default value is 50.
#
# int() converts the environment variable from a string
# into a Python integer.
MAX_TESTS = int(
    os.getenv(
        "MAX_TESTS",
        "50"
    )
)