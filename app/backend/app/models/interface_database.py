from psycopg2 import connect

from sqlalchemy import create_engine, text

import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    # connection string
    f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/{os.getenv("POSTGRES_DB")}"
)

with engine.connect() as conn:
    result = conn.execute(
        text(
            '''
            SELECT * FROM users u, holdings h
            WHERE u.id = h.user_id; 
            '''
        )
    )

rows = result.fetchall()
for row in rows:
    # we can just get the row attributes accordingly
    print(row.user_id)
    print(type(row))