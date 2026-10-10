# treasure-price-tracker

treasureofgems.com の商品の価格を毎日記録し、グラフで表示します。

| 商品 | グラフ | 通知 |
|---|---|---|
| [氷種翡翠の無事牌](https://treasureofgems.com/product/2087517284863156226) | [グラフ](https://junichi629.github.io/treasure-price-tracker/?id=2087517284863156226) | 毎日 |
| [濃緑色の翡翠勾玉](https://treasureofgems.com/product/2087516465723973633) | [グラフ](https://junichi629.github.io/treasure-price-tracker/?id=2087516465723973633) | 価格が変わった日だけ |

- `fetch_price.py` … 公開API（`api.treasureofgems.com/tea/tea/goods/{id}`）から価格を取得し `data/prices.csv` に追記
- `.github/workflows/daily.yml` … GitHub Actions で毎日 9:00 JST に自動実行し、ntfy でスマホに価格を通知
- `index.html` … GitHub Pages で公開する価格推移グラフ

## 商品を追加したいとき
`daily.yml` の `PRODUCT_IDS` にカンマ区切りで商品IDを足します（グラフ上部に切替メニューが出ます）。
価格が変わった日だけ通知したい商品は `NOTIFY_ON_CHANGE_IDS` にも入れてください。
グラフの URL に `?id=商品ID` を付けると、その商品のグラフを直接開けます。

※ 価格はAPIの `goodsAmount` の値をそのまま記録しています（サイト上に単位表示がないため単位は不明）。

## スマホ通知（ntfy）
1. スマホに ntfy アプリ（iOS / Android）を入れ、「+」でトピックを購読する
2. GitHub の Settings → Secrets and variables → Actions → New repository secret で
   `NTFY_TOPIC` に同じトピック名を登録する
トピック名を知っている人は誰でも通知を読めるので、推測されにくい名前にしてください。
