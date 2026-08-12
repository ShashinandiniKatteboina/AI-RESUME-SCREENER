import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    MONGO_URI = os.getenv("MONGO_URI")

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")