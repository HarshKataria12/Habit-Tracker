import unittest
import sqlite3
from datetime import date, timedelta

# Import your actual project files
import database
from habit import HabitTracker
import analytics

class TestHabitApp(unittest.TestCase):
    
    def setUp(self):
        """
        This runs BEFORE every single test.
        We use ':memory:' to create a temporary database in RAM. 
        This is a pro-move: it tests the database logic without deleting or messing up your real 'my_database.db'!
        """
        self.db = sqlite3.connect(':memory:')
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON;")
        database.create_table(self.db)
        self.manager = HabitTracker(self.db)

    def tearDown(self):
        """This runs AFTER every test to clean up."""
        self.db.close()

    # --- 1. Testing Database & Habit Manager ---
    
    def test_add_and_retrieve_habit(self):
        """Tests if a habit can be inserted and fetched correctly."""
        # Add a habit
        habit_id = self.manager.add_habit("Read a Book", "🟣 Study", "Daily", 7)
        self.assertIsNotNone(habit_id, "Habit ID should not be None")

        # Fetch it back
        habits = self.manager.get_habits()
        self.assertEqual(len(habits), 1, "There should be exactly 1 habit in the database")
        self.assertEqual(habits[0].name, "Read a Book")
        self.assertEqual(habits[0].goal, 7)
        self.assertEqual(habits[0].periodicity, "Daily")

    def test_complete_habit(self):
        """Tests logging a completion day."""
        habit_id = self.manager.add_habit("Go to Gym", "💪 Fitness", "Weekly", 3)
        test_date = date.today().isoformat()
        
        # Mark it complete
        self.manager.complete_habit(habit_id, test_date)
        
        # Verify in database
        completions = database.fetch_completions(self.db, habit_id)
        self.assertIn(test_date, completions, "The completion date was not saved to the database")
        self.assertEqual(len(completions), 1)

    def test_cascade_delete(self):
        """Tests if deleting a habit also wipes its completion history (housekeeping!)."""
        habit_id = self.manager.add_habit("Drink Water", "Health", "Daily", 7)
        self.manager.complete_habit(habit_id, date.today().isoformat())
        
        # Delete the habit
        self.manager.delete_habit(habit_id)
        
        # Check that completions are gone too
        completions = database.fetch_completions(self.db, habit_id)
        self.assertEqual(len(completions), 0, "CASCADE delete failed; completions were left behind")

    # --- 2. Testing Pure Functional Analytics ---
    
    def test_daily_streak_math(self):
        """Verifies the pure functional streak calculator."""
        today = date.today()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        
        # Mocking 3 consecutive days leading up to today
        mock_dates = [two_days_ago.isoformat(), yesterday.isoformat(), today.isoformat()]
        
        streak = analytics.calculate_streak(mock_dates, "Daily")
        self.assertEqual(streak, 3, "The streak calculator did not count 3 consecutive days correctly")

    def test_broken_streak(self):
        """Verifies that a missed day resets the active streak."""
        today = date.today()
        # Skipped yesterday! Gap is too large.
        three_days_ago = today - timedelta(days=3)
        two_days_ago = today - timedelta(days=2)
        
        mock_dates = [three_days_ago.isoformat(), two_days_ago.isoformat()]
        
        streak = analytics.calculate_streak(mock_dates, "Daily")
        self.assertEqual(streak, 0, "The streak should be 0 because yesterday was missed")

if __name__ == '__main__':
    unittest.main(verbosity=2)
