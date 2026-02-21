from datetime import datetime

# --- 1. Return a list of all currently tracked habits ---
def get_all_tracked_habits(habits_list):
    """Simply returns the list of habits (useful for pure functional flow)."""
    return habits_list

# --- 2. Return a list of all habits with the same periodicity ---
def filter_by_periodicity(habits_list, periodicity):
    """
    Uses the functional 'filter' tool to find habits that match the given periodicity.
    """
    return list(filter(lambda h: h.periodicity.lower() == periodicity.lower(), habits_list))

# --- 3. Return the longest run streak for a given habit ---
def calculate_streak(completion_dates, periodicity):
    """Calculates the current active streak based on consecutive completions."""
    if not completion_dates:
        return 0

    # Sort unique dates
    dates = sorted(list(set([datetime.strptime(d, "%Y-%m-%d").date() for d in completion_dates])))
    today = datetime.now().date()
    
    # If the last completion was more than 1 day ago, the current active streak is 0
    if (today - dates[-1]).days > 1:
        return 0

    streak = 1
    # Check backwards from the most recent date
    for i in range(len(dates) - 1, 0, -1):
        if (dates[i] - dates[i-1]).days == 1:
            streak += 1
        else:
            break # Streak broken by a gap
            
    return streak
# --- 4. Return the longest run streak of all defined habits ---
def get_longest_streak_overall(habits_with_completions):
    """
    Takes a list of tuples/lists containing (Habit_Object, [list_of_dates]).
    Uses functional 'map' to calculate streaks for all of them and returns the highest.
    """
    if not habits_with_completions:
        return 0
        
    # Map applies the calculate_streak function to every item in the list automatically
    all_streaks = list(map(lambda item: calculate_streak(item[1], item[0].periodicity), habits_with_completions))
    
    # Return the maximum streak found
    return max(all_streaks)


# --- Quick Test Block ---
if __name__ == "__main__":
    # We don't need the database to test functional programming! 
    # We just pass in raw data to see if the math works.
    print("\n--- Testing Daily Streak ---")
    daily_dates = ["2024-06-01", "2024-06-02", "2024-06-03", "2024-06-05"] # Missed the 4th!
    daily_streak = calculate_streak(daily_dates, "daily")
    print(f"Dates: {daily_dates}")
    print(f"Longest Daily Streak: {daily_streak} (Should be 3)")

    print("\n--- Testing Weekly Streak ---")
    weekly_dates = ["2024-06-05", "2024-06-12", "2024-06-26"] # Missed the week of the 19th!
    weekly_streak = calculate_streak(weekly_dates, "weekly")
    print(f"Dates: {weekly_dates}")
    print(f"Longest Weekly Streak: {weekly_streak} (Should be 2)")
    print("\n")