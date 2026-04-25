"""Mobile-shell navigation — 5 bottom tabs + page-to-tab mapping.

Layout: ✨ Beranda · 🪞 Diri · 🌟 Vibe · 🧰 Tools · ⚙️ Profil. Each tab
either is a leaf page itself (chat) or hosts a list of sub-pages
(diri / vibe / tools), and the bottom tab bar always shows the parent
tab highlighted regardless of which leaf is currently open.

Navigation is URL-driven. The bottom tab bar renders <a href="?page=X">
links so a click triggers a Streamlit rerun via query-param change;
sync_page_from_query() reads the param and updates session state.
"""

from __future__ import annotations

import streamlit as st


# (label_text_key, icon_emoji, tab_page_key, [leaf_page_keys])
NAV_TABS: list[tuple[str, str, str, list[str]]] = [
    ("nav_tab_chat",   "✨", "chat",   []),
    ("nav_tab_diri",   "🪞", "diri",   ["karakter", "inner", "karmic", "fase", "arah", "mbti"]),
    ("nav_tab_vibe",   "🌟", "vibe",   ["zodiak", "shio", "weton"]),
    ("nav_tab_tools",  "🧰", "tools",  ["career", "relationship", "reflection", "oracle"]),
    ("nav_tab_profil", "⚙️", "profil", []),
]


def _build_page_to_tab() -> dict[str, str]:
    out: dict[str, str] = {}
    for _, _, tab_key, leaves in NAV_TABS:
        out[tab_key] = tab_key
        for leaf in leaves:
            out[leaf] = tab_key
    return out


PAGE_TO_TAB: dict[str, str] = _build_page_to_tab()


def sync_page_from_query() -> None:
    """Mirror ?page=X into session_state.current_page so URL-driven nav
    works (refresh-stable, deep-linkable). Run once at the top of app.py
    before the page dispatcher."""
    qp_page = st.query_params.get("page")
    if qp_page and qp_page != st.session_state.get("current_page"):
        st.session_state.current_page = qp_page


def render_bottom_tabs(t) -> None:
    """Render the fixed bottom tab bar. Highlights the parent tab of
    whichever leaf page is currently active."""
    current = st.session_state.get("current_page", "chat")
    parent_tab = PAGE_TO_TAB.get(current, "chat")
    rows = []
    for label_key, icon, tab_key, _ in NAV_TABS:
        is_active = parent_tab == tab_key
        cls = "sn-tab-item sn-tab-active" if is_active else "sn-tab-item"
        rows.append(
            f'<a href="?page={tab_key}" target="_self" class="{cls}">'
            f'<div class="sn-tab-icon">{icon}</div>'
            f'<div class="sn-tab-label">{t(label_key)}</div>'
            "</a>"
        )
    html = (
        '<div class="sn-tabbar"><div class="sn-tabbar-inner">'
        + "".join(rows)
        + "</div></div>"
    )
    st.markdown(html, unsafe_allow_html=True)
