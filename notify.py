"""data/prices.csv の最新価格を ntfy でスマホに通知する。"""
import csv
import json
import os
import urllib.request

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "prices.csv")
TOPIC = os.environ["NTFY_TOPIC"]
REPO = os.environ.get("GITHUB_REPOSITORY", "")  # 例: owner/treasure-price-tracker
# ここに入れた商品は「価格が変わった日」だけ通知する（それ以外は毎日通知）
ON_CHANGE_IDS = {p.strip() for p in os.environ.get("NOTIFY_ON_CHANGE_IDS", "").split(",") if p.strip()}


def fmt(n):
    return f"{n:,.0f}" if n == int(n) else f"{n:,.2f}"


def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    lines = []
    for pid in dict.fromkeys(r["product_id"] for r in rows):
        hist = [r for r in rows if r["product_id"] == pid]
        last = hist[-1]
        price = float(last["price"])
        if len(hist) > 1:
            prev = float(hist[-2]["price"])
            d = price - prev
            if pid in ON_CHANGE_IDS and d == 0:
                continue
            change = "前日比 ±0" if d == 0 else f"前日比 {'+' if d > 0 else '-'}{fmt(abs(d))}"
            if pid in ON_CHANGE_IDS:
                change = f"{fmt(prev)} → {fmt(price)}、{change}"
        else:
            change = "記録初日"
        lines.append(f"{last['name']}\n価格 {fmt(price)}（{change}）\n在庫 {last['stock']}")

    if not lines:
        print("no notification today")
        return

    payload = {
        "topic": TOPIC,
        "title": f"価格チェック {rows[-1]['date']}",
        "message": "\n\n".join(lines),
        "tags": ["gem"],
    }
    if REPO:
        owner, name = REPO.split("/")
        payload["click"] = f"https://{owner.lower()}.github.io/{name}/"

    req = urllib.request.Request(
        "https://ntfy.sh/",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        print("notified:", res.status)


if __name__ == "__main__":
    main()
