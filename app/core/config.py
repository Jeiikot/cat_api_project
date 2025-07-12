import os
from dotenv import load_dotenv


load_dotenv()

# External API
CAT_API_KEY = os.getenv("CAT_API_KEY", )
CAT_API_URL = os.getenv("CAT_API_URL", )

# Set up MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
DB_NAME = "catapi"

# Pagination settings
DEFAULT_PAGINATION_LIMIT = int(os.getenv("DEFAULT_PAGINATION_LIMIT", 20))
MAX_PAGINATION_LIMIT = int(os.getenv("MAX_PAGINATION_LIMIT", 100))