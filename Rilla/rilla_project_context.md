# Rilla – Account Health Score & FY26 Revenue Forecast
_Context doc compiled from ChatGPT discussion with Winston (PEAKUP GLOBAL INC)._

---

## 1. Project Background

**Company:** Rilla (AI-powered virtual ridealong platform for outside sales and field service teams)  
**Consultant:** PEAKUP GLOBAL INC (Winston)  
**Timeframe:** Modeling work targeted to support FY26 (Jan 2026 – Dec 2026) planning for Rilla.

### 1.1 What Rilla Does (high level)

- Rilla is a **virtual ridealong software platform** for **outside sales and service teams** (HVAC, plumbing, home improvement, etc.).  
- Reps and technicians use a **mobile app** to record **in‑person customer conversations**.  
- Rilla uses **AI + speech analytics** to:
  - Transcribe and analyze conversations  
  - Surface insights and coaching opportunities  
  - Enable managers to review and comment on calls asynchronously  
- Goal: make physical ridealongs **“100× faster, better, more productive”** for coaching and performance management.

### 1.2 Business Model Summary

- B2B **SaaS**, subscription model.  
- Pricing: customer-reported estimates are **$4,000+ per user per year**, annual commitment, minimum ~5 users.  
- One‑time **implementation/onboarding fee**: typically \$1.5k–\$5k depending on size/complexity.  
- Revenue mainly from:
  - Per‑seat SaaS licenses  
  - Implementation fees  
- Customers: mid‑sized to large home‑service & field‑service companies (HVAC, plumbing, electrical, home improvement, etc.).  
  - Example brands: LongHome Products, Mister Sparky, Benjamin Franklin Plumbing, One Hour Heating & Air Conditioning, A1 Garage, etc.  
- Estimated annual revenue range (public sources): **\$10–\$25M** with **1,500+ contractor customers**.

### 1.3 Why Churn & Revenue Prediction Matter

Because per‑seat pricing is high, **churn of even a single multi‑seat customer** (e.g., 10–200 reps) has a large impact on ARR. Rilla’s value proposition is revenue lift & sales efficiency, so **perceived ROI and product adoption** directly impact retention and upsell.

The CEO (Sebastian Jimenez) wants to understand:

> “How does engagement with the ridealong features (recording + manager commenting) predict long‑term revenue retention, and what revenue should we expect from existing customers in FY26?”

---

## 2. High-Level Modeling Framing

### 2.1 Key Question

> Looking at user behavior, especially ridealong engagement, how does it predict long‑term customer health and FY26 revenue from existing customers?

### 2.2 Core Modeling Objects

1. **Account‑level churn probability (12‑month horizon).**  
2. **Account Health Score (AHS):**  
   - Defined as `AHS = 1 − P(churn in next 12 months)`  
   - Scaled to [0, 1] or [0, 100].  
3. **FY26 expected revenue for each existing customer**, derived by combining:
   - Contract data (renewal dates, ACV)  
   - AHS / churn probability as a discount factor  
4. **(Later / optional)**: productionization of AHS and use in CS workflows.

---

## 3. Sebastian Meeting Notes (Structure of Rilla’s Process)

Meeting with Sebastian (CEO) in Nov 2025 – main process outline:

### 3.1 Timeline of Customer Journey

1. **Kickoff Call (around April 2024 example)**  
   - Participants: Account owner, managers, Rilla CS.  
   - Agenda: CRM connection, sales scripts, expectations.

2. **Sales Reps Enablement**  
   - Participants: Rilla CS, sales reps, managers.  
   - Focus: enabling reps to use the app & recording feature.  
   - Data signals:
     - Number of **sales IDs created (voice recognition)** vs **seats purchased**.  
     - Reps begin **recording real field conversations**.  
     - Metrics:
       - Adoption rate.  
       - Time from recognition → first recording.  
       - Dn retention of rep usage (day‑N / week‑N).

3. **Ridealong Onboarding (typically ~1 week after enablement)**  
   - Participants: managers, Rilla CS.  
   - Goal: teach managers to use **ridealong commenting** to coach reps.  
   - Metrics:
     - Number of managers onboarded (e.g., WhatsApp/WA group).  
     - Manager onboarding participation rate.  
     - Time to first ridealong use (first comment).  
     - % of recordings that receive a manager comment.  
     - Dn retention for manager commenting activity.  
   - Problem: managers often **don’t show up** to the live onboarding call, causing low onboarding and low later commenting.

4. **Self‑Serve Onboarding (for managers)**  
   - Designed to **increase manager onboarding rate** without scheduling constraints.  
   - Flow: manager can onboard at any time; system presents a **fake recording** and an **auto‑generated comment**, so they learn by practicing how to leave comments / feedback.  
   - Purpose: get managers comfortable with commenting workflows (so they later coach on real field visits).  
   - Key metrics:
     - Whether manager used self‑serve onboarding.  
     - Completion state & timestamps.  
     - Time from enabling self‑serve → completion.  
     - Transition: self‑serve completion → first real comment on an actual recording.

5. **Weekly Check‑Ins (historically used, possible revival)**  
   - CS pokes managers weekly to ensure they leave comments, review recordings, etc.  
   - These check‑ins were paused and may be restarted.  
   - Events here can be modeled as **CS interventions**.

### 3.2 Ridealong Feature Definition

Ridealong feature has **two sides**:

1. **Reps recording** their field interactions.  
2. **Managers making comments** to provide feedback/coaching on those recordings.

Success requires both sides to be adopted.

---

## 4. Analytical & ML Solution Concepts (From Conversation)

### 4.1 Multi-Layer ML Design

1. **Account Health Score (AHS) Model**
   - Inputs: behavioral and contextual features.
   - Output: churn probability and AHS.

2. **Revenue Forecast for FY26 (Existing Customers Only)**
   - Uses churn probabilities as discount factors on post‑renewal revenue.
   - Aggregates expected revenue across all accounts.

3. **(Future) AHS Operationalization & CS Use Cases**
   - Weekly refresh of health scores.  
   - CS dashboards and playbooks.  
   - Additional models (expansion propensity, CLV, etc.).

### 4.2 Example Feature Categories

**Sales rep behavior:**
- # of sales IDs created vs seats purchased.  
- Rep enablement meeting participation.  
- Time to first recording after enablement.  
- Frequency of recordings per rep (weekly, monthly).  
- Dn retention curves for recording usage.  
- Seat utilization (active reps / seats purchased).  
- Drop in activity over rolling windows.

**Manager behavior:**
- Manager onboarding participation (live and/or self‑serve).  
- Time to first comment.  
- # comments per recording / per week.  
- % of recordings that receive at least one comment.  
- Dn retention of commenting activity.  
- Use of self‑serve onboarding flows and completion.

**Account-level signals:**
- Kickoff call participation.  
- CRM connected flag + timestamp.  
- Number of seats purchased, purchase timestamps.  
- Contract start and end dates.  
- Contract value (ACV), expansions/contractions.  
- Unsubscribe events / non‑renewal.

**CS/support/intervention signals (if available):**
- Weekly CS check‑ins, email nudges, etc.  
- Support tickets and resolution.

---

## 5. Data Requirements Draft (from Diagram)

The sketch in the conversation breaks down data into four logical blocks:

1. **Global event fields**
2. **Manager data**
3. **Sales rep data**
4. **Account owner (account-level) data**

### 5.1 Global Event Fields

Requested fields:

- `ts`: timestamp of event.  
- `$`: revenue (or amount, as appropriate).  
- `txn`: transaction quantity (e.g., # transactions).  
- `imp`: impression events (e.g., view events on features).  
- `clk`: click events (employee list click, comment typing starts, emoji click, comment submit, etc.).

These define the basic structure for clickstream and engagement logs.

### 5.2 Manager Data

Key fields listed in draft:

- `user_id`  
- `login_ts`  

Onboarding / self‑serve:

- `onboarding_appointment_ts`  
- `onboarding_participated_meeting_ts`  
- `onboarding_participated_meeting_duration`  
- `self_serve_onboarding_comp_milestone_ts` (for completion rate)  

Self‑serve onboarding feature usage:

- `self_serve_onboarding_imp_with`
  - `feature_1_ts`
  - `feature_2_ts`
  - `feature_3_ts`
- `self_serve_onboarding_clk_with`
  - `feature_1_ts`
  - `feature_2_ts`
  - `feature_3_ts`

Ridealong commenting:

- `ridealong_comment_id`  
- `ridealong_comment_ts`  
- `ridealong_comment_text_content` (ideally raw text; if not, length proxy).  

Ridealong click events:

- `ridealong_imp_with`  
  - `feature_1_ts` / `feature_2_ts` / `feature_3_ts` …  
- `ridealong_clk_with`  
  - `feature_1_ts` / `feature_2_ts` / `feature_3_ts` …  

### 5.3 Sales Reps Data

Fields listed:

- `user_id`  
- `enablement_meeting_appointment_ts`  
- `enablement_meeting_participation_ts`  
- `sales_ids_generated_ts` (voice recognition IDs)  
- `recording_ts`  
- `recording_end_ts`  
- Recording & commenting join keys:
  - `recording_id`  
  - `ridealong_comment_id`  
  - `ridealong_comment_ts`  
  - `ridealong_comment_text_content` (or length).

### 5.4 Account Owner / Account-Level Data

Fields listed:

- `seat_purchase_ts` (multiple if incremental)  
- `seat_purchase_txn` (count)  
- `seat_purchase_amount` (if available)  

Kickoff:

- `kickoff_call_appointment_ts`  
- `kickoff_call_connected_ts`  
- `kickoff_call_participations` (# attendees / presence)  
- `CRM_connected_ts`  
- `sales_scripts` (config indicators)  

Churn / unsubscribe:

- `unsubscribed_ts`  
- `unsubscribed_txn`  
- `unsubscribed_amount` (lost revenue).  

These will be combined later with contract structures & ACV to define true churn and revenue outcomes.

---

## 6. Statement of Work (SOW) – Key Points

A draft SOW was created in the conversation (not pasted verbatim here but summarized). Core components:

### 6.1 Objectives

- Build an ML model to estimate **12‑month churn probability** per account and thus AHS.  
- Use churn probabilities as discount factors to forecast **FY26 revenue for existing customers**.

### 6.2 AHS Definition

- `AHS = 1 − churn_probability_12m`  
- Output as continuous score 0–1 or 0–100.  

### 6.3 FY26 Revenue Forecast Method (Existing Customers Only)

- Consider only customers with active contracts as of reference date.  
- Revenue prior to next renewal date in 2026 is treated as **contracted** (probability 1).  
- For revenue **after** next renewal date within FY26, discount by `(1 − churn_probability)`.

**Example:**  
- Customer contract value for post‑renewal FY26 period = \$500k.  
- Renewal date: 1 June 2026.  
- Churn probability for that renewal = 0.5.  
- Expected post‑renewal revenue for FY26 = \$500k × (1 − 0.5) = \$250k.

This logic is valid under assumptions:
- Churn is primarily at renewal.  
- Contracts are annual with clear renewal boundaries.  
- Mid‑term cancellations either rare or separately modeled.

### 6.4 Phases

1. **Phase 1 – Discovery & Data Preparation (2–3 weeks)**  
   - Confirm data availability and quality.  
   - Build account‑level modeling dataset.

2. **Phase 2 – AHS / Churn Model (3–4 weeks)**  
   - Design, train and evaluate model.  
   - Explainability (feature importance, SHAP, partial dependence).

3. **Phase 3 – FY26 Revenue Forecast (2–3 weeks)**  
   - Apply AHS to forecast account‑level FY26 revenue.  
   - Aggregate to totals & segments.  
   - Provide documentation and final readout.

Total expected project duration: **approximately 8 weeks** from data availability (adjustable).

### 6.5 Deliverables (Current SOW Version)

- Data schema and modeling dataset description.  
- Trained AHS model (with documentation).  
- Account‑level table with:
  - Account ID  
  - Churn probability  
  - AHS  
  - Expected FY26 revenue  
- Summary memo / slide‑style explanation of assumptions, results, and insights.

### 6.6 Out of Scope

- No dashboards.  
- No productionization / serving pipelines.  
- No UI integration in Rilla’s product.  
- No ongoing model monitoring.  
- (Future phase may cover these.)

---

## 7. Pricing & Timeline Guidance (For Winston’s Internal Use)

From discussion:

- **Likely pricing range** for a project of this scope, by a senior solo consultant:
  - Lean MVP: \$35k–\$50k.  
  - Standard (recommended): \$60k–\$90k.  
  - Premium/boutique: \$100k–\$150k.

- Per‑hour implied rate: \$175–\$300/hr.  
- Estimated effort: ~250–350 hours.

**Timeline rough plan (standard):**

- Weeks 1–2: Discovery & data prep.  
- Weeks 3–5: AHS model.  
- Weeks 6–8: FY26 revenue forecast & final readout.

---

## 8. Future / Optional Scope Ideas (Not in Current SOW)

The following potential follow‑on work was identified:

1. **Productionization of AHS**
   - Weekly recalculation of churn probabilities and AHS in Rilla’s data stack.  
   - Integration into CRM/CS tooling.

2. **Customer Success Use Cases**
   - Health‑score–based prioritization of accounts for outreach.  
   - Playbooks triggered by specific driver patterns (e.g., “low manager commenting, high rep recording”).

3. **Scenario / What‑If Tools**
   - Estimate revenue impact if ridealong metrics (e.g., comments per recording, manager onboarding rate) improve by X%.  

4. **Additional Models**
   - Expansion propensity model.  
   - Full customer lifetime value (CLV) estimation.  
   - Segmented benchmarks by industry, company size, region, etc.

5. **Dashboards (future SOW)**
   - Executive and CS dashboards for AHS, churn risk, and revenue at risk.

---

## 9. Pending Items / Next Steps

At the time of this compilation:

1. Rilla engineering is expected to provide:
   - Manager data file (`manager_data.csv`)  
   - Sales rep identity data (`sales_rep_identity.csv`)  
   - Plus other data extracts as per spec.

2. Winston’s plan is to:
   - Inspect real data to assess complexity of feature engineering.  
   - Then finalize SOW with concrete pricing and timeline.

3. Current communication plan:
   - Inform CEO that SOW + quote will follow **a few days after** data access and initial review.

You can now use this document as context in Cursor or a local Jupyter notebook while building the models, feature engineering, and final deliverables.
