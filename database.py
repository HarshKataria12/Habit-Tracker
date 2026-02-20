import sqlite3
# establish a connection to the SQLite database
def connect_db(db_name="my_database.db"):
    # connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # enable accessing columns by name
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_table(conn):
    # Creates the 'habits' and 'completions' tables if they don't already exist.
    cursor = conn.cursor()
    
    # CORRECTED: Create a habits table in the database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            creation_date TEXT NOT NULL,
            goal INTEGER NOT NULL
        )
    ''')
    
    # Create a completions table in the database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completion_date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()

# insert a new habit into the habit table
def insert_habit(db, name, category, periodicity, creation_date, goal):
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO habits (name, category, periodicity, creation_date, goal)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, category, periodicity, creation_date, goal))
    db.commit()
    return cursor.lastrowid  # Return the ID of the newly inserted habit
def insert_completion(db, habit_id, completion_date):
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO completions (habit_id, completion_date)
        VALUES (?, ?)
    ''', (habit_id, completion_date))
    db.commit()
# fetch all habits from the habit table
def fetch_habits(db):    
    cursor = db.cursor()
    cursor.execute('SELECT * FROM habits')
    return cursor.fetchall()  # Return all habits as a list of rows
def fetch_completions(db, habit_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM completions WHERE habit_id = ?', (habit_id,))
    return [row['completion_date'] for row in cursor.fetchall()] # Return a list of completion dates for the specified habit
def delete_habit(db, habit_id):
    """
    Deletes a habit from the database. 
    Because of ON DELETE CASCADE, all its completions will also be deleted automatically.
    """
    cursor = db.cursor()
    cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    db.commit()
if __name__ == "__main__":
   
    db = connect_db()
    create_table(db)
    
    print("\n--- 🟢 Testing Insert ---")
    h1_id = insert_habit(db, "Read a Book", "🔵 Study", "Daily", "2024-06-01", 7)
    h2_id = insert_habit(db, "Go to Gym", "🟢 Health", "Weekly", "2024-06-01", 3)
    
    insert_completion(db, h1_id, "2024-06-02")
    insert_completion(db, h1_id, "2024-06-03")
    insert_completion(db, h2_id, "2024-06-05")

    habits = fetch_habits(db)

    print("\n" + "="*80)
    print(f"{'ID':<5} | {'NAME':<15} | {'CATEGORY':<10} | {'PERIOD':<8} | {'CREATED':<12} | {'GOAL'}")
    print("-" * 80)
    
    # Because you are using sqlite3.Row, we access by index or column name
    for h in habits:
        print(f"{h['id']:<5} | {h['name']:<15} | {h['category']:<10} | {h['periodicity']:<8} | {h['creation_date']:<12} | {h['goal']}")
        
    print("="*80)