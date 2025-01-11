from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    COSMOS_URI = os.getenv("COSMOS_URI")
    COSMOS_KEY = os.getenv("COSMOS_KEY")
    COSMOS_DB_NAME = os.getenv("COSMOS_DB_NAME")
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")