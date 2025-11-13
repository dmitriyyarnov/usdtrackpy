import os
import json
import matplotlib.pyplot as plt
from config import DATA_FOLDER
if not os.path.exists(DATA_FOLDER):
    raise FileNotFoundError("Папка 'data' не найдена! Запустите скрапер хотя бы один раз.")

files = sorted([f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")])

if not files:
    raise FileNotFoundError("Нет JSON-файлов в папке 'data'!")

dates, rates = [], []
for file in files:
    file_path = os.path.join(DATA_FOLDER, file)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        dates.append(data["date"])
        rates.append(data["rate"])

plt.plot(dates, rates, marker="o")
plt.xticks(rotation=45)
plt.title("USD курс ЦБРФ")
plt.xlabel("Дата")
plt.ylabel("Курс")
plt.grid(True)
plt.tight_layout()
plt.show()

