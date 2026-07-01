"""
Reusable UI components for the Maternal Care platform.

These are purely presentational helpers — none of them touch the
machine-learning logic, the prediction pipeline, or any backend
calculation. They exist so every page shares one consistent,
premium-feeling design system instead of duplicating markup.
"""

import streamlit as st


# -----------------------------------------------------------------------
# Page chrome
# -----------------------------------------------------------------------
def set_page(title: str, icon: str, sidebar_state: str = "collapsed"):
    """Standard page config + global CSS injection, shared by every page."""
    st.set_page_config(
        page_title=f"{title} • Maternal Care",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state=sidebar_state,
    )
    load_css()


def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# -----------------------------------------------------------------------
# Navbar
# -----------------------------------------------------------------------
def render_navbar(active: str = "Home"):
    """Sticky glass navbar. Uses st.page_link for real navigation between
    the multipage app's pages, and a plain anchor for in-page scrolling
    to the Features section on the home page."""
    with st.container(key="navbar"):
        cols = st.columns([1.5, 0.8, 0.95, 0.95, 0.95, 1.05, 1.05, 0.85, 1.1])

        with cols[0]:
            st.markdown(
                "<div class='nav-logo'><span class='dot'></span>"
                "Maternal&nbsp;Care</div>",
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.page_link("app.py", label="Home")
        with cols[2]:
            st.markdown(
                "<a class='nav-anchor' href='/#features'>Features</a>",
                unsafe_allow_html=True,
            )
        with cols[3]:
            st.page_link("pages/1_Risk_Prediction.py", label="Prediction")
        with cols[4]:
            st.page_link("pages/2_Pregnancy_Tracker.py", label="Tracker")
        with cols[5]:
            st.page_link("pages/4_AI_Assistant.py", label="AI Assistant")
        with cols[6]:
            st.page_link("pages/3_Health_Tips.py", label="Health Tips")
        with cols[7]:
            st.page_link("pages/5_About.py", label="About")
        with cols[8]:
            with st.container(key="navcta"):
                st.page_link("pages/1_Risk_Prediction.py", label="Get Started →")


# -----------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------
def render_footer():
    st.markdown(
        """
        <div class="site-footer" id="contact">
            <div style="display:flex;flex-wrap:wrap;gap:40px;justify-content:space-between;">
                <div style="flex:1.4;min-width:220px;">
                    <h4 style="font-size:1.2rem;margin-bottom:10px;">🤰 Maternal Care</h4>
                    <p style="max-width:320px;font-size:0.9rem;line-height:1.6;">
                        An AI-powered maternal health platform built to make pregnancy
                        risk awareness clearer, calmer, and more accessible.
                    </p>
                    <div class="social-row" style="margin-top:16px;">
                        <div class="social-pill">🐦</div>
                        <div class="social-pill">💼</div>
                        <div class="social-pill">📸</div>
                        <div class="social-pill">▶️</div>
                    </div>
                </div>
                <div style="flex:1;min-width:160px;">
                    <h4 style="font-size:0.95rem;">Platform</h4>
                    <div class="footer-links">
                        <a href="/#features">Features</a>
                        <a href="/Risk_Prediction">Risk Prediction</a>
                        <a href="/Pregnancy_Tracker">Pregnancy Tracker</a>
                        <a href="/AI_Assistant">AI Assistant</a>
                    </div>
                </div>
                <div style="flex:1;min-width:160px;">
                    <h4 style="font-size:0.95rem;">Resources</h4>
                    <div class="footer-links">
                        <a href="/Health_Tips">Health Tips</a>
                        <a href="/About">About</a>
                        <a href="/#contact">Contact</a>
                    </div>
                </div>
                <div style="flex:1.1;min-width:200px;">
                    <h4 style="font-size:0.95rem;">Stay Informed</h4>
                    <p style="font-size:0.85rem;">Educational tips, new milestones, and
                    platform updates — no spam.</p>
                </div>
            </div>
            <div class="footer-bottom">
                <span>© 2026 Maternal Care Platform · Graduation Project</span>
                <span>For educational purposes only — not a medical diagnosis.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    back_l, back_c, back_r = st.columns([2, 1, 2])
    with back_c:
        st.page_link("app.py", label="↑ Back to top", icon=None)


# -----------------------------------------------------------------------
# Hero
# -----------------------------------------------------------------------
def render_hero(eyebrow: str, title_html: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-eyebrow">✨ {eyebrow}</div>
            <div class="hero-title">{title_html}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(eyebrow: str, title: str, sub: str = ""):
    sub_html = f"<div class='section-sub'>{sub}</div>" if sub else ""
    st.markdown(
        f"""
        <div class="section-eyebrow">{eyebrow}</div>
        <div class="section-title">{title}</div>
        {sub_html}
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------
# Cards
# -----------------------------------------------------------------------
def feature_card_html(icon: str, title: str, desc: str) -> str:
    return f"""
    <div class="feature-card">
        <div class="icon-badge">{icon}</div>
        <h4>{title}</h4>
        <p>{desc}</p>
    </div>
    """


def render_card_grid(cards_html: list):
    st.markdown(
        f"<div class='card-grid'>{''.join(cards_html)}</div>",
        unsafe_allow_html=True,
    )


def risk_result_card(level: str, confidence: float, title: str, sub: str):
    """level: 'low' | 'medium' | 'high'"""
    icon_map = {
        "low": ("🛡️", ""),
        "medium": ("⚠️", ""),
        "high": ("💓", "beat"),
    }
    icon, beat_cls = icon_map.get(level, ("ℹ️", ""))
    conf_html = (
        f"<div class='result-badge'>Confidence: {confidence:.1f}%</div>"
        if confidence is not None
        else ""
    )
    st.markdown(
        f"""
        <div class="result-card {level}">
            <span class="result-icon {beat_cls}">{icon}</span>
            {conf_html}
            <div class="result-title">{title}</div>
            <div class="result-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def step_pills(steps: list, current_index: int):
    """steps: list of labels, current_index: 0-based index of active step"""
    pills = []
    for i, label in enumerate(steps):
        cls = "active" if i == current_index else ("done" if i < current_index else "")
        mark = "✓" if i < current_index else str(i + 1)
        pills.append(
            f"<div class='step-pill {cls}'><span class='num'>{mark}</span><span>{label}</span></div>"
        )
    st.markdown(
        f"<div class='step-pill-row'>{''.join(pills)}</div>", unsafe_allow_html=True
    )


def progress_ring(percent: float, big_text: str, small_text: str):
    percent = max(0, min(100, percent))
    st.markdown(
        f"""
        <div class="ring-wrap">
            <div class="ring" style="--p:{percent}%;">
                <div class="ring-label">
                    <span class="big">{big_text}</span>
                    <span class="small">{small_text}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
