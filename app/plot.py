import csv
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path
from config import DATA_FOLDER
from app.scraper import USDRateScraper

CSV_FILE = Path(DATA_FOLDER) / "usd_rates.csv"

if not CSV_FILE.exists():
    print(f"CSV-файл {CSV_FILE} не найден. Запускаем скрейпер...")
    scraper = USDRateScraper()
    scraper.run()
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"После запуска скрейпера CSV {CSV_FILE} всё ещё отсутствует!")

dates, rates = [], []

with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            dates.append(datetime.fromisoformat(row["date"]))
            rates.append(float(row["rate"]))
        except (ValueError, KeyError):
            continue

if not dates:
    raise ValueError("Нет корректных данных для построения графика.")

dates, rates = zip(*sorted(zip(dates, rates)))

plt.figure(figsize=(12, 6))
plt.plot(dates, rates, marker="o", linestyle="-")
plt.title("Динамика курса USD/RUB")
plt.xlabel("Дата")
plt.ylabel("Курс")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


