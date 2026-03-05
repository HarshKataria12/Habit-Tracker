import customtkinter as ctk
from tkinter import messagebox
from datetime import date, timedelta
import database
from habit import HabitTracker
import analytics # Requires your analytics.py file in the same folder

# Set the modern theme!
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HabitAppGUI:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("Habit Tracker - Pro Edition")
        self.root.geometry("1000x700")
        
        # Color Palette
        self.primary_color = "#4F46E5"
        self.success_color = "#22C55E"
        self.row_color = "#2A2A2A"
        self.header_color = "#333333"

        # --- Top Section: Input ---
        input_frame = ctk.CTkFrame(root, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=20)

        self.name_entry = ctk.CTkEntry(input_frame, placeholder_text="Habit Name...", width=160)
        self.name_entry.pack(side="left", padx=5)

        # UPDATED: More category options
        self.cat_combo = ctk.CTkComboBox(input_frame, values=[
            "💪 Fitness", "💼 Work", "💰 Finance", "🎨 Creative", "⚪ Other"
        ], width=120)
        self.cat_combo.set("💪 Fitness")
        self.cat_combo.pack(side="left", padx=5)

        # Smart Periodicity Dropdown
        self.period_combo = ctk.CTkComboBox(
            input_frame, 
            values=["Daily", "Weekly", "Custom"], 
            width=100, 
            command=self.update_goal_logic
        )
        self.period_combo.set("Daily")
        self.period_combo.pack(side="left", padx=5)

        # Smart Goal Entry (Locked by default)
        self.goal_entry = ctk.CTkEntry(input_frame, placeholder_text="Goal", width=60)
        self.goal_entry.insert(0, "7")
        self.goal_entry.configure(state="disabled", fg_color="#3d3d3d") 
        self.goal_entry.pack(side="left", padx=5)

        ctk.CTkButton(input_frame, text="+ Add", fg_color=self.primary_color, width=70, command=self.add_habit).pack(side="left", padx=5)
        
        # Analytics Button
        ctk.CTkButton(input_frame, text="📊 Analytics", fg_color="#6366F1", width=100, command=self.show_analytics).pack(side="left", padx=5)

        # --- The Grid Container ---
        self.grid_container = ctk.CTkScrollableFrame(root, fg_color="transparent")
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=5)

        self.refresh_ui()

    def update_goal_logic(self, selection):
        """Manages the automatic goal settings based on periodicity."""
        self.goal_entry.configure(state="normal")
        self.goal_entry.delete(0, 'end')
        if selection == "Daily":
            self.goal_entry.insert(0, "7")
            self.goal_entry.configure(state="disabled", fg_color="#3d3d3d")
        elif selection == "Weekly":
            self.goal_entry.insert(0, "1")
            self.goal_entry.configure(state="disabled", fg_color="#3d3d3d")
        elif selection == "Custom":
            self.goal_entry.configure(state="normal", fg_color="#1e1e1e")
            self.goal_entry.focus()
    def refresh_ui(self):
        """Rebuilds the grid with current-day only interaction and creation-date protection."""
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        # 1. NEW: Top Header for Current Date
        today = date.today()
        today_str = str(today)
        date_display = today.strftime("%A, %B %d, %Y")
        ctk.CTkLabel(self.grid_container, text=f"Today is {date_display}",
                     font=("Inter", 16, "bold"), text_color=self.primary_color).pack(pady=(0, 15))

        habits = self.manager.get_habits()
        
        # Grid automatically refreshes for the current week based on today's date
        monday = today - timedelta(days=today.weekday())
        week_dates = [str(monday + timedelta(days=i)) for i in range(7)]
        day_names = ["M", "T", "W", "T", "F", "S", "S"]

        # --- HEADER ROW ---
        header = ctk.CTkFrame(self.grid_container, fg_color=self.header_color, corner_radius=5)
        header.pack(fill="x", pady=2)
        ctk.CTkLabel(header, text="HABIT", width=200, anchor="w", font=("Inter", 12, "bold")).pack(side="left", padx=15)
        for day in day_names:
            ctk.CTkLabel(header, text=day, width=40, font=("Inter", 12, "bold")).pack(side="left", padx=2)
        ctk.CTkLabel(header, text="ACHIEVED", width=80, font=("Inter", 12, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(header, text="GOAL", width=60, font=("Inter", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="", width=40).pack(side="left", padx=5)

        # --- HABIT ROWS ---
        daily_totals = [0, 0, 0, 0, 0, 0, 0]
        for h in habits:
            completions = database.fetch_completions(self.manager.db, h.id)
            row = ctk.CTkFrame(self.grid_container, fg_color=self.row_color, corner_radius=5)
            row.pack(fill="x", pady=2)

            # 2. NEW: Name + Creation Date Mention
            name_container = ctk.CTkFrame(row, fg_color="transparent")
            name_container.pack(side="left", padx=15, pady=8)
            ctk.CTkLabel(name_container, text=f"{h.category} {h.name}", width=200, anchor="w", font=("Inter", 14)).pack(anchor="w")
            ctk.CTkLabel(name_container, text=f"Created: {h.creation_date}", font=("Inter", 10), text_color="gray").pack(anchor="w")

            achieved = 0
            for i, day_date in enumerate(week_dates):
                is_checked = day_date in completions
                if is_checked:
                    achieved += 1
                    daily_totals[i] += 1
                
                # 3. FEATURE: Logic for disabling non-current days
                is_today = (day_date == today_str)
                is_before_creation = (day_date < h.creation_date)
                
                # Only today is clickable; all other days are locked
                btn_state = "normal" if (is_today and not is_before_creation) else "disabled"
                
                btn_text = "✔" if is_checked else ""
                
                # Visual feedback for disabled vs active buttons
                if btn_state == "disabled":
                    btn_color = "#1B5E20" if is_checked else "#222222" # Dark green if done, dark gray if not
                    border_color = "#333333"
                else:
                    btn_color = self.success_color if is_checked else "transparent"
                    border_color = self.success_color if is_checked else "#52525B"

                btn = ctk.CTkButton(row, text=btn_text, width=40, height=30, corner_radius=4,
                                    fg_color=btn_color, border_width=2, 
                                    border_color=border_color,
                                    state=btn_state,
                                    command=lambda hi=h.id, dd=day_date, ic=is_checked: self.toggle_day(hi, dd, ic))
                btn.pack(side="left", padx=2)

            ctk.CTkLabel(row, text=str(achieved), width=80, font=("Inter", 14, "bold")).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=str(h.goal), width=60, font=("Inter", 14)).pack(side="left", padx=5)
            ctk.CTkButton(row, text="🗑️", width=40, height=30, fg_color="transparent", hover_color="#EF4444",
                          command=lambda hi=h.id: self.delete_habit(hi)).pack(side="left", padx=5)

        # --- TOTAL ROW ---
        if habits:
            total_row = ctk.CTkFrame(self.grid_container, fg_color="transparent")
            total_row.pack(fill="x", pady=10)
            ctk.CTkLabel(total_row, text="TOTAL", width=200, anchor="e", font=("Inter", 12, "bold"), text_color="gray").pack(side="left", padx=15)
            for total in daily_totals:
                ctk.CTkLabel(total_row, text=str(total), width=40, font=("Inter", 12, "bold"), text_color="gray").pack(side="left", padx=2)

    def toggle_day(self, habit_id, target_date, is_checked):
        if is_checked:
            cursor = self.manager.db.cursor()
            cursor.execute("DELETE FROM completions WHERE habit_id = ? AND completion_date = ?", (habit_id, target_date))
            self.manager.db.commit()
        else:
            self.manager.complete_habit(habit_id, target_date)
        self.refresh_ui()

    def add_habit(self):
        name = self.name_entry.get().strip()
        cat = self.cat_combo.get().split()[0]
        periodicity = self.period_combo.get()
        
        # Access goal even if field is disabled
        self.goal_entry.configure(state="normal")
        goal_val = self.goal_entry.get()
        self.update_goal_logic(periodicity)

        try:
            goal = int(goal_val)
            if not name: raise ValueError
            self.manager.add_habit(name, cat, periodicity, goal)
            self.name_entry.delete(0, 'end')
            self.refresh_ui()
        except:
            messagebox.showwarning("Input Error", "Please enter a name and valid goal.")

    def delete_habit(self, habit_id):
        if messagebox.askyesno("Confirm", "Delete habit?"):
            self.manager.delete_habit(habit_id)
            self.refresh_ui()

    def show_analytics(self):
        """Opens the dashboard using analytics.py logic."""
        habits = self.manager.get_habits()
        if not habits:
            messagebox.showinfo("Analytics", "No habits to analyze yet!")
            return

        habit_data = [(h, database.fetch_completions(self.manager.db, h.id)) for h in habits]
        
        top = ctk.CTkToplevel(self.root)
        top.title("Dashboard")
        top.geometry("400x500")
        top.attributes('-topmost', True)

        ctk.CTkLabel(top, text="📈 PERFORMANCE", font=("Inter", 20, "bold")).pack(pady=20)
        
        longest = analytics.get_longest_streak_overall(habit_data)
        ctk.CTkLabel(top, text=f"Best Overall Streak: {longest} days", font=("Inter", 14, "bold"), text_color=self.primary_color).pack(pady=5)

        scroll = ctk.CTkScrollableFrame(top, width=350, height=300)
        scroll.pack(padx=20, pady=10, fill="both", expand=True)

        for h, comps in habit_data:
            streak = analytics.calculate_streak(comps, h.periodicity)
            f = ctk.CTkFrame(scroll, fg_color="transparent")
            f.pack(fill="x", pady=5)
            ctk.CTkLabel(f, text=f"{h.category} {h.name}", font=("Inter", 13)).pack(side="left")
            ctk.CTkLabel(f, text=f"{streak} day streak", font=("Inter", 12, "italic"), text_color=self.success_color).pack(side="right")

if __name__ == "__main__":
    db_conn = database.connect_db()
    database.create_table(db_conn) 
    app = HabitAppGUI(ctk.CTk(), HabitTracker(db_conn))
    app.root.mainloop()
