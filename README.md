# A/B Testing — E-commerce Conversion Optimization

> Does a **'Limited Time Offer' badge** increase purchase conversion?  
> Short answer: **yes — but only for the right users.**

[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://a-b-testing-a.streamlit.app/)

---

## What I tested

A simulated A/B test on an e-commerce platform measuring the impact of an urgency-based UI element (LTO badge) on conversion rate. Includes hypothesis testing, confidence interval estimation, and user segmentation analysis.

---

## Results

| Metric | Value |
|---|---|
| Control conversion rate | 5.1% |
| Variant conversion rate | 8.3% |
| Absolute uplift | +3.2 percentage points |
| 95% Confidence Interval | [1.8%, 4.2%] |
| p-value | < 0.05 ✅ |
| Statistically significant | Yes |

---

## Key Insight — Segment Matters

The badge works, **but not universally.**

| Segment | Effect |
|---|---|
| New users | Significant uplift — roll out ✅ |
| New users (mobile) | Highest uplift observed 📱 |
| Returning users | No measurable effect — skip ❌ |

A blanket rollout would dilute the real signal. Segmentation is what makes this result actionable.

---

## Recommendation

- Roll out LTO badge to **new users**, prioritise mobile
- Suppress badge for **returning users** — no lift, adds UI noise
- Re-test returning users separately with a different incentive type

---

## Stack

`Python` `NumPy` `Pandas` `SciPy` `Statsmodels` `Matplotlib` `Seaborn` `Streamlit`

---

## Skills Demonstrated

Experimental design · Hypothesis testing (Z-test for proportions) · Confidence interval estimation · User segmentation · Business recommendation from data
