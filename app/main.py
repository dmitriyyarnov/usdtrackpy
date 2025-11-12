from fastapi import FastAPI, Query, HTTPException
from pathlib import Path
import csv
from datetime import datetime
from app.scraper import USDRateScraper
from config import DATA_FOLDER

CSV_FILE = Path(DATA_FOLDER) / "usd_rates.csv"

app = FastAPI(title="USD Rates API")

scraper = USDRateScraper()
scraper.run()

@app.get("/rates")
def get_rates(limit: int = Query(10, ge=1, le=100),
              sort: str = Query("desc", regex="^(asc|desc)$")):
    if not CSV_FILE.exists():
        raise HTTPException(status_code=404, detail="Нет данных")

    rates = []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rates.append({
                    "date": row["date"],
                    "rate": float(row["rate"]),
                    "currency": row["currency"],
                    "source": row["source"],
                    "updated_at": row["updated_at"]
                })
            except (ValueError, KeyError):
                continue

    if not rates:
        raise HTTPException(status_code=404, detail="Нет корректных данных")

    rates.sort(key=lambda x: datetime.fromisoformat(x["date"]), reverse=(sort == "desc"))

    return rates[:limit]




