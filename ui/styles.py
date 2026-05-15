import streamlit as st


THEME_CSS = """
<style>
:root {
    --sage: #8fb9a8;
    --sage-dark: #4f7d6b;
    --leaf: #6fa38e;
    --blush: #d79a8b;
    --ivory: #fffaf3;
    --cream: #f7efe5;
    --ink: #24302c;
    --muted: #74817b;
    --line: #eadfd3;
    --surface: #ffffff;
    --soft: #f7faf8;
    --shadow: 0 18px 42px rgba(79, 125, 107, 0.12);
}
.stApp {
    background:
        linear-gradient(180deg, #fffaf3 0%, #fbf8f1 44%, #ffffff 100%),
        #ffffff;
    color: var(--ink);
}
.block-container {
    max-width: 1160px;
    padding-top: 1.7rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p {
    letter-spacing: 0;
}
h1 {
    color: var(--ink);
    font-size: 2.12rem;
    line-height: 1.2;
    margin: 0 0 0.45rem;
    word-break: keep-all;
}
[data-testid="stSidebar"] {
    background: #fbf5ec;
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--sage-dark);
}
.stButton > button {
    width: 100%;
    min-height: 3rem;
    border: 0;
    border-radius: 999px;
    background: linear-gradient(135deg, var(--sage-dark), var(--leaf));
    color: white;
    font-weight: 800;
    box-shadow: 0 12px 26px rgba(79, 125, 107, 0.22);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #456f5f, #628f7d);
    color: white;
}
.hero {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 1.15rem;
    align-items: center;
    border: 1px solid rgba(234, 223, 211, 0.95);
    border-radius: 20px;
    padding: 1.35rem 1.45rem;
    background:
        linear-gradient(135deg, rgba(255,255,255,0.94), rgba(246,250,247,0.9));
    box-shadow: var(--shadow);
    margin-bottom: 1.55rem;
    overflow: visible;
}
.hero-kicker {
    color: var(--blush);
    font-weight: 800;
    margin-bottom: 0.35rem;
}
.hero-copy p {
    color: var(--muted);
    font-size: 0.98rem;
    margin: 0;
    max-width: 720px;
    line-height: 1.65;
    word-break: keep-all;
}
.hero-badges {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    gap: 0.45rem;
    max-width: 270px;
}
.hero-badges span,
.profile-pills span,
.tag-row span {
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    padding: 0.38rem 0.68rem;
    background: #f1f7f3;
    color: var(--sage-dark);
    font-size: 0.82rem;
    font-weight: 800;
}
.section-label {
    color: var(--blush);
    font-size: 0.78rem;
    font-weight: 900;
    letter-spacing: 0;
    margin-bottom: 0.18rem;
}
.section-title {
    color: var(--ink);
    font-size: 1.08rem;
    font-weight: 900;
    margin-bottom: 0.78rem;
}
.panel {
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1rem;
    background: var(--surface);
    margin-bottom: 0.9rem;
    box-shadow: 0 10px 24px rgba(23, 32, 38, 0.04);
}
.soft-panel {
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1rem;
    background: var(--soft);
}
.analysis-ready,
.result-card,
.care-comment,
.mini-card {
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 1.12rem;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: var(--shadow);
}
.analysis-ready,
.result-card,
.care-comment,
.mini-card,
.notice-panel {
    margin-bottom: 1.05rem;
}
.analysis-ready p {
    color: var(--muted);
    line-height: 1.6;
    margin: 0 0 0.75rem;
}
.profile-pills,
.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
}
.result-card {
    margin-top: 1rem;
}
.result-heading,
.score-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    align-items: center;
}
.status-badge {
    border-radius: 999px;
    padding: 0.45rem 0.75rem;
    background: #f1f7f3;
    color: var(--sage-dark);
    font-size: 0.9rem;
    font-weight: 900;
}
.score-caption {
    color: var(--muted);
    font-size: 0.84rem;
}
.score-track {
    height: 10px;
    border-radius: 999px;
    overflow: hidden;
    background: #eee6da;
    margin: 0.95rem 0;
}
.score-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #d8e9df, var(--leaf));
}
.result-tone {
    border-top: 1px solid var(--line);
    padding-top: 0.75rem;
    margin-top: 0.5rem;
}
.image-column-spacer {
    height: 1rem;
    border-top: 1px solid var(--line);
    margin-top: 1.15rem;
}
.notice-panel {
    border: 1px solid #ead8d3;
    border-radius: 16px;
    padding: 1rem;
    background: #fff8f4;
    color: #8a5a50;
    margin-top: 1rem;
}
.guide-panel {
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1rem;
    background: #ffffff;
    margin-top: 1rem;
    margin-bottom: 0.35rem;
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
    color: var(--sage-dark);
    font-size: 1.75rem;
    font-weight: 900;
    line-height: 1.15;
}
.care-note {
    color: var(--muted);
    margin-top: 0.45rem;
}
.product-card {
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 1rem;
    background: #ffffff;
    margin-bottom: 0.85rem;
    box-shadow: 0 12px 28px rgba(23, 32, 38, 0.06);
}
.product-tag {
    display: inline-flex;
    border-radius: 999px;
    padding: 0.28rem 0.55rem;
    background: #fff3ec;
    color: #a76c5e;
    font-size: 0.78rem;
    font-weight: 900;
    margin-bottom: 0.55rem;
}
.product-name {
    color: var(--ink);
    font-size: 1.05rem;
    font-weight: 900;
    margin-bottom: 0.3rem;
}
.product-reason {
    color: var(--muted);
    font-size: 0.88rem;
    line-height: 1.55;
    margin-bottom: 0.4rem;
}
.product-effect {
    color: var(--muted);
    margin-bottom: 0.65rem;
}
.product-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    padding: 0.48rem 0.78rem;
    background: var(--ink);
    color: #ffffff !important;
    font-size: 0.88rem;
    font-weight: 800;
    text-decoration: none;
}
.privacy-note {
    border: 1px solid #e8efec;
    border-radius: 14px;
    padding: 0.8rem 0.9rem;
    background: rgba(255, 255, 255, 0.82);
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.55;
    margin-top: 0.65rem;
}
.compare-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    align-items: center;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 0.95rem 1rem;
    background: #ffffff;
    margin-bottom: 0.75rem;
}
.compare-row span {
    min-width: 4.8rem;
    text-align: right;
    color: var(--sage-dark);
    font-weight: 900;
}
.small-muted {
    color: var(--muted);
    font-size: 0.92rem;
}
@media (max-width: 760px) {
    .hero {
        display: block;
        padding: 1.1rem;
    }
    .hero-badges {
        justify-content: flex-start;
        margin-top: 0.9rem;
        min-width: 0;
    }
    h1 {
        font-size: 1.62rem;
    }
}
</style>
"""


def apply_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)
