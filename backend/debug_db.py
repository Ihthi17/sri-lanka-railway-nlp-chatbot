from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM train_schedules")).scalar()
    print(f"Total schedules: {count}")
    
    sample = conn.execute(text("SELECT * FROM train_schedules LIMIT 5")).fetchall()
    print("Sample data:")
    for s in sample:
        print(s)
