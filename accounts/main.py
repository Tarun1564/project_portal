import sqlite3

# 1. Connect to the database file
# If the file does not exist, it will be automatically created
database_file = 'db.sqlite3'
try:
    connection = sqlite3.connect(database_file)
    print(f"Connected to {database_file} successfully!")

    # 2. Create a cursor object
    # A cursor is used to execute SQL commands
    cursor = connection.cursor()

    # 3. Execute an SQL query (example: selecting data)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    # 4. Fetch the results
    tables = cursor.fetchall()

    if tables:
        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")
    else:
        print("No tables found in the database.")

    # 5. Close the connection
    connection.close()

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
