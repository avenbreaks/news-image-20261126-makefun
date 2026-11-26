# news-image-20261126-makefun

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/avenbreaks/news-image-20261126-makefun/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/avenbreaks/news-image-20261126-makefun/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

The world in one image: 26 November 2026. A newspaper front page — "THE WORLD TODAY" — drawn from the day's reporting: the Houthis' strike on Saudi Arabia's Ras Tanura refinery as Brent crude tops $94, two tankers hitting mines in the Strait of Hormuz, the Israeli strike on a Hamas colonel in Gaza, BepiColombo reaching Mercury orbit after eight years, Gukesh vs Sindarov's drawn Game 2 at the World Chess Championship, the Cairo fuel tanker crash, and the US tariff plan for Taiwan. Every illustration is drawn from scratch with PIL primitives in `build_image.py`; `main.ts` copies the finished page to `/output/entry.png`.

## Run it

```sh
python3 build_image.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=rm0h50bh&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
