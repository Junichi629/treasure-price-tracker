# treasure-price-tracker

[treasureofgems.com の商品](https://treasureofgems.com/product/2087517284863156226) の価格を毎日記録し、グラフで表示します。

- `fetch_price.py` … 公開API（`api.treasureofgems.com/tea/tea/goods/{id}`）から価格を取得し `data/prices.csv` に追記
- `.github/workflows/daily.yml` … GitHub Actions で毎日 9:00 JST に自動実行し、ntfy でスマホに価格を通知
- `index.html` … GitHub Pages で公開する価格推移グラフ

## 商品を追加したいとき
`daily.yml` の `python fetch_price.py` の行を次のように変えると、カンマ区切りで複数商品を追跡できます（グラフ上部に切替メニューが出ます）。

```yaml
      - run: python fetch_price.py
        env:
          PRODUCT_IDS: "2087517284863156226,別の商品ID"
```

※ 価格はAPIの `goodsAmount` の値をそのまま記録しています（サイト上に単位表示がないため単位は不明）。

## スマホ通知（ntfy）
1. スマホに ntfy アプリ（iOS / Android）を入れ、「+」でトピックを購読する
2. GitHub の Settings → Secrets and variables → Actions → New repository secret で
   `NTFY_TOPIC` に同じトピック名を登録する
トピック名を知っている人は誰でも通知を読めるので、推測されにくい名前にしてください。
