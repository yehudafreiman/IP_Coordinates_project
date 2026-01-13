# Black Coordinates List

## תיאור המערכת
מערכת תשתיתית להמרת כתובות IP לנקודות ציון גאוגרפיות ואחסון הנתונים.

המערכת מורכבת משני שירותים:
- **Service A** - קליטת IP והמרה למיקום גאוגרפי
- **Service B** - אחסון ושליפה של נקודות ציון

## ארכיטקטורה
```
Client → Service A → Service B → Redis
         (Port 8000)  (Port 8001)
```

---

## Service A - IP Resolution Service

### אחריות
- קבלת כתובות IP
- המרת IP למיקום גאוגרפי באמצעות שירות חיצוני
- העברת הנתונים ל-Service B

### מבנה
```
service-a/
├── main.py          # אפליקציית FastAPI
├── routers.py       # נקודות קצה
├── services.py      # לוגיקת המרה
└── Dockerfile
```

### הרצה
```bash
# התקנת חבילות
pip install fastapi uvicorn requests

# הרצת השירות
python main.py
```
השירות רץ על פורט 8000.

### Endpoint
```
POST /
Body: "213.151.56.89"
```

---

## Service B - Coordinates Storage Service

### אחריות
- קבלת נקודות ציון מ-Service A
- אחסון הנתונים ב-Redis
- שליפת נתונים לפי IP

### מבנה
```
service-b/
├── main.py          # אפליקציית FastAPI
├── routers.py       # נקודות קצה
├── storage.py       # עבודה מול Redis
├── schemas.py       # מודלים (Pydantic)
├── Dockerfile
└── .env.example
```

### משתני סביבה
```
REDIS_HOST=localhost
REDIS_PORT=6379
```

### הרצה
```bash
# התקנת חבילות
pip install fastapi uvicorn redis

# הרצת השירות
python main.py
```
השירות רץ על פורט 8001.

### Endpoints

**שמירת נתונים**
```
POST /saveCoordinatesToRedis
Body: {
  "ip": "213.151.56.89",
  "lat": 31.7674,
  "lon": 35.2186
}
```

**שליפת נתונים**
```
GET /getCoordinates/{ip}
```

---

## הרצת המערכת המלאה

1. הפעל Redis
2. הפעל Service B על פורט 8001
3. הפעל Service A על פורט 8000
4. שלח בקשה ל-Service A עם IP

## עקרונות ארכיטקטוניים
- Service A לא שומר נתונים ולא ניגש ל-Redis
- Service B לא פונה לשירותים חיצוניים
- כל שירות אחראי על תחום מוגדר וברור
