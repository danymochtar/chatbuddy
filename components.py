"""Reusable Supernova UI components.

Each component returns either a rendered Streamlit element or an HTML
string the caller injects via st.markdown(..., unsafe_allow_html=True).
Keep this module small — only redesign-driven helpers, not a generic
refactor of app.py.
"""

from __future__ import annotations

import re
from html import escape

import streamlit as st


# Matches parenthesized numerology tokens — single 1-2 digit numbers and
# slash-chained reductions like (29/11/2). Lookbehind / lookahead prevent
# matching things like "year (2023)" or "1(2)pm".
_INLINE_NUM_PATTERN = re.compile(
    r"(?<![\w/])\((\d{1,2}(?:/\d{1,2})*)\)(?![\w])"
)


def inject_inline_num_tokens(text: str) -> str:
    """Wrap parenthesized numerology tokens with the .sn-inline-num pill.
    Apply to assistant-generated markdown only — never user input.
    Renders as HTML, so callers must use unsafe_allow_html=True.
    """
    if not text:
        return text
    return _INLINE_NUM_PATTERN.sub(r'<span class="sn-inline-num">\1</span>', text)


def render_ai_markdown(text: str) -> None:
    """Render assistant markdown with the inline-num pill applied."""
    st.markdown(inject_inline_num_tokens(text or ""), unsafe_allow_html=True)


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


def profile_avatar_row(nickname: str, full_name: str, born_label: str, dob: str) -> None:
    """Sidebar profile header: gold-bordered initial circle + name + meta."""
    initial = (nickname or full_name or "?").strip()[:1].upper()
    html = (
        '<div class="sn-profile-row">'
        f'<div class="sn-avatar">{escape(initial)}</div>'
        '<div class="sn-profile-text">'
        f'<div class="sn-profile-name">👋 {escape(nickname or full_name)}</div>'
        f'<div class="sn-profile-meta">{escape(full_name)} · {escape(born_label)} {escape(dob)}</div>'
        "</div></div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def sn_empty(message: str, *, icon: str = "✨", allow_markdown: bool = False) -> None:
    """Render a soft, branded empty-state card. Replaces stock st.info.

    Set allow_markdown=True when the message contains markdown (bold,
    italic, etc.) that should render — in that case the message is
    passed through without HTML-escaping (it'll be parsed by
    Streamlit's markdown engine before our wrapping HTML applies).
    """
    body = message if allow_markdown else escape(message)
    safe_icon = escape(icon)
    st.markdown(
        f'<div class="sn-empty">{safe_icon} &nbsp; {body}</div>',
        unsafe_allow_html=True,
    )


def render_loading_pulse(placeholder, message: str) -> None:
    """Render a pulsing ✨ + label into a Streamlit placeholder. The first
    streamed chunk overwrites it, so this works as a brand-aligned
    replacement for st.spinner around stream_assistant calls."""
    safe = escape(message)
    placeholder.markdown(
        f'<div class="sn-empty"><span class="sn-pulse">✨</span> &nbsp; <em>{safe}</em></div>',
        unsafe_allow_html=True,
    )


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
