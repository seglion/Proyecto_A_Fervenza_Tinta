import pytest
from dotenv import load_dotenv
from pathlib import Path
import os
import asyncio

@pytest.fixture(scope="session", autouse=True)
def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env.dev"
    load_dotenv(dotenv_path=env_path)
    # Ensure SENDGRID_API_KEY is set for tests
    if "SENDGRID_API_KEY" not in os.environ:
        os.environ["SENDGRID_API_KEY"] = "SG.test_sendgrid_api_key"


