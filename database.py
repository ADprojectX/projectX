import pymysql
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)
db_host = os.getenv("DB_host")
db_user = os.getenv("DB_user")
db_pwd = os.getenv("DB_password")
db_database = os.getenv("DB_database")

connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_pwd,
    database=db_database
)
cursor = connection.cursor()

def add_pending_tasks(prompt, image_folder):
    cursor.execute('''CREATE TABLE IF NOT EXISTS pending_tasks (prompt text, image_folder text)''')
    cursor.execute("INSERT INTO pending_tasks (prompt, image_folder) VALUES (%s, %s)", (prompt, image_folder))
    connection.commit()

def remove_pending_tasks(prompt):
    cursor.execute("SELECT * FROM pending_tasks WHERE prompt=%s", (prompt,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            prompt, image_folder = row
        # Delete entry based on prompt
        cursor.execute("DELETE FROM pending_tasks WHERE prompt=%s", (prompt,))
        connection.commit()
        return image_folder
    else:
        return None

# data = cursor.fetchall()
# connection.close()
