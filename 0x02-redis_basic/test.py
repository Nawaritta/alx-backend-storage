import redis

r = redis.Redis()
r.set("Morocco", "Rabat")
r.set("Senegal", "Dakar")
r.set("Egypt", "Cairo")

print(r.get("Morocco"))
print(r.get("Egypt"))
