from dotenv import load_dotenv
import os

load_dotenv()

name_db = os.getenv("POSTGRES_DB")
username = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("DB_HOST")
