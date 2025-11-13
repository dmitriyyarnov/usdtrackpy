from fastapi import FastAPI, Query, HTTPException
import os
import json

DATA_FOLDER = "data"

app = FastAPI(title="USD Rates API")

@app.get("/rates")
def get_rates(
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query("desc", pattern="^(asc|desc)$")
):
    if not os.path.exists(DATA_FOLDER) or len(os.listdir(DATA_FOLDER)) == 0:
        raise HTTPException(status_code=404, detail="Нет доступных данных о курсах")

    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]

    files = sorted(
        files,
        key=lambda f: os.path.getmtime(os.path.join(DATA_FOLDER, f)),
        reverse=(sort == "desc")
    )

    files = files[:limit]

    result = []
    for file in files:
        path = os.path.join(DATA_FOLDER, file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                result.append(json.load(f))
        except json.JSONDecodeError:
            continue

    return result



