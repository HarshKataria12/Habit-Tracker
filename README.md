# 📈 Habit Tracker - Pro Edition (HabitFlow)

A sleek, locally hosted desktop application designed to help you build and maintain healthy routines. Built entirely in Python, this project features a modern Graphical User Interface (GUI) and combines **Object-Oriented Programming (OOP)** for core data structures with **Functional Programming** for lightning-fast analytics.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-success)
![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey)

---

## ✨ Features

* **Modern Interface:** A responsive, dark-mode desktop aesthetic built with `customtkinter`.
* **Interactive 7-Day Dashboard:** A dynamic, rolling calendar grid that updates natively based on today's date. Check off tasks with a single click.
* **Smart Categorization & Periodicity:** Organize habits with tags/emojis and set strict tracking periods (Daily or Weekly).
* **Deep Analytics Engine:** Utilizing pure functional programming techniques (`map`, `filter`) to instantly calculate your highest consecutive run streaks overall and for specific habits.
* **100% Private & Secure:** Powered by a serverless SQLite database. Your personal habits and completion timestamps are stored securely on your local machine.
* **Automated Housekeeping:** Deleting a habit automatically triggers SQL `CASCADE` deletion to clean up associated historical check-ins and save space.

---

## 🛠️ Tech Stack

* **Language:** Python 3.7+
* **UI Framework:** CustomTkinter
* **Database:** SQLite3 (Built-in)
* **Testing:** Pytest / Unittest

---

## 📁 Project Structure

```text
habit_tracker/
├── main.py            # Entry point & CustomTkinter UI logic
├── habit.py           # OOP models (Habit class & HabitManager)
├── database.py        # SQLite database connection & queries
├── analytics.py       # Functional programming streak calculations
├── test_fixtures.py   # Script to load 5 predefined habits & 4 weeks of data
├── tests/             # Pytest suite for core logic
│   └── test_logic.py
├── requirements.txt   # Project dependencies
└── README.md          # Setup & Usage instructions
