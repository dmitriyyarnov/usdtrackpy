## USDTrackPy
Проект для сбора курса USD/RUB с сайта ЦБ РФ, хранения истории в CSV, предоставления API через FastAPI и построения графиков динамики курса.
### **Что делает проект**
1. Сбор курса USD (скрапинг) 
   - Скрейпер автоматически собирает курс USD с сайта ЦБ РФ и сохраняет его в CSV (data/usd_rates.csv). https://github.com/dmitriyyarnov/usdtrackpy/tree/dev/data

2. Анализ и визуализация
   - Автоматически запускается скрейпер, если CSV отсутствует.
   - График строится по данным CSV (data/usd_rates.csv): https://github.com/dmitriyyarnov/usdtrackpy/blob/dev/rate.png
3. API для получения исторических курсов USD из CSV-файлов (data/).
   - Параметры: limit (1–100, по умолчанию 10), sort (asc/desc, по умолчанию desc).

### Установка зависимостей
    pip install -r requirements.txt

### Сбор первого курса USD
    python -m app.main

### Построение графика
    python -m app.plot

### Запуск FastAPI:  
     
    uvicorn app.main:app --reload
Эндпоинт: `GET /rates`  
Параметры: limit (по умолчанию 10) — количество записей; sort (asc/desc, по умолчанию desc) — сортировка по дате 
Пример запросов: 'http://127.0.0.1:8000/rates', 'GET http://127.0.0.1:8000/rates?limit=5&sort=asc'
<img width="782" height="152" alt="image" src="https://github.com/user-attachments/assets/d26e8d66-edd9-4835-a68e-84e24ec2433f" />


Swagger UI: 'http://127.0.0.1:8000/docs'

Этот проект распространяется под лицензией MIT.
Подробности см. в файле [LICENSE](./LICENSE).
