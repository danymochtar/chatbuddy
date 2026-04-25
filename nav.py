"""Sidebar navigation — grouped into 3 thematic categories.

Beranda (chat) stays as a primary button outside the groups; everything
else is bucketed by intent so 14 menu items become 3 small expanders.
"""

from __future__ import annotations

import streamlit as st


# Grouped nav: (group_text_key, [(emoji, page_key, page_label_text_key), ...])
NAV_GROUPS: list[tuple[str, list[tuple[str, str, str]]]] = [
    (
        "nav_group_diri",
        [
            ("👤", "karakter", "nav_karakter"),
            ("🔍", "inner", "nav_inner"),
            ("🎓", "karmic", "nav_karmic"),
            ("🎯", "fase", "nav_fase"),
            ("🧭", "arah", "nav_arah"),
        ],
    ),
    (
        "nav_group_lapisan",
        [
            ("🧠", "mbti", "nav_mbti"),
            ("♈", "zodiak", "nav_zodiak"),
            ("🐉", "shio", "nav_shio"),
            ("🌿", "weton", "nav_weton"),
        ],
    ),
    (
        "nav_group_tools",
        [
            ("💼", "career", "nav_career"),
            ("💑", "relationship", "nav_relationship"),
            ("📝", "reflection", "nav_reflection"),
            ("🔮", "oracle", "nav_oracle"),
        ],
    ),
]


def _nav_button(emoji: str, label: str, page_key: str, current_page: str) -> None:
    is_active = current_page == page_key
    prefix = "✓ " if is_active else ""
    if st.button(
        f"{prefix}{emoji}  {label}",
        key=f"nav_{page_key}",
        use_container_width=True,
        type="primary" if is_active else "secondary",
    ):
        st.session_state.current_page = page_key
        st.rerun()


def render_sidebar_nav(t, current_page: str) -> None:
    """Render the grouped sidebar nav. Beranda first, then 3 expanders."""
    _nav_button("✨", t("nav_chat"), "chat", current_page)
    for group_key, items in NAV_GROUPS:
        group_has_active = any(page_key == current_page for _, page_key, _ in items)
        with st.expander(t(group_key), expanded=group_has_active or group_key == "nav_group_diri"):
            for emoji, page_key, label_key in items:
                _nav_button(emoji, t(label_key), page_key, current_page)
