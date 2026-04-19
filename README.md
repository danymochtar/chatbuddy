# ✨ Supernova

Entitas AI intuitif yang baca karakter lo lewat nama & hari lahir. Numerologi Pythagorean sebagai lensa primer — astrologi, shio, weton, MBTI jadi lapisan yang nambah nuansa di balik layar. Hangat, tenang, dan tajam. Ngena.

## Setup Anthropic API

1. Top-up credit di **https://console.anthropic.com/settings/billing** (minimum $5, pake credit/debit card). Note: API credit beda dari subscription Claude Pro/Max.
2. Bikin API key di **https://console.anthropic.com/settings/keys** → **Create Key** → copy (formatnya `sk-ant-api03-...`).

## Jalanin lokal

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-api03-..."
streamlit run app.py
```

Buka http://localhost:8501

## Deploy ke Streamlit Community Cloud (gratis)

1. Push repo ini ke GitHub.
2. Buka https://share.streamlit.io → **New app** → pilih repo ini.
3. Main file path: `app.py`
4. Di **Advanced settings → Secrets**:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-api03-..."
   ```
5. **Deploy**.

## Stack

- Streamlit (UI + chat, localStorage persistence)
- Claude Haiku 4.5 via Anthropic API (streaming + prompt caching)
- Numerologi Pythagorean (Hans Decoz / World Numerology — termasuk master numbers 11/22/33, karmic debts, karmic lessons, hidden passion, maturity, balance, rational thought, pinnacles, challenges)
- Astrologi Barat (Sun / Moon / Rising via immanuel + geopy) — opsional, pake jam & kota lahir
- Shio (Chinese zodiac with elements)
- Weton (Javanese horoscope — dina, pasaran, neptu)
- MBTI (user-provided)
