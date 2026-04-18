# ChatBuddy Numerologi

Temen AI personal yang pake lensa numerologi (Life Path, Expression, Soul Urge, Personality, Birthday Number) buat ngejawab pertanyaan soal hidup, karir, percintaan, pertemanan, dll.

## Jalanin lokal

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
streamlit run app.py
```

Buka http://localhost:8501

## Deploy ke Streamlit Community Cloud (gratis)

1. Push repo ini ke GitHub (public/private terserah).
2. Buka https://share.streamlit.io → **New app** → pilih repo ini.
3. Main file path: `app.py`
4. Di menu **Advanced settings → Secrets**, tambahin:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
5. Klik **Deploy**. Selesai — dapet URL publik otomatis.

## Stack

- Streamlit (UI + chat)
- Claude API (`claude-opus-4-7`) dengan streaming + prompt caching
- Numerologi Pythagorean (termasuk master numbers 11/22/33)
