"""treasureofgems.com の商品価格を取得して data/prices.csv に追記する。"""
import csv
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

PRODUCT_IDS = os.environ.get("PRODUCT_IDS", "2087517284863156226").split(",")
API = "https://api.treasureofgems.com/tea/tea/goods/{}"
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "prices.csv")
JST = timezone(timedelta(hours=9))
FIELDS = ["date", "product_id", "name", "price", "stock", "status", "site_updated"]


def fetch(product_id):
    req = urllib.request.Request(API.format(product_id), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        body = json.load(res)
    if body.get("code") != 0 or not body.get("data"):
        raise RuntimeError(f"API error for {product_id}: {body.get('msg')}")
    return body["data"]


def main():
    today = datetime.now(JST).strftime("%Y-%m-%d")
    rows = []
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

    for pid in (p.strip() for p in PRODUCT_IDS if p.strip()):
        d = fetch(pid)
        new = {
            "date": today,
            "product_id": pid,
            "name": d.get("goodsName", ""),
            "price": d.get("goodsAmount"),
            "stock": d.get("goodsStock"),
            "status": d.get("goodsStatus"),
            "site_updated": d.get("updateDate", ""),
        }
        # 同じ日・同じ商品の行は上書き（1日1件）
        rows = [r for r in rows if not (r["date"] == today and r["product_id"] == pid)]
        rows.append(new)
        print(f"{today} {pid} {new['name']} price={new['price']}")

    rows.sort(key=lambda r: (r["product_id"], r["date"]))
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
