# Black Coordinates List

## תיאור המערכת
מערכת תשתיתית להמרת כתובות IP לנקודות ציון גאוגרפיות ואחסון הנתונים.

המערכת מורכבת משני שירותים עצמאיים:
- **Service A** - קליטת IP והמרה למיקום גאוגרפי
- **Service B** - אחסון ושליפה של נקודות ציון

## ארכיטקטורה
```
Client → Service A → ip-api.com (שירות חיצוני)
           ↓
       Service B → Redis
```

**זרימת מידע:**
1. לקוח שולח כתובת IP ל-Service A
2. Service A ממיר את ה-IP למיקום גאוגרפי באמצעות שירות חיצוני
3. Service A שולח את הנתונים ל-Service B
4. Service B שומר את הנתונים ב-Redis
5. Service B מחזיר אישור שמירה
6. Service A מחזיר את התשובה ללקוח

---

## מבנה הפרויקט
```
IP_Coordinates_project/
├── README.md
├── docker-compose.yml
├── service-a/
│   ├── app/
│   │   ├── main.py          # אפליקציית FastAPI
│   │   ├── routers.py       # נקודות קצה
│   │   ├── services.py      # לוגיקת המרה ושליחה
│   │   ├── schemas.py       # מודלים
│   │   └── Dockerfile
│   └── requirements.txt
└── service-b/
    ├── app/
    │   ├── main.py          # אפליקציית FastAPI
    │   ├── routers.py       # נקודות קצה
    │   ├── storage.py       # עבודה מול Redis
    │   ├── schemas.py       # מודלי Pydantic
    │   └── Dockerfile
    └── requirements.txt
```

---

## Service A - IP Resolution Service

### תפקיד
- קבלת כתובות IP מלקוחות
- המרת IP למיקום גאוגרפי באמצעות http://ip-api.com
- העברת הנתונים ל-Service B לשמירה
- החזרת אישור שמירה ללקוח

### משתני סביבה
צור קובץ `.env` בתיקיית `service-a/app/`:
```bash
SERVICE_B_URL=http://localhost:8001
```

### API

#### המרת IP למיקום
```http
POST /
Content-Type: application/json

Body: "213.151.56.89"
```

**תשובה מוצלחת:**
```json
{
  "message": "Saved successfully",
  "ip": "213.151.56.89"
}
```

---

## Service B - Coordinates Storage Service

### תפקיד
- קבלת נקודות ציון מ-Service A
- ולידציה של הנתונים
- שמירת הנתונים ב-Redis
- שליפת נתונים לפי IP

### משתני סביבה
צור קובץ `.env` בתיקיית `service-b/app/`:
```bash
REDIS_HOST=localhost
REDIS_PORT=6379
```

### API

#### שמירת נקודות ציון (מופעל רק על ידי Service A)
```http
POST /saveCoordinatesToRedis
Content-Type: application/json

{
  "ip": "213.151.56.89",
  "lat": 31.7674,
  "lon": 35.2186
}
```

#### שליפת נתונים
```http
GET /getCoordinates/{ip}
```

**תשובה:**
```json
{
  "ip": "213.151.56.89",
  "lat": 31.7674,
  "lon": 35.2186
}
```

---

## הוראות הרצה

### דרישות מקדימות
- Python 3.12+
- Redis
- pip

### שלב 1: הפעלת Redis
```bash
# התקנה (אם לא מותקן):
# macOS
brew install redis

# הפעלה
redis-server
```

בדוק ש-Redis רץ:
```bash
redis-cli ping
# אמור להחזיר: PONG
```

---

### שלב 2: הפעלת Service B

#### טרמינל 1 - Service B
```bash
# עבור לתיקיית Service B
cd service-b/app

# התקן חבילות (פעם אחת)
pip install -r ../requirements.txt

# צור קובץ .env
echo "REDIS_HOST=localhost" > .env
echo "REDIS_PORT=6379" >> .env

# הפעל את השירות
python main.py
```

**פלט צפוי:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8001
```

✅ Service B רץ על פורט **8001**

---

### שלב 3: הפעלת Service A

#### טרמינל 2 - Service A
```bash
# עבור לתיקיית Service A
cd service-a/app

# התקן חבילות (פעם אחת)
pip install -r ../requirements.txt

# צור קובץ .env
echo "SERVICE_B_URL=http://localhost:8001" > .env

# הפעל את השירות
python main.py
```

**פלט צפוי:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Service A רץ על פורט **8000**

---

### שלב 4: בדיקת המערכת

#### טרמינל 3 - בדיקות

**בדיקה 1: המרת IP ושמירה (דרך Service A)**
```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '"8.8.8.8"'
```

**תשובה צפויה:**
```json
{
  "message": "Saved successfully",
  "ip": "8.8.8.8"
}
```

---

**בדיקה 2: שליפת נתונים מ-Redis (דרך Service B)**
```bash
curl http://localhost:8001/getCoordinates/8.8.8.8
```

**תשובה צפויה:**
```json
{
  "ip": "8.8.8.8",
  "lat": 39.03,
  "lon": -77.5
}
```

---

**בדיקה 3: שליפה של IP שלא קיים**
```bash
curl http://localhost:8001/getCoordinates/1.1.1.1
```

**תשובה צפויה:**
```json
{
  "detail": "IP not found"
}
```

---

**בדיקה 4: שמירת IP נוסף**
```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '"1.1.1.1"'
```

**תשובה צפויה:**
```json
{
  "message": "Saved successfully",
  "ip": "1.1.1.1"
}
```

---

**בדיקה 5: שליפה של ה-IP החדש**
```bash
curl http://localhost:8001/getCoordinates/1.1.1.1
```

**תשובה צפויה:**
```json
{
  "ip": "1.1.1.1",
  "lat": -27.4766,
  "lon": 153.0166
}
```

---

## סיכום תהליך בדיקה מלא

```bash
# 1. וודא ש-Redis רץ
redis-cli ping
# צפוי: PONG

# 2. שמור IP ראשון
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '"8.8.8.8"'

# 3. שלוף את ה-IP
curl http://localhost:8001/getCoordinates/8.8.8.8

# 4. נסה לשלוף IP שלא קיים (צריך להחזיר 404)
curl http://localhost:8001/getCoordinates/9.9.9.9

# 5. שמור IP נוסף
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '"1.1.1.1"'

# 6. שלוף את ה-IP החדש
curl http://localhost:8001/getCoordinates/1.1.1.1
```

---

## עקרונות ארכיטקטוניים

### הפרדת אחריות
- **Service A**: אחראי רק על תקשורת חיצונית והעברת נתונים
- **Service B**: אחראי רק על אחסון ושליפה
- **Redis**: מאגר נתונים בלבד

### עקרונות עיצוב
1. כל שירות עצמאי ובלתי תלוי
2. תקשורת בין שירותים רק דרך HTTP
3. Service A לא ניגש ישירות ל-Redis
4. Service B לא פונה לשירותים חיצוניים
5. שימוש במשתני סביבה לקונפיגורציה

### ולידציה
- Pydantic לולידציית נתונים
- טווח תקין ל-Latitude: -90 עד 90
- טווח תקין ל-Longitude: -180 עד 180

---

## הערות חשובות

### מגבלות ip-api.com
- 45 בקשות לדקה (גרסה חינמית)
- לשימוש מסחרי יש לשדרג חשבון

### סדר הפעלה
חשוב להפעיל את השירותים בסדר הנכון:
1. ✅ Redis
2. ✅ Service B
3. ✅ Service A

### עצירת השירותים
לעצירת כל שירות לחץ `Ctrl+C` בטרמינל הרלוונטי
