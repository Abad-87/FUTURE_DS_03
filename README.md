# Bank Marketing Campaign Analysis

## Overview
Analysis of 86,399 telemarketing contacts from the UCI Bank Marketing dataset (combining `bank-full.csv` and `bank-additional-full.csv`).

**Key Metrics:**
- **Total Contacts**: 86,399
- **Total Conversions** (Term Deposit Subscriptions): 9,929
- **Overall Conversion Rate**: **11.49%**

---

## Key Insights

### 1. Channel Performance
- **Cellular** significantly outperforms Telephone and Unknown contacts.
- Unknown contact method has the lowest conversion rate (~4%).
- **Recommendation**: Prioritize cellular calls. Minimize unknown contacts.

### 2. Call Duration (Strongest Zero-Lag Predictor)
- Calls <1 minute → ~0.2% conversion
- 1-3 minutes → ~4%
- 3-5 minutes → ~11%
- 5-10 minutes → ~19%
- **>10 minutes → ~48%+ conversion**

**Insight**: Longer, engaging conversations dramatically improve success.  
**Action**: Train agents to qualify quickly and extend high-potential calls beyond 5–10 minutes.

### 3. Seasonality & Timing
- **Best months**: March (52%), September (46.5%), October (43.8%), December (46.7%)
- **Worst month**: May (6.7%)

**Recommendation**: Focus maximum budget and resources on March, September, October, and December. Reduce or re-test May campaigns.

### 4. Age Group Performance
- **65+**: Highest conversion at **42.1%**
- **Under 25**: Strong at **25.6%**
- Middle ages (35–54): Lower performance (~9–13%)

**Action**: Target seniors (65+) and young customers/students.

### 5. Job & Segment Performance
- Top jobs: **Students**, **Retired**, **Management**, **Technician**
- Best segments often combine **Student/Retired + Tertiary education**

### 6. Previous Campaign Outcome
- When previous outcome was **"success"**, current conversion jumps to **~65%**

**Golden Rule**: Aggressively re-contact previous successful customers (very high ROI).

### 7. Other Observations
- Tertiary (university) educated customers convert better.
- Customers with no housing loan tend to perform better.
- Higher account balance shows positive correlation with conversion.
- More calls in a campaign often lead to diminishing returns.

---

## Strategic Recommendations (Prioritized)

1. **Engagement Training** — Focus on increasing average call duration (target >5 minutes for qualified leads).
2. **Channel Optimization** — Shift as many contacts as possible to cellular.
3. **Seasonal Planning** — Heavy campaigns in Mar, Sep, Oct, Dec.
4. **Targeted Audience**:
   - Age 65+ and under 25
   - Students and Retired customers
   - Tertiary educated individuals
5. **Re-engagement Strategy** — Dedicated track for previous "success" outcomes.
6. **Lead Qualification** — Use call duration and previous outcome as real-time scoring signals.

---

## Visualizations

All charts are saved in the `charts/` folder:

### Static PNG Charts:
- `01_Overall_Conversion.png`
- `02_Channel_Funnel.png`
- `03_Duration_Funnel.png`
- `04_Monthly_Seasonality.png`
- `05_Age_Group.png`
- `06_Top_Jobs.png`
- `07_Education.png`
- `08_Previous_Outcome.png`
- `09_Housing_Loan.png`
- `10_Campaign_Effect.png`
- `11_Balance_Boxplot.png`
- `12_Top_Segments.png`

### Interactive HTML Charts (if Plotly is installed):
Files ending with `_Interactive.html` provide hover tooltips showing exact counts and percentages.

---

## How to View Charts
1. Open the `charts` folder in VS Code.
2. Double-click any `.png` file to view.
3. For interactive versions, open the `.html` files in your browser.

---

## Business Impact
Implementing the above recommendations (especially call duration training, seasonal focus, and re-engagement of previous successes) can significantly improve conversion rates and campaign ROI.

---

**Generated on**: April 2026  
**Dataset**: UCI Bank Marketing (bank-full + bank-additional-full)
