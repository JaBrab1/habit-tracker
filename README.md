# Habit Tracker

A simple command-line application written in Python to track four daily habits: drinking enough water, exercising, reaching a step goal, and sleeping for at least seven hours.

The application stores entries in a local SQLite database, uses Pandas to calculate completion statistics, and visualizes successful days with Matplotlib.

## Features

- Add an entry for today or a selected date (`YYYY-MM-DD`).
- Answer four yes/no questions (`t` for yes, `n` for no; the program prompts are in Polish).
- Save and update daily records in an SQLite database (`habits.db`).
- Display recorded entries in reverse chronological order.
- Calculate the number and percentage of recorded days on which each habit was completed.
- View a chart marking successful days for each habit.

**Note:** Saving another entry for the same date replaces the previous one. Completion percentages are calculated using the days recorded in the database, not every calendar day.

## Technologies

- Python 3
- SQLite (Python's built-in `sqlite3` module)
- Pandas
- Matplotlib

## Getting started

1. Clone the repository and open its directory:

   ```bash
   git clone https://github.com/YOUR_USERNAME/habit-tracker.git
   cd habit-tracker
   ```

   Replace `YOUR_USERNAME` with your GitHub username. Alternatively, download the repository as a ZIP file.

2. (Optional but recommended) Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Activate it on Windows (PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Or on macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

The repository includes `habits.db` with existing entries so you can explore the history and chart immediately. If the database file is missing, the application creates a new, empty database automatically.

## Menu

The current application interface is in Polish:

```text
--- MONITOR NAWYKÓW ---
1 - Dodaj wpis
2 - Pokaż listę wpisów
3 - Analiza i Wykres
0 - Wyjście
```

## Project structure

```text
habit-tracker/
├── main.py
├── habits.db
├── README.md
├── requirements.txt
└── .gitignore
```

`habits.db` contains the initial records. SQLite-generated temporary files are excluded via `.gitignore`.

## Current limitations

- The application uses a command-line interface and requires interactive input.
- Each habit is recorded as either completed (`1`) or not completed (`0`).
- The chart shows successful days only; date labels may become crowded as the number of entries grows.
- The user-facing prompts and menu are currently in Polish.
