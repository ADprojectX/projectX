import psycopg2
from dotenv import load_dotenv
import os

def refresh_env(key):
    load_dotenv(override=True)
    return os.getenv(key)

def find_pending_task(prompt):
    connection = psycopg2.connect(
        host=refresh_env('AWS_RDS_HOST'), user=refresh_env('AWS_RDS_USER'), password=refresh_env('AWS_RDS_KEY'), database=refresh_env('AWS_RDS_DB')
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM videogenerator_pendingtask WHERE prompt=%s", (prompt,))
    row = cursor.fetchone()
    connection.close()
    if row:
        _, prompt, image_folder, _ = row
        return image_folder
    else:
        return None

def delete_pending_task(prompt):
    connection = psycopg2.connect(
        host=refresh_env('AWS_RDS_HOST'), user=refresh_env('AWS_RDS_USER'), password=refresh_env('AWS_RDS_KEY'), database=refresh_env('AWS_RDS_DB')
    )
    cursor = connection.cursor()
    cursor.execute("DELETE FROM videogenerator_pendingtask WHERE prompt=%s", (prompt,))
    connection.commit()
    connection.close()

# db_host = os.getenv("DB_host")
# db_user = os.getenv("DB_user")
# db_pwd = os.getenv("DB_password")
# db_database = os.getenv("DB_database")

# # Example usage:
# prompt_to_find = "YourPromptHere"

# # Find and return entry
# image_folder = find_pending_task(prompt_to_find)
# if image_folder:
#     print(f"Found entry, Image folder: {image_folder}")
# else:
#     print("No entry found for the prompt.")

# # Delete entry permanently
# delete_pending_task(prompt_to_find)
# print("Entry deleted permanently.")

# prompt = 'a brain with gears turning inside'
# remove_pending_tasks(prompt)

# data = cursor.fetchall()
# connection.close()


# def add_pending_tasks(prompt, image_folder):
#     cursor.execute(
#         """CREATE TABLE IF NOT EXISTS pending_tasks (prompt text, image_folder text)"""
#     )
#     cursor.execute(
#         "INSERT INTO pending_tasks (prompt, image_folder) VALUES (%s, %s)",
#         (prompt, image_folder),
#     )
# def remove_pending_tasks(prompt):
#     connection = psycopg2.connect(
#     host=db_host, user=db_user, password=db_pwd, database=db_database
#     )
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM videogenerator_pendingtask WHERE prompt=%s", (prompt,))
#     rows = cursor.fetchall()
#     if rows:
#         for row in rows:
#             _, prompt, image_folder, _ = row
#         # Delete entry based on prompt
#         cursor.execute("DELETE FROM videogenerator_pendingtask WHERE prompt=%s", (prompt,))
#         connection.commit()
#         return image_folder
#     else:
#         return None
#     connection.commit()