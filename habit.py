import database
from datetime import date

class Habit:
    def __init__(self,id,name,category, periodicity, creation_date=None,goal=0):
        self.id = id
        self.name = name
        self.category = category
        self.periodicity = periodicity
        self.creation_date = creation_date or date.today().isoformat()  # Default to today's date if not provided
        self.goal = goal
    def __str__(self):
        return f"Habit(id={self.id}, name='{self.name}', category='{self.category}', periodicity='{self.periodicity}', creation_date='{self.creation_date}', goal={self.goal})"
class HabitTracker:
    # This class manages the habits and their completions, interfacing with the database.
    def __init__(self, db):
        self.db = db
    def add_habit(self, name, category, periodicity,goal):
        # Add a new habit to the database and return its ID
        habit_id = database.insert_habit(self.db, name, category, periodicity, date.today().isoformat(), goal)
        return habit_id
    # We add completion_date=None so it can accept a specific date from the grid!
    def complete_habit(self, habit_id, completion_date=None):
        date_to_save = completion_date or date.today().isoformat()
        database.insert_completion(self.db, habit_id, date_to_save)
        print(f"Habit with ID {habit_id} marked as completed for {date_to_save}.")
    def delete_habit(self, habit_id):
        # Delete a habit from the database
        database.delete_habit(self.db, habit_id)
    def get_habits(self):
        # Fetch all habits from the database and return them as Habit objects
        habit_rows = database.fetch_habits(self.db)
        habits = []
        for row in habit_rows:
            habit_id, name, category, periodicity, creation_date,goal = row
            habits.append(Habit(habit_id, name, category, periodicity, creation_date, goal))
        return habits
    
# --- Testing Block ---
# --- Testing Block ---
if __name__ == "__main__":
    db_conn = database.connect_db()
    database.create_table(db_conn) # Ensure table exists for the test
    
    manager = HabitTracker(db_conn)
    
    print("\n--- Testing HabitTracker ---")
    
    # 5. Updated the test to include the Category emoji and the Goal number (7)
    new_id = manager.add_habit("Meditate", "🟣 Mind", "Daily", 7)
    
    manager.complete_habit(new_id)
    
    print("\n--- All Current Habits ---")
    habits_list = manager.get_habits()
    for h in habits_list:
        print(h) 
    
    print("\n")