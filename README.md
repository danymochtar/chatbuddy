# ChatBuddy Numerologi

Temen AI personal yang pake lensa numerologi (Life Path, Expression, Soul Urge, Personality, Birthday Number) buat ngejawab pertanyaan soal hidup, karir, percintaan, pertemanan, dll.

## Dapetin Gemini API Key (gratis)

1. Buka **https://aistudio.google.com/apikey**
2. Login pake akun Google
3. Klik **Create API key** → copy key-nya (formatnya `AIza...`)

Free tier: 15 request/menit, 1500 request/hari di model Flash. Cukup banget buat personal use.

## Jalanin lokal

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="AIza..."
streamlit run app.py
```

Buka http://localhost:8501

## Deploy ke Streamlit Community Cloud (gratis)

1. Push repo ini ke GitHub.
2. Buka https://share.streamlit.io → **New app** → pilih repo ini.
3. Main file path: `app.py`
4. Di menu **Advanced settings → Secrets**, tambahin:
   ```toml
   GEMINI_API_KEY = "AIza..."
   ```
5. Klik **Deploy**. Selesai — dapet URL publik otomatis.

## Stack

- Streamlit (UI + chat)
- Google Gemini API (`gemini-2.5-flash`) dengan streaming
- Numerologi Pythagorean (termasuk master numbers 11/22/33)
