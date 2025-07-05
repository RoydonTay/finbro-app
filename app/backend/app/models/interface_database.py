import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("POSTGRES_DB")

engine = create_engine(
    # connection string
    f"postgresql://{postgres_user}:{postgres_password}@localhost:5432/{postgres_db}"
)

with engine.connect() as conn:
    result = conn.execute(
        text(
            """
            SELECT * FROM users u, holdings h
            WHERE u.id = h.user_id;
            """
        )
    )

rows = result.fetchall()
for row in rows:
    # we can just get the row attributes accordingly
    print(row.user_id)
    print(type(row))
