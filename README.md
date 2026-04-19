# A/B Testing Case Study — E-commerce Conversion Optimization

app: https://a-b-testing-a.streamlit.app/

## Business Problem
Does adding a **'Limited Time Offer' badge** on product pages increase purchase conversion rate?

## Project Summary
Designed and analyzed a simulated A/B test for an e-commerce platform to evaluate the impact of urgency-based UI elements on conversion rate. The analysis includes hypothesis testing, confidence interval estimation, and user segmentation.

## Key Results
| Metric | Value |
|---|---|
| Control conversion rate | ~5% |
| Variant conversion rate | ~8% |
| Absolute uplift | ~3% |
| 95% Confidence Interval | [1.8%, 4.2%] |
| P-value | < 0.05 ✅ |
| Statistically significant | Yes |

## Segmentation Insight
The badge significantly improves conversion for **new users** but has no measurable effect on **returning users** — enabling a targeted rollout strategy.

## Business Recommendation
- ✅ Roll out LTO badge for **new users** (significant uplift)
- ❌ Do not show badge to **returning users** (no effect, adds noise)
- 📱 Prioritise **mobile new users** (highest uplift observed)

## Tools Used
- Python (NumPy, Pandas, SciPy, Statsmodels, Matplotlib, Seaborn)
- Jupyter Notebook

## How to Run
```bash
pip install numpy pandas scipy statsmodels matplotlib seaborn
jupyter notebook ab_testing_ecommerce.ipynb
```

## Skills Demonstrated
- Experimental design & hypothesis formulation
- Statistical significance testing (Z-test for proportions)
- Confidence interval interpretation
- User segmentation analysis
- Data-driven business recommendation
