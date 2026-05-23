import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
import math
import io

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="SplitSense — A/B Testing Intelligence",
    page_icon="⚗️",
    layout="centered",
)

# ==============================
# DARK THEME CSS
# ==============================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

    :root {
        --bg:      #080808;
        --surface: #111111;
        --surf2:   #181818;
        --border:  #242424;
        --accent:  #c8ff00;
        --blue:    #3b82f6;
        --purple:  #a855f7;
        --danger:  #ff4444;
        --warn:    #ffb800;
        --ok:      #00e676;
        --text:    #f0f0f0;
        --muted:   #555555;
        --radius:  14px;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }

    .main .block-container {
        background: var(--bg);
        max-width: 860px;
        padding: clamp(1rem, 4vw, 2.5rem);
    }

    /* ── Hero ── */
    .hero {
        text-align: center;
        padding: clamp(2.5rem, 8vw, 4.5rem) 1rem clamp(1.5rem, 4vw, 2.5rem);
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse 70% 50% at 50% 0%,
            rgba(200,255,0,0.06) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(200,255,0,0.08);
        border: 1px solid rgba(200,255,0,0.22);
        color: var(--accent);
        font-size: clamp(0.58rem, 1.6vw, 0.7rem);
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        padding: 0.28rem 0.9rem;
        border-radius: 100px;
        margin-bottom: 1.1rem;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: clamp(1.9rem, 6.5vw, 3.6rem);
        font-weight: 800;
        line-height: 1.05;
        color: var(--text);
        margin: 0 0 0.45rem;
        letter-spacing: -0.02em;
    }
    .hero-title span { color: var(--accent); }
    .hero-sub {
        font-size: clamp(0.82rem, 2.2vw, 0.97rem);
        color: var(--muted);
        font-weight: 300;
        margin: 0;
    }

    /* ── Section labels ── */
    .sec-label {
        font-family: 'Syne', sans-serif;
        font-size: clamp(0.6rem, 1.6vw, 0.7rem);
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--muted);
        margin: 2rem 0 0.75rem;
        padding-bottom: 0.45rem;
        border-bottom: 1px solid var(--border);
    }

    /* ── Cards ── */
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: clamp(1rem, 3vw, 1.5rem);
        margin-bottom: 1rem;
    }
    .card-danger { border-left: 3px solid var(--danger); background: rgba(255,68,68,0.04); }
    .card-warn   { border-left: 3px solid var(--warn);   background: rgba(255,184,0,0.04); }
    .card-ok     { border-left: 3px solid var(--ok);     background: rgba(0,230,118,0.04); }
    .card-blue   { border-left: 3px solid var(--blue);   background: rgba(59,130,246,0.04); }

    /* ── Group headers ── */
    .group-header {
        font-family: 'Syne', sans-serif;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .group-control  { color: var(--blue); }
    .group-variant  { color: var(--purple); }

    /* ── Inputs ── */
    [data-testid="stNumberInput"] input {
        background: var(--surf2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stNumberInput"] input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(200,255,0,0.1) !important;
    }
    [data-testid="stNumberInput"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stSlider"] label {
        color: var(--muted) !important;
        font-size: 0.75rem !important;
        font-family: 'DM Mono', monospace !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    [data-testid="stSelectbox"] > div > div {
        background: var(--surf2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        font-family: 'DM Mono', monospace !important;
    }

    /* ── Button ── */
    [data-testid="stButton"] button,
    [data-testid="stDownloadButton"] button {
        background: var(--accent) !important;
        color: #000 !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: clamp(0.88rem, 2.2vw, 0.98rem) !important;
        letter-spacing: 0.04em;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 1.8rem !important;
        transition: opacity 0.2s, transform 0.15s !important;
    }
    [data-testid="stButton"] button:hover {
        opacity: 0.85 !important;
        transform: translateY(-1px) !important;
    }
    [data-testid="stDownloadButton"] button {
        background: var(--surface) !important;
        color: var(--accent) !important;
        border: 1px solid var(--accent) !important;
    }

    /* ── Metrics ── */
    [data-testid="stMetric"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 1rem 1.2rem !important;
        transition: border-color 0.2s, transform 0.2s;
    }
    [data-testid="stMetric"]:hover {
        border-color: #3a3a3a !important;
        transform: translateY(-1px);
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.68rem !important;
        color: var(--muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-family: 'DM Mono', monospace !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Syne', sans-serif !important;
        font-size: clamp(1.3rem, 3.5vw, 1.8rem) !important;
        font-weight: 700 !important;
        color: var(--accent) !important;
    }

    /* ── Alerts ── */
    [data-testid="stAlert"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        color: var(--text) !important;
        font-size: 0.88rem;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
    }
    [data-testid="stExpander"] summary {
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.88rem !important;
    }

    /* ── Divider / HR ── */
    hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

    /* ── Caption ── */
    [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
        font-size: 0.72rem !important;
        font-family: 'DM Mono', monospace !important;
    }

    /* ── Headers ── */
    h1,h2,h3 {
        font-family: 'Syne', sans-serif !important;
        color: var(--text) !important;
        letter-spacing: -0.01em;
    }
    h2 { font-size: clamp(1.05rem, 2.8vw, 1.35rem) !important; font-weight: 700 !important; }
    h3 { font-size: clamp(0.92rem, 2.2vw, 1.08rem) !important; font-weight: 600 !important; }

    /* ── Big stat display ── */
    .big-stat-wrap { text-align: center; padding: 1.2rem 0 0.8rem; }
    .big-stat-num {
        font-family: 'Syne', sans-serif;
        font-size: clamp(2.5rem, 8vw, 4.5rem);
        font-weight: 800;
        line-height: 1;
    }
    .big-stat-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--muted);
        margin-top: 0.3rem;
    }
    .sig-pill {
        display: inline-block;
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.25rem 0.8rem;
        border-radius: 100px;
        margin-top: 0.8rem;
        background: rgba(200,255,0,0.08);
        border: 1px solid rgba(200,255,0,0.2);
        color: var(--accent);
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--surface); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

    /* ── Mobile ── */
    @media (max-width: 600px) {
        .main .block-container { padding: 0.75rem !important; }
        .hero { padding: 2rem 0.5rem 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme ──────────────────────────────────────────────────
mpl.rcParams.update({
    "figure.facecolor":  "#111111",
    "axes.facecolor":    "#111111",
    "axes.edgecolor":    "#242424",
    "axes.labelcolor":   "#888888",
    "xtick.color":       "#555555",
    "ytick.color":       "#888888",
    "text.color":        "#f0f0f0",
    "grid.color":        "#1e1e1e",
    "grid.linestyle":    "--",
    "font.family":       "monospace",
})

# ==============================
# HERO
# ==============================

st.markdown("""
<div class="hero">
    <div class="hero-badge">Statistical Testing · Bayesian Decision Engine · Product Analytics</div>
    <div class="hero-title">Split<span>Sense</span></div>
    <p class="hero-sub">Statistically sound, business-driven A/B testing intelligence</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# INPUTS
# ==============================

st.markdown("<div class='sec-label'>Experiment Input</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='group-header group-control'>Control Group (A)</div>", unsafe_allow_html=True)
    control_users = st.number_input("Users (Control)", min_value=1, value=1000)
    control_conv  = st.number_input("Conversions (Control)", min_value=0, value=50)

with col2:
    st.markdown("<div class='group-header group-variant'>Variant Group (B)</div>", unsafe_allow_html=True)
    variant_users = st.number_input("Users (Variant)", min_value=1, value=1000)
    variant_conv  = st.number_input("Conversions (Variant)", min_value=0, value=80)

# ── Segment ──────────────────────────────────────────────────────────────
st.markdown("<div class='sec-label'>Segment</div>", unsafe_allow_html=True)

col_seg, col_conf = st.columns(2)
with col_seg:
    segment = st.selectbox("User Segment", ["All Users", "New Users", "Returning Users", "Mobile Users", "Desktop Users"])
with col_conf:
    alpha_pct = st.selectbox("Significance Level", ["95% (α = 0.05)", "99% (α = 0.01)", "90% (α = 0.10)"])

alpha_map = {"95% (α = 0.05)": 0.05, "99% (α = 0.01)": 0.01, "90% (α = 0.10)": 0.10}
alpha = alpha_map[alpha_pct]

st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# ANALYZE BUTTON
# ==============================

if st.button("⚗️ Run Statistical Analysis", use_container_width=True):

    # ── Core stats ────────────────────────────────────────────────────────
    cr_control = control_conv / control_users
    cr_variant = variant_conv / variant_users
    uplift     = cr_variant - cr_control
    rel_uplift = (uplift / cr_control) * 100 if cr_control > 0 else 0

    conversions = np.array([variant_conv, control_conv])
    users       = np.array([variant_users, control_users])

    z_stat, p_value = proportions_ztest(conversions, users)

    ci_low, ci_high = proportion_confint(
        count=variant_conv,
        nobs=variant_users,
        alpha=alpha,
    )

    is_significant = p_value < alpha

    # ── Big p-value display ───────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)

    p_color = "#00e676" if is_significant else "#ff4444"
    sig_text = "Statistically Significant" if is_significant else "Not Significant"

    st.markdown(f"""
    <div class="big-stat-wrap">
        <div class="big-stat-num" style="color:{p_color};">{p_value:.4f}</div>
        <div class="big-stat-label">P-Value</div>
        <div class="sig-pill">{sig_text} · α = {alpha}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Metrics ───────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Control CR",   f"{cr_control:.2%}")
    c2.metric("Variant CR",   f"{cr_variant:.2%}")
    c3.metric("Abs. Uplift",  f"{uplift:+.2%}")
    c4.metric("Rel. Uplift",  f"{rel_uplift:+.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Confidence interval ───────────────────────────────────────────────
    st.markdown(f"""
    <div class="card card-blue">
        <div style="font-family:DM Mono,monospace; font-size:0.7rem; color:#555; text-transform:uppercase;
                    letter-spacing:0.1em; margin-bottom:0.5rem;">
            {int((1-alpha)*100)}% Confidence Interval — Variant CR
        </div>
        <div style="font-family:Syne,sans-serif; font-weight:700; font-size:1.3rem; color:#3b82f6;">
            [{ci_low:.2%} &nbsp;–&nbsp; {ci_high:.2%}]
        </div>
        <div style="font-size:0.8rem; color:#555; margin-top:0.3rem;">
            Z-statistic: {z_stat:.4f} &nbsp;·&nbsp; Segment: {segment}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Conversion rate chart ─────────────────────────────────────────────
    st.markdown("<div class='sec-label'>Conversion Rate Comparison</div>", unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 2, figsize=(8, 3))

    # Bar chart
    ax1 = axes[0]
    bars = ax1.bar(
        ["Control (A)", "Variant (B)"],
        [cr_control, cr_variant],
        color=["#3b82f6", "#a855f7"],
        width=0.45,
        edgecolor="#111",
    )
    for bar, val in zip(bars, [cr_control, cr_variant]):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.002,
            f"{val:.2%}",
            ha="center", va="bottom", fontsize=9, color="#f0f0f0"
        )
    ax1.set_ylabel("Conversion Rate", fontsize=9)
    ax1.set_title("Group Comparison", fontsize=10, color="#888", pad=8)
    ax1.spines[["top", "right", "left"]].set_visible(False)
    ax1.spines["bottom"].set_color("#242424")
    ax1.tick_params(labelsize=8)
    ax1.set_ylim(0, max(cr_control, cr_variant) * 1.35)

    # Uplift bar
    ax2 = axes[1]
    uplift_color = "#00e676" if uplift >= 0 else "#ff4444"
    ax2.barh(
        ["Absolute Uplift"],
        [uplift],
        color=uplift_color,
        height=0.35,
        edgecolor="#111",
    )
    ax2.axvline(0, color="#333", linewidth=1)
    ax2.set_title("Uplift", fontsize=10, color="#888", pad=8)
    ax2.spines[["top", "right", "bottom"]].set_visible(False)
    ax2.spines["left"].set_color("#242424")
    ax2.tick_params(labelsize=8)
    ax2.text(uplift, 0, f" {uplift:+.2%}", va="center", fontsize=9, color=uplift_color)

    fig.tight_layout(pad=2.0)
    st.pyplot(fig)

    # ── Decision card ─────────────────────────────────────────────────────
    st.markdown("<div class='sec-label'>Decision</div>", unsafe_allow_html=True)

    if is_significant and uplift > 0:
        card_class = "card-ok"
        verdict    = "✅ Rollout Recommended"
        verdict_color = "#00e676"
        advice = f"""
        The variant shows a statistically significant uplift of <strong>{uplift:.2%}</strong>
        ({rel_uplift:+.1f}% relative) at the {int((1-alpha)*100)}% confidence level.
        <br><br>
        <strong>Next Steps:</strong> Deploy to all users · Monitor retention & long-term LTV ·
        Document learnings for future experiments.
        """
    elif is_significant and uplift <= 0:
        card_class = "card-danger"
        verdict    = "❌ Reject Variant"
        verdict_color = "#ff4444"
        advice = f"""
        The variant significantly <em>underperforms</em> the control with a change of <strong>{uplift:.2%}</strong>.
        <br><br>
        <strong>Next Steps:</strong> Discard variant · Re-evaluate hypothesis · Test a new design direction.
        """
    elif not is_significant and uplift > 0:
        card_class = "card-warn"
        verdict    = "⚠️ Inconclusive — Extend Test"
        verdict_color = "#ffb800"
        advice = f"""
        Positive uplift of <strong>{uplift:.2%}</strong> observed but not statistically significant
        (p = {p_value:.4f} &gt; α = {alpha}).
        <br><br>
        <strong>Next Steps:</strong> Increase sample size · Run experiment longer ·
        Consider the sample size calculator below.
        """
    else:
        card_class = "card-danger"
        verdict    = "❌ Reject Variant"
        verdict_color = "#ff4444"
        advice = f"""
        Negative uplift and not statistically significant. The variant is unlikely to improve performance.
        <br><br>
        <strong>Next Steps:</strong> Re-evaluate design assumptions · Test a new hypothesis.
        """

    st.markdown(f"""
    <div class="card {card_class}">
        <div style="font-family:Syne,sans-serif; font-weight:700; font-size:1.05rem;
                    color:{verdict_color}; margin-bottom:0.5rem;">{verdict}</div>
        <div style="font-size:0.87rem; color:#aaa; line-height:1.7;">{advice}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sample size calculator ────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='sec-label'>Sample Size Calculator</div>", unsafe_allow_html=True)

    ss_col1, ss_col2 = st.columns(2)
    with ss_col1:
        expected_uplift_pct = st.number_input(
            "Expected Uplift (%)", value=2.0, min_value=0.1, step=0.5
        )
    with ss_col2:
        power_pct = st.selectbox("Statistical Power", ["80% (β = 0.20)", "90% (β = 0.10)", "95% (β = 0.05)"])

    power_map = {"80% (β = 0.20)": 0.84, "90% (β = 0.10)": 1.28, "95% (β = 0.05)": 1.645}
    z_beta  = power_map[power_pct]
    z_alpha = {0.05: 1.96, 0.01: 2.576, 0.10: 1.645}[alpha]

    p1 = cr_control
    p2 = cr_control + (expected_uplift_pct / 100)
    p_avg = (p1 + p2) / 2

    if p2 != p1:
        n_required = math.ceil(
            ((z_alpha + z_beta) ** 2 * 2 * p_avg * (1 - p_avg)) / ((p2 - p1) ** 2)
        )
    else:
        n_required = 0

    st.markdown(f"""
    <div class="card card-blue">
        <div style="font-family:DM Mono,monospace; font-size:0.7rem; color:#555; text-transform:uppercase;
                    letter-spacing:0.1em; margin-bottom:0.3rem;">Required per group</div>
        <div style="font-family:Syne,sans-serif; font-weight:800; font-size:2rem; color:#3b82f6;">
            {n_required:,}
        </div>
        <div style="font-size:0.78rem; color:#555; margin-top:0.2rem;">
            users &nbsp;·&nbsp; baseline CR {cr_control:.2%} &nbsp;·&nbsp;
            target uplift +{expected_uplift_pct:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Duration estimator ────────────────────────────────────────────────
    st.markdown("<div class='sec-label'>Duration Estimator</div>", unsafe_allow_html=True)

    dur_col1, dur_col2 = st.columns(2)
    with dur_col1:
        daily_users = st.number_input("Daily Users (Total)", value=500, min_value=1)
    with dur_col2:
        traffic_split = st.slider("Traffic Split to Experiment (%)", 10, 100, 100, step=10)

    effective_daily = int(daily_users * (traffic_split / 100) / 2)  # per group
    days_needed     = math.ceil(n_required / effective_daily) if effective_daily > 0 else 0
    weeks_needed    = days_needed / 7

    d1, d2, d3 = st.columns(3)
    d1.metric("Days Needed",    f"{days_needed}")
    d2.metric("Weeks Needed",   f"{weeks_needed:.1f}")
    d3.metric("Users/Day/Group", f"{effective_daily:,}")

    # ── Download report ────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='sec-label'>Export</div>", unsafe_allow_html=True)

    report_text = f"""SplitSense — A/B Testing Report
{'='*50}

Segment          : {segment}
Significance     : {int((1-alpha)*100)}% (α = {alpha})

RESULTS
-------
Control Users    : {control_users:,}
Control Conv.    : {control_conv:,}
Control CR       : {cr_control:.4f} ({cr_control:.2%})

Variant Users    : {variant_users:,}
Variant Conv.    : {variant_conv:,}
Variant CR       : {cr_variant:.4f} ({cr_variant:.2%})

Absolute Uplift  : {uplift:+.4f} ({uplift:+.2%})
Relative Uplift  : {rel_uplift:+.2f}%

STATISTICAL TEST
----------------
Z-Statistic      : {z_stat:.4f}
P-Value          : {p_value:.5f}
Significant      : {"Yes" if is_significant else "No"}
{int((1-alpha)*100)}% CI (Variant): [{ci_low:.4f}, {ci_high:.4f}]

DECISION
--------
{verdict.replace("✅ ", "").replace("❌ ", "").replace("⚠️ ", "")}

SAMPLE SIZE
-----------
Required per group : {n_required:,}
Expected Uplift    : +{expected_uplift_pct:.1f}%
Daily Users        : {daily_users:,}
Estimated Duration : {days_needed} days ({weeks_needed:.1f} weeks)
"""

    st.download_button(
        "📥 Download Full Report",
        report_text,
        file_name="ab_test_report.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.caption("⚠️ Statistical significance does not guarantee business impact. Always consider practical significance alongside p-values.")

# ==============================
# EXPLAINERS
# ==============================

st.markdown("<hr>", unsafe_allow_html=True)

with st.expander("📖 How to interpret results"):
    st.markdown("""
    - **P-value** — Probability of observing this result (or more extreme) if there's no real difference. Lower = stronger evidence.
    - **Confidence Interval** — Range where the true conversion rate likely falls.
    - **Absolute Uplift** — Raw difference in conversion rates (Variant − Control).
    - **Relative Uplift** — Percentage improvement relative to control (useful for business communication).
    - **Statistical significance ≠ practical significance.** A tiny uplift can be significant with huge sample sizes but not worth shipping.
    """)

with st.expander("📐 Sample size formula"):
    st.markdown(r"""
    $$n = \frac{(z_{\alpha/2} + z_\beta)^2 \cdot 2\bar{p}(1-\bar{p})}{(p_2 - p_1)^2}$$

    Where $\bar{p} = (p_1 + p_2) / 2$, $z_{\alpha/2}$ is the critical value for your significance level,
    and $z_\beta$ is the critical value for your desired power.
    """)

# ==============================
# FOOTER
# ==============================

st.markdown("""
<hr>
<div style='text-align:center; padding:1rem 0 0.5rem;'>
    <div style='font-family:DM Mono,monospace; font-size:0.68rem; color:#2a2a2a; letter-spacing:0.1em;'>
        SPLITSENSE &nbsp;·&nbsp; v1.0 &nbsp;·&nbsp; Portfolio Demonstration &nbsp;·&nbsp; Built by Akash M S
    </div>
</div>
""", unsafe_allow_html=True)
