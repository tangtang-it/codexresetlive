# codexresetlive

> 🚀 **CodexReset.live** — A source-first radar for public OpenAI Codex quota resets, verified developer signals, and personal 5-hour rolling limit recovery calculators.

Official Site: [https://codexresetlive.com/](https://codexresetlive.com/)

---

## Features

- 📡 **Live Quota Radar**: Real-time 48-hour probability forecasting based on verified signals from OpenAI leadership (@thsottiaux).
- 📈 **Forecast Pulse Curve**: Interactive native SVG time-series probability wave with historical milestone tags.
- 🕒 **Personal 5-Hour Recovery Engine**: Dynamic rolling recovery clock with timezone detection, recovery progress bar, and unlock alerts.
- 📅 **Interactive Reset Calendar**: Historical monthly calendar with prev/next navigation across all verified public resets since September 2025.
- 🌐 **Global Multi-Language Matrix**: 10 dedicated locales (`en`, `zh-hans`, `zh-hant`, `ja`, `ko`, `es`, `de`, `fr`, `pt-br`, `ru`) with clean URLs and bi-directional `hreflang` matrices.
- 📑 **Search Intent Segmentation**: 4 dedicated landing pages per locale:
  - `/`: Dual-engine flagship dashboard
  - `/reset-today/`: Timely status verdict
  - `/history/`: Complete historical archive & monthly calendar
  - `/methodology/`: Algorithm whitepaper & 8-factor signal switchboard
- 🤖 **GEO & Machine Readable Ready**: Optimized with structured Schema.org JSON-LD, `llms.txt`, and `llms-full.txt`.

---

## Tech Stack & Architecture

- **Static Generation Engine**: Python 3.11+
- **Styling**: Sleek Binance-inspired Dark Minimalist UI (Pure Vanilla CSS, zero heavy frontend framework overhead)
- **Deployment**: Cloudflare Pages / Vercel (Pure static HTML with millisecond edge CDN delivery)

---

## Build & Compile

```bash
# Build all 40+ static pages across 10 languages
python scripts/build_studio.py
```

The generated static output will be located in the `site/` directory ready for deployment.
