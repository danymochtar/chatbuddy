"""Supernova theme — single CSS injection for the whole app.

Brand: midnight intimate. Dark base, warm gold accents, restrained
celestial vibe. No gradient soup. The persona limits celestial metaphors;
the visual side does the same.
"""


def theme_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');

:root {
  --sn-bg: #0E1226;
  --sn-surface: #181C36;
  --sn-surface-2: #20254A;
  --sn-gold: #E9C77B;
  --sn-gold-soft: #B89A5A;
  --sn-cyan: #5BC0BE;
  --sn-text: #F2EAD3;
  --sn-text-dim: #9AA3B5;
  --sn-text-muted: #6F7891;
  --sn-warm-tint: rgba(233, 199, 123, 0.06);
  --sn-cool-tint: rgba(155, 165, 180, 0.06);
  --sn-border: rgba(233, 199, 123, 0.18);
  --sn-border-soft: rgba(233, 199, 123, 0.10);
}

/* Body + reading column */
.stApp { background: var(--sn-bg); }
[data-testid="stMain"] .block-container {
  max-width: 760px;
  padding-top: 2.2rem;
  padding-bottom: 6rem;
}

/* Typography */
html, body, [class*="css"], .stMarkdown, [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
  color: var(--sn-text);
}
h1, h2, h3, h4 {
  font-family: 'Lora', Georgia, serif;
  letter-spacing: -0.01em;
}
[data-testid="stMarkdownContainer"] h1 {
  font-size: 1.85rem !important;
  font-weight: 600;
  margin: 0.4rem 0 0.6rem !important;
}
[data-testid="stMarkdownContainer"] h2 {
  font-size: 1.25rem !important;
  font-weight: 600;
  color: var(--sn-gold);
  margin: 1.4rem 0 0.4rem !important;
}
[data-testid="stMarkdownContainer"] h3 {
  font-size: 1.05rem !important;
  font-weight: 600;
  margin: 1rem 0 0.3rem !important;
}
code, .sn-num {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
}

/* Wordmark */
.sn-wordmark {
  font-family: 'Lora', Georgia, serif;
  font-weight: 600;
  font-size: 2rem;
  background: linear-gradient(90deg, #F2EAD3 0%, #E9C77B 60%, #B89A5A 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: -0.02em;
  text-shadow: 0 0 24px rgba(233, 199, 123, 0.18);
  display: inline-block;
}

/* Blockquote — gold left rule for "— Supernova" sign-offs */
[data-testid="stMarkdownContainer"] blockquote {
  border-left: 2px solid var(--sn-gold-soft);
  padding: 0.4rem 0 0.4rem 0.9rem !important;
  margin: 0.8rem 0 !important;
  color: var(--sn-text-dim);
  font-style: italic;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
  padding: 0.7rem 1rem !important;
  border-radius: 12px !important;
  margin-bottom: 0.6rem !important;
}
[data-testid*="chatMessage"][data-testid*="assistant"],
[data-testid="stChatMessage"][aria-label*="assistant"] {
  background: var(--sn-warm-tint) !important;
  border-left: 2px solid var(--sn-gold-soft) !important;
  border-radius: 0 12px 12px 0 !important;
}
[data-testid*="chatMessage"][data-testid*="user"],
[data-testid="stChatMessage"][aria-label*="user"] {
  background: var(--sn-cool-tint) !important;
}

/* chat_input — soften, gold focus */
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] div[contenteditable="true"] {
  background: var(--sn-surface) !important;
  color: var(--sn-text) !important;
  border: 1px solid var(--sn-border) !important;
  border-radius: 14px !important;
}
[data-testid="stChatInput"] textarea:focus,
[data-testid="stChatInput"] div[contenteditable="true"]:focus-within {
  border-color: var(--sn-gold) !important;
  box-shadow: 0 0 0 2px rgba(233, 199, 123, 0.18) !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
  background: var(--sn-surface) !important;
  border-right: 1px solid var(--sn-border-soft);
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary,
[data-testid="stSidebar"] [data-testid="stExpander"] summary p {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--sn-text-muted) !important;
}

/* Sidebar buttons — flat, left-aligned, gold-on-active */
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"] {
  background: transparent !important;
  border: 1px solid transparent !important;
  color: var(--sn-text-dim) !important;
  justify-content: flex-start !important;
  text-align: left !important;
  padding: 0.4rem 0.7rem !important;
  font-weight: 400 !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"]:hover {
  background: var(--sn-surface-2) !important;
  color: var(--sn-text) !important;
  border-color: var(--sn-border-soft) !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] {
  background: rgba(233, 199, 123, 0.08) !important;
  color: var(--sn-gold) !important;
  border: 1px solid var(--sn-border) !important;
  justify-content: flex-start !important;
  text-align: left !important;
  padding: 0.4rem 0.7rem !important;
  font-weight: 500 !important;
}

/* Main-area buttons keep more presence (vibe / help / submit) */
[data-testid="stMain"] [data-testid="stButton"] button[kind="primary"] {
  background: rgba(233, 199, 123, 0.12) !important;
  color: var(--sn-gold) !important;
  border: 1px solid var(--sn-border) !important;
}
[data-testid="stMain"] [data-testid="stButton"] button[kind="primary"]:hover {
  background: rgba(233, 199, 123, 0.20) !important;
}

/* Number cards (used in sidebar + Karakter) */
.sn-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 0.55rem;
  margin: 0.4rem 0 0.6rem;
}
.sn-card {
  background: var(--sn-surface);
  border: 1px solid var(--sn-border-soft);
  border-radius: 12px;
  padding: 0.7rem 0.85rem;
  transition: border-color 0.2s, transform 0.15s;
}
.sn-card:hover {
  border-color: var(--sn-gold);
  transform: translateY(-1px);
}
.sn-card-label {
  font-size: 0.72rem;
  color: var(--sn-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.sn-card-num {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 1.6rem;
  color: var(--sn-gold);
  line-height: 1;
  margin: 0.25rem 0 0.18rem;
  text-shadow: 0 0 12px rgba(233, 199, 123, 0.25);
}
.sn-card-archetype {
  font-size: 0.82rem;
  color: var(--sn-text-dim);
  font-style: italic;
}

/* Inline number tokens — the "(1)" pill in narrative */
.sn-inline-num {
  display: inline-block;
  padding: 0 0.36em;
  margin: 0 0.08em;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.85em;
  color: var(--sn-gold);
  background: rgba(233, 199, 123, 0.08);
  border-radius: 6px;
}

/* Streaming pulse */
@keyframes sn-pulse {
  0%, 100% { opacity: 0.45; }
  50%      { opacity: 1; }
}
.sn-pulse {
  display: inline-block;
  animation: sn-pulse 1.6s ease-in-out infinite;
  color: var(--sn-gold);
}

/* Sidebar profile header — avatar + greeting */
.sn-profile-row {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin: 0.4rem 0 0.7rem;
}
.sn-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--sn-surface-2);
  border: 1.5px solid var(--sn-gold-soft);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: 'Lora', Georgia, serif;
  font-weight: 600;
  color: var(--sn-gold);
  font-size: 1.15rem;
  flex-shrink: 0;
  text-shadow: 0 0 10px rgba(233, 199, 123, 0.25);
}
.sn-profile-text {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 0;
}
.sn-profile-name {
  font-weight: 600;
  color: var(--sn-text);
  font-size: 0.95rem;
  line-height: 1.15;
}
.sn-profile-meta {
  color: var(--sn-text-muted);
  font-size: 0.72rem;
  line-height: 1.15;
}

/* Empty state card */
.sn-empty {
  background: var(--sn-surface);
  border: 1px dashed var(--sn-border-soft);
  border-radius: 12px;
  padding: 1rem 1.1rem;
  color: var(--sn-text-dim);
  font-style: italic;
  margin: 0.6rem 0;
}

/* Dialog header */
[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h3 {
  color: var(--sn-gold);
}

/* Dividers */
hr {
  border-color: var(--sn-border-soft) !important;
  margin: 1.2rem 0 !important;
}

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }

/* Bordered containers (history cards) — warmer */
[data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
  border-color: var(--sn-border-soft) !important;
  background: var(--sn-surface) !important;
  border-radius: 12px !important;
}
</style>
"""
