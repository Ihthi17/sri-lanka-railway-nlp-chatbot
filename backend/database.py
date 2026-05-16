import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Railway provides DATABASE_URL or individual MYSQL variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Try to build it from individual variables if DATABASE_URL is not provided
    user = os.getenv("MYSQLUSER", "root")
    password = os.getenv("MYSQLPASSWORD", "")
    host = os.getenv("MYSQLHOST", "localhost")
    port = os.getenv("MYSQLPORT", "3306")
    database = os.getenv("MYSQLDATABASE", "train_chatbot")
    
    DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

# Handle cases where Railway might provide a mysql:// URL (SQLAlchemy needs mysql+pymysql://)
if DATABASE_URL and DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)


from sqlalchemy import text

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Test connection and set flag
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    DB_CONNECTED = True
    print("Database connected successfully")
except Exception as e:
    print(f"Database connection failed: {e}")
    DB_CONNECTED = False

