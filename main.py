import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime

# --- 1. KONFIGURACJA BAZY DANYCH ---
conn = sqlite3.connect("habits.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_log (
    date TEXT PRIMARY KEY,
    water_ok INTEGER,
    training_ok INTEGER,
    steps_ok INTEGER,
    sleep_ok INTEGER
)
""")
conn.commit()

# --- 2. FUNKCJE POMOCNICZE ---

def ask_yes_no(question_text):
    """Pyta użytkownika t/n i zwraca 1 (tak) lub 0 (nie)."""
    while True:
        answer = input(question_text).lower()
        if answer == 't': return 1
        if answer == 'n': return 0
        print("❌ Wpisz 't' lub 'n'.")

def add_entry():
    """Dodaje nowy dzień do Twojego trackera."""
    today_date = date.today().isoformat()
    
    while True:
        user_date = input(f"Data [Enter = dziś {today_date}]: ")
        if user_date == "":
            user_date = today_date
            break
        try:
            # Sprawdzamy czy format daty jest poprawny
            datetime.strptime(user_date, '%Y-%m-%d')
            break
        except ValueError:
            print("❌ Błąd! Użyj formatu RRRR-MM-DD (np. 2026-02-03).")

    water = ask_yes_no("Czy wypity limit wody? (t/n): ")
    training = ask_yes_no("Czy był trening? (t/n): ")
    steps = ask_yes_no("Czy był cel kroków? (t/n): ")
    sleep = ask_yes_no("Czy sen trwał min. 7h? (t/n): ")

    cursor.execute("""
        INSERT OR REPLACE INTO daily_log VALUES (?, ?, ?, ?, ?)
    """, (user_date, water, training, steps, sleep))
    conn.commit()
    print("✅ Zapisano pomyślnie!\n")

def show_entries():
    """Wyświetla listę wszystkich wpisów w terminalu."""
    cursor.execute("SELECT * FROM daily_log ORDER BY date DESC")
    rows = cursor.fetchall()
    
    if not rows:
        print("📭 Baza danych jest pusta.\n")
        return

    print("\nDATA       | WODA | TREN | KROK | SEN")
    print("-" * 37)
    for r in rows:
        # Formatowanie f-string wyrównuje kolumny
        print(f"{r[0]:10} |  {r[1]}   |  {r[2]}   |  {r[3]}   |  {r[4]}")
    print("")

def analyze_habits():
    """Analizuje postępy i rysuje wykres."""
    df = pd.read_sql_query("SELECT * FROM daily_log ORDER BY date", conn)

    if df.empty:
        print("❌ Brak danych do analizy.\n")
        return

    # Przygotowanie dat dla biblioteki Pandas
    df['date'] = pd.to_datetime(df['date'])

    # --- CZĘŚĆ 1: STATYSTYKI TEKSTOWE ---
    print("\n--- TWOJE OSIĄGNIĘCIA ---")
    habit_columns = ['water_ok', 'training_ok', 'steps_ok', 'sleep_ok']
    display_names = ['Woda', 'Trening', 'Kroki', 'Sen']

    for i in range(len(habit_columns)):
        col = habit_columns[i]
        name = display_names[i]
        
        count = df[col].sum() # Liczy ile razy wystąpiła 1
        percentage = (count / len(df)) * 100
        print(f"{name:10}: {int(count)} dni ({percentage:.0f}%)")

    # --- CZĘŚĆ 2: WYKRES ---
    plt.figure(figsize=(10, 5))
    colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B']

    for i in range(len(habit_columns)):
        col = habit_columns[i]
        # Wybieramy tylko dni z sukcesem (1)
        subset = df[df[col] == 1]
        plt.scatter(subset['date'], [i] * len(subset), 
                    color=colors[i], s=250, marker='s', label=display_names[i])

    # Ustawienia osi
    plt.yticks(range(4), display_names)
    plt.xticks(df['date'], df['date'].dt.strftime('%Y-%m-%d'), rotation=45)
    
    plt.title("Mój Habit Tracker - Aktywność w czasie", pad=20)
    plt.grid(True, axis='x', linestyle=':', alpha=0.4)
    plt.tight_layout()
    
    print("📊 Otwieram wykres...")
    plt.show()


# --- 3. MENU GŁÓWNE ---
while True:
    print("\n--- MONITOR NAWYKÓW ---")
    print("1 - Dodaj wpis")
    print("2 - Pokaż listę wpisów")
    print("3 - Analiza i Wykres")
    print("0 - Wyjście")

    choice = input("Wybierz opcję: ")

    if choice == "1":
        add_entry()
    elif choice == "2":
        show_entries()
    elif choice == "3":
        analyze_habits()
    elif choice == "0":
        print("Do zobaczenia!")
        break
    else:
        print("⚠️ Nieznana opcja, spróbuj ponownie.")

conn.close()