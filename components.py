"""Reusable Supernova UI components.

Each component returns either a rendered Streamlit element or an HTML
string the caller injects via st.markdown(..., unsafe_allow_html=True).
Keep this module small — only redesign-driven helpers, not a generic
refactor of app.py.
"""

from __future__ import annotations

from html import escape

import streamlit as st


def number_card(label: str, num: int | str | None, archetype: str | None = None) -> str:
    """Render a single number card as an HTML string. Caller wraps the
    returned strings into number_card_grid() to display them.
    """
    if num is None or num == "":
        return ""
    return (
        '<div class="sn-card">'
        f'<div class="sn-card-label">{escape(label)}</div>'
        f'<div class="sn-card-num">{escape(str(num))}</div>'
        f'<div class="sn-card-archetype">{escape(archetype or "")}</div>'
        "</div>"
    )


def number_card_grid(cards: list[str]) -> None:
    """Render a list of HTML card strings into a responsive grid."""
    cards = [c for c in cards if c]
    if not cards:
        return
    html = '<div class="sn-card-grid">' + "".join(cards) + "</div>"
    st.markdown(html, unsafe_allow_html=True)


def cta_ask_deeper(page_key: str, t) -> None:
    """Render a 'Tanya lebih dalem' CTA at the bottom of a non-chat page.
    Click → seeds the chat with a context-aware draft and switches to
    Beranda. The draft renders as a 'pill' on Beranda with Send / Cancel.
    """
    if st.button(
        t("cta_ask_deeper"),
        key=f"ask_deeper_{page_key}",
        use_container_width=True,
    ):
        st.session_state["_chat_seed"] = {
            "page_key": page_key,
            "text": t(f"seed_{page_key}"),
        }
        st.session_state.current_page = "chat"
        st.rerun()
