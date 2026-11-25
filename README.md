# News-image-24 v2 — Tuesday 24 November 2026 in one image

[![Competition](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/ahh955/News-image-24/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/ahh955/News-image-24/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the [make.fun news-image-20261124 bounty](https://make.fun/bounty/news-image-20261124):
sum up 24 November's world news in one image.

A newspaper front page — big serif date headline, stat strip, three
illustrated lead stories, a world map with numbered pins, a numbered
ALSO ON list, a "how to read the labels" box, and a red DATE CHECK box.
18 stories, every one verified against a live source as happening (or
first reported) on Tuesday 24 November 2026. Claims that could not be
independently confirmed (the Hormuz tanker incident, Kyiv's casualty
figure) carry a CLAIM label and are attributed to their source, not
stated as fact.

This is a v2 rebuild of the first entry (round 1 #143, round 2 #1,873):
seven stories whose 24 Nov date could not be verified were dropped and
replaced, the market figures were corrected to the 24 Nov closes, the
three lead photos were regenerated as realistic photographs, and the
ten tiny photo panels were replaced by a legible two-line ALSO ON list.

## The three leads

1. **Russian jets breach Korean air zone** — Seoul alerts Ulleung Island
   as Russian jets enter the air defence zone; the alert is lifted after
   3 minutes. (Reuters / Yonhap)
2. **Tankers burn in Hormuz** — Iran's IRGC says tankers hit mines in
   the strait, a fourth reported later; US Central Command rejects the
   claim. (Press TV / Reuters)
3. **Asia's markets roar back** — Nikkei +3.9%, Kospi +6.3% to a record
   5,006, Taiwan +9.1% as Huang returns to Nvidia. (WSJ)

## Files

- `entry.png` — the finished front page (1024×1024, under 1 MiB)
- `main.ts` — the entrypoint: validates `entry.png` and copies it to
  `/output/entry.png`
- `LICENSE` — MIT

## Regenerate

```sh
python3 compose.py   # rebuilds entry.png (deterministic)
node main.ts         # validates and copies it to /output/entry.png
```

Panel pictures are original generated images; the map is drawn in code
from rough continent outlines. Sources: Reuters, Yonhap, Press TV, KCNA,
MEE, SCMP, WSJ, CoinDesk, Kyiv Independent, Bloomberg, US Dept. of Justice.
