from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.db import urls
from app.utils import generate_short_id
from app.config import settings
import redis

app = FastAPI(title="URL Link Shortener")

# Connection with Redis
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


# ---- Rate Limiter ----
def rate_limit(ip: str):
    key = f"rl:{ip}"
    count = redis_client.incr(key)
    if count == 1:
        redis_client.expire(key, 60)
    return count > settings.RATE_LIMIT

#---- Root Page -------
@app.get("/")
def root():
    return {"Welcome to Link Shortener Backend. For documentation, go to /docs"}

#---- Creates Short URL ----
@app.post("/shorten")
def shorten(request: Request, body: dict):
    if "url" not in body:
        raise HTTPException(400, "'url' field is required")

    # RL
    ip = request.client.host
    if rate_limit(ip):
        raise HTTPException(429, "Rate limit exceeded")

    short_id = generate_short_id()

    # Save to MongoDB
    urls.insert_one({
        "short_id": short_id,
        "original_url": body["url"],
        "clicks": 0
    })

    # Cache check in Redis
    redis_client.set(short_id, body["url"], ex=43200)

    return {
        "short_id": short_id,
        "short_url": f"{settings.BASE_URL}/{short_id}"
    }


# ---- Redirect ----
@app.get("/{short_id}")
def redirect(short_id: str):

    # Try cache
    cached_url = redis_client.get(short_id)
    if cached_url:
        urls.update_one({"short_id": short_id}, {"$inc": {"clicks": 1}})
        return RedirectResponse(cached_url)

    # Fallback to DB
    doc = urls.find_one({"short_id": short_id})
    if not doc:
        raise HTTPException(404, "URL not found")

    # Restore cache
    redis_client.set(short_id, doc["original_url"])

    urls.update_one({"short_id": short_id}, {"$inc": {"clicks": 1}})

    return RedirectResponse(doc["original_url"])


# ---- Info Endpoint ----
@app.get("/info/{short_id}")
def info(short_id: str):
    doc = urls.find_one({"short_id": short_id}, {"_id": 0})
    if not doc:
        raise HTTPException(404)
    return doc
