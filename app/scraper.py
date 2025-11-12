import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import csv
from config import DATA_FOLDER

class USDRateScraper:

    def __init__(self, data_folder: Path = DATA_FOLDER):
        self.data_folder = Path(data_folder)
        self.url = "https://www.cbr.ru/scripts/XML_daily.asp"
        self.session = requests.Session()
        self.csv_file = self.data_folder / "usd_rates.csv"

    def fetch_usd_rate(self):
        try:
            response = self.session.get(self.url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "xml")

            date_str = soup.find("ValCurs")["Date"]
            iso_date = datetime.strptime(date_str, "%d.%m.%Y").date().isoformat()

            usd = soup.find("Valute", ID="R01235")
            if not usd:
                raise ValueError("USD курс не найден")

            rate = float(usd.Value.text.replace(",", "."))
            return iso_date, rate

        except Exception as e:
            print(f"Ошибка fetch_usd_rate: {e}")
            return None, None

    def save_rate_to_csv(self, date_str: str, rate: float):
        self.data_folder.mkdir(parents=True, exist_ok=True)
        file_exists = self.csv_file.exists()

        if file_exists:
            with open(self.csv_file, newline="", encoding="utf-8") as f:
                existing_dates = {row["date"] for row in csv.DictReader(f)}
            if date_str in existing_dates:
                print(f"Курс за {date_str} уже сохранён")
                return self.csv_file

        with open(self.csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "rate", "currency", "source", "updated_at"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "date": date_str,
                "rate": rate,
                "currency": "USD/RUB",
                "source": "cbr.ru",
                "updated_at": datetime.now().isoformat()
            })
        return self.csv_file

    def run(self):
        date_str, rate = self.fetch_usd_rate()
        if date_str and rate is not None:
            return self.save_rate_to_csv(date_str, rate)
        return None


