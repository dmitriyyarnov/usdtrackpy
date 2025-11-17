import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from pathlib import Path
from config import DATA_FOLDER


class USDRateScraper:

    def __init__(self, data_folder: str = DATA_FOLDER):
        self.data_folder = Path(data_folder)
        self.url = "https://www.cbr.ru/scripts/XML_daily.asp"
        self.session = requests.Session()

    def fetch_usd_rate(self):
        try:
            response = self.session.get(self.url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")

            val_curs = soup.find("ValCurs")
            if not val_curs or not val_curs.get("Date"):
                raise ValueError("Не удалось получить дату из ответа ЦБ")

            date_str = val_curs["Date"]
            date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
            iso_date = date_obj.isoformat()

            usd = soup.find("Valute", ID="R01235")
            if not usd:
                raise ValueError("Курс USD не найден в ответе ЦБ")

            raw_value = usd.Value.text.replace(",", ".")
            rate = float(raw_value)

            return iso_date, rate

        except Exception as e:
            print(f"Ошибка при получении курса: {e}")
            raise

    def save_rate(self, date_str: str, rate: float):
        try:
            self.data_folder.mkdir(parents=True, exist_ok=True)
            file_path = self.data_folder / f"{date_str}.json"

            data = {
                "date": date_str,
                "rate": rate,
                "currency": "USD/RUB",
                "source": "cbr.ru",
                "updated_at": datetime.now().isoformat()
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return file_path

        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            raise

    def run(self):
        date_str, rate = self.fetch_usd_rate()
        self.save_rate(date_str, rate)
        return date_str, rate


def run_scraper():
    try:
        scraper = USDRateScraper()
        date_str, rate = scraper.run()
        print(f"Курс USD успешно сохранён: {rate} RUB на {date_str}")

    except Exception as e:
        print(f"Не удалось выполнить скрейпер: {e}")


if __name__ == "__main__":
    run_scraper()



