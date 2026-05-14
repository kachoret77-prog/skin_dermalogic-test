import streamlit as st


THEME_CSS = """
<style>
:root {
    --mint: #14b8a6;
    --mint-dark: #0f766e;
    --coral: #fb7185;
    --ink: #172026;
    --muted: #667085;
    --line: #e4ebe8;
    --surface: #ffffff;
    --soft: #f3fbf8;
}
.stApp {
    background:
        linear-gradient(180deg, #f4fbf8 0%, #ffffff 36%),
        #ffffff;
    color: var(--ink);
}
.block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p {
    letter-spacing: 0;
}
h1 {
    color: var(--ink);
    font-size: 2.2rem;
    line-height: 1.2;
    margin-bottom: 0.35rem;
}
[data-testid="stSidebar"] {
    background: #f0faf7;
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--mint-dark);
}
.stButton > button {
    width: 100%;
    min-height: 3rem;
    border: 0;
    border-radius: 8px;
    background: var(--ink);
    color: white;
    font-weight: 800;
}
.stButton > button:hover {
    background: var(--mint-dark);
    color: white;
}
.intro {
    padding: 1rem 0 1.35rem;
    border-bottom: 1px solid var(--line);
    margin-bottom: 1.25rem;
}
.intro-kicker {
    color: var(--coral);
    font-weight: 800;
    margin-bottom: 0.35rem;
}
.intro-copy {
    color: var(--muted);
    font-size: 1rem;
    margin: 0;
}
.panel {
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 1rem;
    background: var(--surface);
    margin-bottom: 0.9rem;
}
.soft-panel {
    border: 1px solid #d7f0e9;
    border-radius: 8px;
    padding: 1rem;
    background: var(--soft);
}
.result-tone {
    margin-top: 0.2rem;
    margin-bottom: 0.9rem;
}
.image-column-spacer {
    height: 0.85rem;
    border-top: 1px solid var(--line);
    margin-top: 1rem;
}
.notice-panel {
    border: 1px solid #fde2e7;
    border-radius: 8px;
    padding: 0.9rem 1rem;
    background: #fff7f8;
    color: #8a3a47;
    margin-top: 0.75rem;
}
.guide-panel {
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 1rem;
    background: #ffffff;
    margin-top: 0.9rem;
    margin-bottom: 0.15rem;
}
.guide-title {
    color: var(--ink);
    font-size: 0.98rem;
    font-weight: 900;
    margin-bottom: 0.35rem;
}
.guide-text {
    color: var(--muted);
    line-height: 1.6;
}
.metric-label {
    color: var(--muted);
    font-size: 0.88rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.metric-value {
    color: var(--mint-dark);
    font-size: 1.55rem;
    font-weight: 900;
    line-height: 1.15;
}
.care-note {
    color: var(--muted);
    margin-top: 0.45rem;
}
.product-card {
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 1rem;
    background: #ffffff;
    margin-bottom: 0.75rem;
}
.product-name {
    color: var(--ink);
    font-size: 1.02rem;
    font-weight: 900;
    margin-bottom: 0.3rem;
}
.product-effect {
    color: var(--muted);
    margin-bottom: 0.65rem;
}
.product-card a {
    color: var(--mint-dark);
    font-weight: 800;
    text-decoration: none;
}
.small-muted {
    color: var(--muted);
    font-size: 0.92rem;
}
</style>
"""


def apply_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)
