import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the apiKey value
apiKey = os.getenv("apiKey")

# Print the apiKey value
print(apiKey)