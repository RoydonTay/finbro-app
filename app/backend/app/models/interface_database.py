from psycopg2 import connect

import os
from dotenv import load_dotenv

load_dotenv()

connection = connect(
    dbname=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host='localhost',
    port=5432
)

cursor = connection.cursor()

sql = '''
SELECT * FROM users;
'''

cursor.execute(sql)
results = cursor.fetchall()
print(results)
print(type(results[0]))