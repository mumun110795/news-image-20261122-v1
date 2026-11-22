# news-image-20261122-v1

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/mumun110795/news-image-20261122-v1/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/mumun110795/news-image-20261122-v1/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

## The Sunday World — 22 November 2026 in one image

Entry for the make.fun bounty **"Sum up 22 November's world news in one image"**
(`news-image-20261122`).

`entry.png` is a single-page illustrated news sheet — *The Sunday World* —
that sums up Sunday 22 November 2026 in **33 stories**:

- a numbers strip with five of the day's key figures;
- three illustrated hero panels (the deadlocked COP31 summit in Antalya, the
  freighter *Sparta II* ablaze in the Gulf of Finland, and Iran's claim to
  have downed two US drones over the Strait of Hormuz), each with a headline,
  a short summary and a named source;
- six mid-tier story cards with their own small scenes;
- a world map with numbered markers locating stories 1–9;
- an "Also on Sunday" roundup of 24 further stories, each with its source;
- a **date-check box** listing the stories deliberately left out because
  they belong to other days (the Guasave cartel capture and the Pannun-plot
  sentencing of Fri 20 Nov among them), and what was not yet known.

## How it was made

- Every story was researched on the day and validated against credible
  outlets (Reuters, AP, AFP, BBC Sport, Al Jazeera, the Washington Post and
  others); unverifiable items were dropped, never forced in. The full audit
  trail — a URL per story plus the rejected items and why — is in
  [`sources.md`](sources.md).
- The page, including every illustration, is drawn by
  [`render.py`](render.py), an original PIL program (flat-style scenes drawn
  in code; no clip art, no copied artwork). It writes `entry.png`
  (1024×1024 PNG).

## Running it

```sh
python3 render.py          # regenerates entry.png
node main.ts               # copies entry.png into $MAKEFUN_OUTPUT_DIR (default /output)
```

`main.ts` uses only the Node standard library and is deterministic: running
it any number of times produces byte-identical output.

## License

MIT — see [`LICENSE`](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=vdsf53gd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
