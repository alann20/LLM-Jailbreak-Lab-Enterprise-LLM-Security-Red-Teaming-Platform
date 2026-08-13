import os
from dotenv import load_dotenv


# Project root directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# .env absolute path
ENV_FILE = os.path.join(
    BASE_DIR,
    ".env"
)


# Load environment variables
load_dotenv(ENV_FILE)


# OpenAI configuration
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)


# LLM configuration
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gpt-4.1-mini"
)


# Provider configuration
MODEL_PROVIDER = os.getenv(
    "MODEL_PROVIDER",
    "mock"
)


# Test configuration
MAX_TESTS = int(
    os.getenv(
        "MAX_TESTS",
        "50"
    )
)