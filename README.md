# Black Coordinates List

## תיאור
מערכת להמרת כתובות IP לנקודות ציון גאוגרפיות ואחסון הנתונים.

**ארכיטקטורה:**
```
Client → Service A → ip-api.com
           ↓
       Service B → Redis
```

---

## הרצה מהירה

### הפעלת המערכת
```bash
docker-compose up -d --build
```

### בדיקת המערכת
```bash
# שמירת IP
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '"8.8.8.8"'

# שליפת נתונים
curl http://localhost:8001/getCoordinates/8.8.8.8

# שליפת כל הנתונים
curl http://localhost:8001/getAllCoordinates
```

### עצירת המערכת
```bash
docker-compose down
```

---

## API

### Service A (פורט 8000)
**המרת IP למיקום:**
```bash
POST /
Body: "8.8.8.8"
```

### Service B (פורט 8001)
**שליפת נתונים לפי IP:**
```bash
GET /getCoordinates/{ip}
```

**שליפת כל הנתונים:**
```bash
GET /getAllCoordinates
```

---

## פקודות שימושיות

```bash
# צפייה בלוגים
docker-compose logs -f

# עצירה + מחיקת נתונים
docker-compose down -v

# הפעלה מחדש
docker-compose restart

# בדיקת סטטוס
docker-compose ps
```

---

## פתרון בעיות

**בדיקת Redis:**
```bash
docker-compose exec redis redis-cli ping
# צפוי: PONG
```

**צפייה בלוגים:**
```bash
docker-compose logs service-a
docker-compose logs service-b
```
