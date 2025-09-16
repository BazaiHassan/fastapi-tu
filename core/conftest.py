from dotenv import load_dotenv
from pathlib import Path

# Load .env.test BEFORE anything else imports Settings()
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env.test")