# News-image-24 — Tuesday 24 November 2026 in one image

[![Competition](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/ahh955/News-image-24/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/ahh955/News-image-24/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the [make.fun news-image-20261124 bounty](https://make.fun/bounty/news-image-20261124):
sum up 24 November's world news in one image.

A newspaper front page — big serif date headline, stat strip, three
illustrated lead stories, ten more features, a world map with numbered
pins, an ALSO ON list, and a red DATE CHECK box. 18 stories, every one
verified against a live source as happening (or first reported) on
Tuesday 24 November 2026. Claims that could not be independently
confirmed (the Hormuz tanker incident) are attributed to their source,
not stated as fact.

## The three leads

1. **Russian jets breach Korean skies** — Seoul sounds a 3-minute
   evacuation alert for Ulleung Island after warplanes enter the air
   defence zone without notice. (Reuters / Yonhap)
2. **Three tankers burn in Hormuz** — Iran's IRGC says three oil tankers
   hit naval mines and caught fire in the strait overnight; unconfirmed.
   (Press TV)
3. **Asia's markets roar back** — Nikkei +2.6%, Kospi +4%, SoftBank +15%
   after Wall Street's best day since April. (Reuters)

## Files

- `entry.png` — the finished front page (1024×1024, under 1 MiB)
- `main.ts` — the entrypoint: validates `entry.png` and copies it to
  `/output/entry.png`
- `compose.py` — builds `entry.png` from the panel photos (run it to
  regenerate; output is deterministic)
- `panels/` — the 13 original generated panel photographs
- `LICENSE` — MIT

## Regenerate

```sh
python3 compose.py   # rebuilds entry.png
node main.ts         # validates and copies it to /output/entry.png
```

Panel pictures are original generated images; the map is drawn in code
from rough continent outlines. Sources: Reuters, Yonhap, Press TV, KCNA,
MEE, SCMP, Japan Times, CNA, WSJ, CoinDesk, Upstox.
