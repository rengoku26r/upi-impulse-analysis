# Column Mapping Reference
## UPI Impulse Analysis — `combined_clean_fixed.csv`

> This document explains every column in the cleaned dataset.  
> For encoded columns, the mapping from original survey text → integer is shown.  
> **Total rows: 105 | Total columns: 46**

---

## Section A — Identifiers

| Column | Type | Description |
|--------|------|-------------|
| `respondent_id` | int | Unique numeric ID assigned per respondent. Prefix indicates source: `1xxx` = AIIMS Jodhpur, `2xxx` = Jaipur Colleges, `3xxx` = IIT Bhilai, `4xxx` = IIT Delhi |
| `source_college` | str | College group derived from `respondent_id` prefix. Values: `"AIIMS Jodhpur"`, `"IIT Bhilai"`, `"IIT Delhi"`, `"Jaipur Colleges"` |

---

## Section B — Demographics

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `age_group` | str | Age range of respondent | `"Under 18"`, `"18-21"`, `"22-25"`, `"25+"` |
| `gender` | str | Gender | `"Male"`, `"Female"` |
| `college_year` | str | Level of study | `"Ug"` (Undergraduate), `"Pg"` (Postgraduate) |
| `income_source` | str | How respondent funds their expenses | `"100% Parents Money"`, `"Mix of parents + I earn something on the side"`, `"I have an internship / part-time job"`, `"I run a side hustle / freelance / small business"` |

---

## Section C — Budget

| Column | Type | Description | Values / Notes |
|--------|------|-------------|----------------|
| `monthly_budget_range` | str | Monthly budget range (joke labels removed) | `"< Rs1000"`, `"Rs1000 - Rs3000"`, `"Rs3000 - Rs6000"`, `"Rs6000+"` |
| `avg_monthly_budget` | float | Best estimate of monthly budget in ₹. Uses exact value if respondent provided one; otherwise uses range midpoint. Outliers (>₹10,000 in Rs6000+ bracket) capped at ₹7,000. | Range: 500–8000 |

**Midpoints used when exact value was missing:**

| Range | Midpoint Used |
|-------|--------------|
| `< Rs1000` | 500 |
| `Rs1000 - Rs3000` | 2000 |
| `Rs3000 - Rs6000` | 4500 |
| `Rs6000+` | 7000 |

---

## Section D — UPI App Usage

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `primary_upi_app` | str | Main UPI app used | `"Google Pay (GPay)"`, `"PhonePe"`, `"Paytm"`, `"Bhim UPI"`, `"Navi UPI"`, `"Cred"`, etc. |
| `perceives_upi_risky` | int | Whether respondent thinks UPI makes overspending easier | `1` = Yes, `0` = No / Never thought about it |
| `upi_usage_reason` | str | Why they use UPI offline (free text, not used in ML) | Raw grouped text |

---

## Section E — Spending Behavior

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `weekly_tx_range` | str | Weekly UPI transaction count range (joke labels removed) | `"1-3"`, `"4-7"`, `"8-15"`, `"15+"` |
| `avg_weekly_tx` | float | Best estimate of weekly transactions. Uses exact value if provided; otherwise uses range midpoint. | Range: 1–40 |
| `pct_unplanned` | str | % of transactions that were unplanned (joke labels removed) | `"<20%"`, `"20-40%"`, `"40-60%"`, `"60-80%"`, `">80%"` |
| `pct_unplanned_avg` | int | Numeric midpoint of `pct_unplanned` | `10`, `30`, `50`, `70`, `90` |

**Midpoints used for `pct_unplanned_avg`:**

| Range | Midpoint |
|-------|---------|
| `<20%` | 10 |
| `20-40%` | 30 |
| `40-60%` | 50 |
| `60-80%` | 70 |
| `>80%` | 90 |

---

## Section F — Financial Habits

| Column | Type | Description | Encoding |
|--------|------|-------------|----------|
| `balance_check_habit` | int | How often respondent checks balance before a UPI transaction | `0` = Never, `1` = Rarely, `2` = Sometimes, `3` = Always. Note: "I check, feel sad, and buy anyway" was mapped to `1` (Rarely) as it reflects low financial control. |
| `tracks_expenses` | int | Whether respondent tracks monthly expenses | `0` = No (includes "I am scared of what I'll find"), `1` = Tries but quits, `2` = Yes |
| `ran_out_of_money` | int | How often respondent runs out of money before month end | `0` = Never, `1` = Rarely, `2` = Occasionally, `3` = Regularly |
| `hidden_purchase` | int | Whether respondent has hidden a purchase from parents/roommate | `0` = No, `1` = Maybe, `2` = Yes |

---

## Section G — Impulse Time Flags

These are binary columns derived from the multi-select `impulse_time` question.  
`1` = this time slot was selected, `0` = not selected.

| Column | Meaning |
|--------|---------|
| `flag_morning` | Makes impulse purchases in the morning |
| `flag_afternoon` | Makes impulse purchases in the afternoon |
| `flag_evening` | Makes impulse purchases in the evening |
| `flag_latenight` | Makes impulse purchases between 10 PM – 2 AM |
| `flag_postmidnight` | Makes impulse purchases after 2 AM |

---

## Section H — Impulse Triggers (Likert Scale)

All trigger columns are on a **1–5 scale** where:  
`1` = Strongly Disagree, `2` = Disagree, `3` = Neutral, `4` = Agree, `5` = Strongly Agree

| Column | Survey Statement |
|--------|----------------|
| `trigger_boredom` | "I make purchases when I'm bored" |
| `trigger_fomo` | "I buy things because my friends bought them (FOMO)" |
| `trigger_latenight` | "Late-night scrolling leads me to buy things" |
| `trigger_cashback` | "I use UPI cashback offers as justification to spend more" |
| `trigger_stress_relief` | "I feel relieved after buying something when stressed" |
| `trigger_scarcity_notif` | "Limited time offers / low stock notifications push me to buy" |
| `trigger_cart_abandon` | "I go back and buy things I left in my cart" |
| `trigger_exam_season` | "I spend more during exam season or stressful academic periods" |

> Note: `trigger_scarcity_notif` and `trigger_cart_abandon` only have values 1–4 in this dataset (no respondent selected 5 for these two).

| Derived Column | Type | Description |
|----------------|------|-------------|
| `impulse_composite_score` | float | Mean of all 8 trigger scores per respondent. Higher = more impulsive overall. Range: 1.0–5.0 |

---

## Section I — Regret Mapping

| Column | Type | Description | Encoding |
|--------|------|-------------|----------|
| `regret_frequency` | int | How many times per month respondent regrets a digital purchase | `0` = Never, `1` = 1-2 times, `2` = 3-5 times, `3` = 5-10 times, `4` = 10+ times |
| `regret_intensity` | int | Respondent's self-rated regret intensity on a 1–10 scale | Raw 1–10 integer. Higher = more intense regret. |
| `high_regret` | int | Binary target variable for ML classification | `1` = `regret_intensity` ≥ 6 (high regret), `0` = `regret_intensity` ≤ 5 (low/moderate). Split: 35 high, 70 low. |
| `post_regret_action` | str | What respondent does after regretting a purchase | `"Accept and move on"`, `"See my expense and feel worse"`, `"Buy Something else to feel better"`, `"Return it"`, `"Tell to friend"` |

---

## Section J — Regret Categories

Binary columns derived from the multi-select `regret_categories` question.  
`1` = this category was selected, `0` = not selected.

| Column | Category |
|--------|---------|
| `cat_food_delivery` | Food delivery (Swiggy / Zomato) |
| `cat_grocery` | Quick commerce (Blinkit / Instamart) |
| `cat_online_shopping` | Online shopping (Myntra, Meesho, Amazon, Flipkart) |
| `cat_subscriptions` | Subscriptions (Netflix, Spotify, Prime) |
| `cat_gaming` | Gaming purchases |
| `cat_gadgets` | Gadgets / Accessories |
| `cat_offline_cafe` | In college cafes and normal shops |
| `cat_other` | Other / unspecified |

---

## Section K — NLP Text

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `regret_combined` | str | Combined open-ended text for NLP. Merges `regret_description` (Q24) and `regret_other_text` (Q23) where available. | Only **23 of 105** respondents filled this. All NLP analysis is based on these 23 responses. |

---

## Summary: Columns Used in ML

| Purpose | Columns |
|---------|---------|
| **K-Means Clustering features** | `impulse_composite_score`, `pct_unplanned_avg`, `avg_weekly_tx`, `regret_intensity`, `regret_frequency`, `balance_check_habit`, `ran_out_of_money`, `hidden_purchase` |
| **Random Forest features** | All clustering features + `flag_morning`, `flag_afternoon`, `flag_evening`, `flag_latenight`, `flag_postmidnight`, `tracks_expenses`, `perceives_upi_risky` |
| **Random Forest target** | `high_regret` |
| **Visualization only (not in ML)** | `age_group`, `gender`, `college_year`, `primary_upi_app`, `income_source`, `source_college`, `upi_usage_reason`, `post_regret_action`, `monthly_budget_range`, `weekly_tx_range`, `pct_unplanned`, all `cat_*` columns |
| **NLP pipeline** | `regret_combined` |
| **Not used anywhere** | `respondent_id` (identifier only) |
