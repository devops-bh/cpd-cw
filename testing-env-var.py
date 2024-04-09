from dotenv import load_dotenv
import os

load_dotenv()
print(os.environ['AWS_SESSION_TOKEN'])