import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
import math

st.set_page_config(page_title="A/B Testing Decision Dashboard", layout="centered")

st.title("📊 A/B Testing Decision Intelligence System")
st.markdown("Make statistically sound and business-driven product decisions.")

# ---------------- INPUT ---------------- #
st.header("🔢 Experiment Input")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Control Group")
    control_users = st.number_input("Users (Control)", min_value=1, value=1000)
    control_conv = st.number_input("Conversions (Control)", min_value=0, value=50)

with col2:
    st.subheader("Variant Group")
    variant_users = st.number_input("Users (Variant)", min_value=1, value=1000)
    variant_conv = st.number_input("Conversions (Variant)", min_value=0, value=80)

# ---------------- SEGMENT ---------------- #
st.header("🎯 Segment Selection")
segment = st.selectbox("User Segment", ["All Users", "New Users", "Returning Users"])

# ---------------- ANALYSIS ---------------- #
if st.button("🚀 Analyze Experiment"):

    cr_control = control_conv / control_users
    cr_variant = variant_conv / variant_users
    uplift = cr_variant - cr_control

    conversions = np.array([variant_conv, control_conv])
    users = np.array([variant_users, control_users])

    z_stat, p_value = proportions_ztest(conversions, users)

    ci_low, ci_high = proportion_confint(
        count=variant_conv,
        nobs=variant_users,
        alpha=0.05
    )

    # ---------------- RESULTS ---------------- #
    st.header("📈 Results")

    col3, col4, col5 = st.columns(3)
    col3.metric("Control CR", f"{cr_control:.2%}")
    col4.metric("Variant CR", f"{cr_variant:.2%}")
    col5.metric("Uplift", f"{uplift:.2%}")

    st.write(f"**P-value:** {p_value:.5f}")
    st.write(f"**95% CI (Variant): [{ci_low:.2%}, {ci_high:.2%}]")

    # ---------------- CHART ---------------- #
    st.subheader("📊 Conversion Comparison")

    fig, ax = plt.subplots()
    ax.bar(["Control", "Variant"], [cr_control, cr_variant])
    ax.set_ylabel("Conversion Rate")
    st.pyplot(fig)

    # ---------------- DECISION ---------------- #
    st.header("🧠 Decision")

    if p_value < 0.05:
        st.success("✅ Statistically Significant — Rollout Recommended")
    else:
        st.error("❌ Not Statistically Significant — Do Not Rollout")

    # ---------------- EXECUTIVE SUMMARY ---------------- #
    st.header("🤖 Executive Decision Insight")

    if p_value < 0.05 and uplift > 0:
        st.success(f"""
        📌 Decision: Rollout Recommended

        The variant shows a statistically significant uplift of {uplift:.2%}.

        Business Impact:
        - Increased conversion → higher revenue
        - Strong candidate for full rollout

        Next Steps:
        - Deploy to all users
        - Monitor retention and long-term impact
        """)
    elif uplift > 0:
        st.warning(f"""
        📌 Decision: Inconclusive

        Positive uplift of {uplift:.2%}, but not statistically significant.

        Next Steps:
        - Increase sample size
        - Run experiment longer
        """)
    else:
        st.error(f"""
        📌 Decision: Reject Variant

        Variant underperforms with negative impact.

        Next Steps:
        - Re-evaluate design
        - Test new hypothesis
        """)

    # ---------------- SAMPLE SIZE ---------------- #
    st.header("📏 Sample Size Calculator")

    baseline = cr_control
    expected_uplift = st.number_input("Expected Uplift (%)", value=2.0) / 100

    p1 = baseline
    p2 = baseline + expected_uplift

    p = (p1 + p2) / 2
    z_alpha = 1.96
    z_beta = 0.84

    n = ((z_alpha + z_beta)**2 * 2 * p * (1 - p)) / ((p2 - p1)**2)

    st.info(f"Required sample size per group: {int(n)} users")

    # ---------------- DURATION ---------------- #
    st.header("⏳ Experiment Duration Estimator")

    daily_users = st.number_input("Daily Users", value=500)

    days = int(n / daily_users) if daily_users > 0 else 0
    st.info(f"Estimated duration: {days} days")

    # ---------------- DOWNLOAD ---------------- #
    st.header("📥 Download Report")

    report = f"""
    A/B Testing Report

    Segment: {segment}

    Control CR: {cr_control:.4f}
    Variant CR: {cr_variant:.4f}
    Uplift: {uplift:.4f}

    P-value: {p_value:.5f}
    Confidence Interval: [{ci_low:.4f}, {ci_high:.4f}]
    """

    st.download_button("Download Report", report, file_name="ab_test_report.txt")
