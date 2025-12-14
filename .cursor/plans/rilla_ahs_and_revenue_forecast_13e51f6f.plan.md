---
name: Rilla AHS and Revenue Forecast
overview: Build an Account Health Score (AHS) model to predict 12-month churn probability and forecast FY26 revenue for existing Rilla customers using behavioral and engagement data from recordings, comments, managers, and sales reps.
todos:
  - id: data-exploration
    content: "Conduct comprehensive data exploration: examine schemas, relationships, missing values, and temporal coverage across all 4 datasets"
    status: pending
  - id: churn-definition
    content: "Define churn outcome variable: identify renewal dates, contract periods, and create 12-month churn labels with proper temporal logic"
    status: pending
  - id: feature-engineering-reps
    content: "Engineer sales rep behavior features: seat utilization, recording frequency, time to first recording, retention metrics, activity trends"
    status: pending
  - id: feature-engineering-managers
    content: "Engineer manager behavior features: onboarding participation, comment frequency/coverage, time to first comment, retention metrics"
    status: pending
  - id: feature-engineering-account
    content: "Create account-level aggregated features: kickoff participation, CRM connection, seats purchased, account age, engagement trends"
    status: pending
  - id: create-modeling-dataset
    content: "Build account-level modeling dataset: join all features, handle missing values, create temporal train/val/test splits"
    status: pending
  - id: train-churn-model
    content: "Train and tune churn prediction model: evaluate baseline and advanced models (XGBoost/LightGBM), optimize hyperparameters"
    status: pending
  - id: model-evaluation
    content: "Evaluate model performance: AUC-ROC, calibration, feature importance, SHAP analysis, segment-level validation"
    status: pending
  - id: calculate-ahs
    content: Calculate Account Health Score (AHS = 1 - churn_prob) for all accounts and create risk tiers
    status: pending
  - id: fy26-revenue-forecast
    content: "Build FY26 revenue forecast: identify active customers, extract renewal dates/ACV, apply churn discounting logic, aggregate results"
    status: pending
  - id: documentation
    content: "Create final deliverables: account-level results table, summary memo with methodology, findings, insights, and recommendations"
    status: pending
  - id: monitoring-framework
    content: "Build monitoring framework: prediction pipeline, performance tracking functions, drift detection, alerting thresholds"
    status: pending
  - id: retraining-pipeline
    content: "Create retraining pipeline: automated data refresh, model retraining workflow, versioning and rollback procedures"
    status: pending
  - id: monitoring-dashboard
    content: "Build monitoring dashboard/reports: weekly/monthly/quarterly performance reports, data quality metrics, business impact tracking"
    status: pending
---

# Rilla Account Health Score & FY26 Revenue Forecast Plan

## Project Overview

Build a machine learning model to predict account-level churn probability (12-month horizon) and use it to:

1. Calculate Account Health Score (AHS = 1 - churn_probability)
2. Forecast FY26 revenue for existing customers by discounting post-renewal revenue by churn probability

## Current State

The Jupyter notebook (`Jupyter/Rilla.ipynb`) has successfully loaded all 4 CSV files:

- **comments_data**: 632,461 rows (ridealong comments)
- **manager_data**: 17,553 rows (manager information)
- **sales_rep_identity**: 61,520 rows (sales rep identity)
- **sales_rep_recordings**: 8,541,723 rows (recording data)

All data is in memory and ready for analysis.

## Implementation Plan

### Phase 1: Data Exploration & Understanding (Week 1-2)

**1.1 Data Quality Assessment**

- Examine schema, data types, and missing values for each dataset
- Identify key join keys: `user_id`, `account_id`, `hubspot_company_id`, `recording_id`, `ridealong_id`
- Check for data quality issues (duplicates, outliers, inconsistencies)
- Understand temporal coverage (date ranges, gaps)

**1.2 Data Relationships**

- Map relationships between datasets
- Identify account-level aggregations needed
- Understand manager-rep-account hierarchies
- Document business logic for key metrics

**1.3 Outcome Variable Definition**

- Define churn based on contract data or unsubscribe events
- Identify renewal dates and contract periods
- Create 12-month churn labels (binary: churned/not churned within 12 months)
- Handle edge cases (mid-term cancellations, expansions, contractions)

### Phase 2: Feature Engineering (Week 2-3)

**2.1 Sales Rep Behavior Features** (from `sales_rep_recordings` and `sales_rep_identity`)

- Seat utilization: active reps / seats purchased
- Recording frequency: recordings per rep per week/month
- Time to first recording after enablement
- Recording activity trends (rolling windows, drop-offs)
- Dn retention metrics (day-N, week-N retention)
- Recording length statistics (avg, median, total)

**2.2 Manager Behavior Features** (from `manager_data` and `comments_data`)

- Manager onboarding participation (live + self-serve)
- Time to first comment after onboarding
- Comment frequency: comments per week/month
- Comment coverage: % of recordings with at least one comment
- Comment engagement: avg comment text length
- Dn retention of commenting activity
- Self-serve onboarding completion rate

**2.3 Account-Level Features** (aggregated across all datasets)

- Kickoff call participation
- CRM connection status and timing
- Total seats purchased over time
- Account age (time since first contract)
- Historical engagement trends
- Account-level recording and commenting aggregates

**2.4 Temporal Features**

- Time-based features (days since onboarding, days since last activity)
- Seasonal patterns
- Growth/decline trends over rolling windows

**2.5 Feature Engineering Implementation**

- Create account-level feature table with all engineered features
- Handle missing values appropriately
- Create train/validation/test splits with temporal considerations
- Ensure no data leakage (features only use historical data)

### Phase 3: Churn Model Development (Week 3-5)

**3.1 Model Selection**

- Start with baseline models (logistic regression, random forest)
- Evaluate gradient boosting (XGBoost, LightGBM) for performance
- Consider ensemble approaches if needed

**3.2 Model Training**

- Train on historical data with proper temporal splits
- Use cross-validation with time-series aware splits
- Tune hyperparameters
- Handle class imbalance if present

**3.3 Model Evaluation**

- Evaluate on holdout test set
- Metrics: AUC-ROC, precision-recall, calibration (Brier score)
- Analyze performance by account segments (size, industry, etc.)
- Validate model calibration (predicted probabilities match actual rates)

**3.4 Model Explainability**

- Feature importance analysis
- SHAP values for model interpretation
- Partial dependence plots for key features
- Identify top drivers of churn risk

### Phase 4: Account Health Score Calculation (Week 5)

**4.1 AHS Definition**

- Calculate AHS = 1 - churn_probability_12m for each account
- Scale to 0-100 range for interpretability
- Create risk tiers (e.g., High/Medium/Low risk)

**4.2 Validation**

- Validate AHS against actual churn outcomes
- Check distribution of scores across accounts
- Identify thresholds for risk categorization

### Phase 5: FY26 Revenue Forecast (Week 6-7)

**5.1 Contract Data Preparation**

- Identify active customers as of reference date
- Extract contract renewal dates
- Get ACV (Annual Contract Value) for each account
- Handle multi-year contracts and expansions

**5.2 Revenue Calculation Logic**

- For revenue before next renewal in FY26: use contracted amount (probability = 1)
- For revenue after renewal in FY26: discount by (1 - churn_probability)
- Example: If renewal is June 1, 2026 and churn_prob = 0.3:
- Jan-Jun 2026 revenue: full ACV × (6/12)
- Jul-Dec 2026 revenue: ACV × (6/12) × (1 - 0.3)

**5.3 Forecast Aggregation**

- Calculate expected revenue per account
- Aggregate by segments (industry, size, risk tier)
- Provide confidence intervals if possible
- Create summary statistics

### Phase 6: Documentation & Deliverables (Week 8)

**6.1 Model Documentation**

- Document model architecture and assumptions
- Feature documentation (definitions, sources, transformations)
- Model performance metrics and validation results
- Limitations and caveats

**6.2 Deliverables**

- Account-level table with: account_id, churn_probability, AHS, expected_FY26_revenue
- Summary memo/slides explaining:
- Methodology
- Key findings and insights
- Top churn risk drivers
- Revenue forecast summary
- Recommendations

**6.3 Code Organization**

- Clean, well-documented code in Jupyter notebook
- Modular functions for reusability
- Clear markdown explanations

## Key Files to Work With

- **Jupyter/Rilla.ipynb**: Main analysis notebook (already has data loaded)
- **rilla_project_context.md**: Project context and requirements

## Technical Considerations

1. **Memory Management**: The recordings dataset is large (4.3GB in memory). Consider:

- Optimizing data types (categoricals, downcast integers)
- Processing in chunks for feature engineering if needed
- Using parquet format for intermediate results

2. **Temporal Validation**: Use time-based splits to avoid look-ahead bias

3. **Feature Engineering Efficiency**: Use vectorized operations and avoid loops where possible

4. **Model Interpretability**: Prioritize explainable models or use SHAP for black-box models

## Success Criteria

- Model achieves reasonable discrimination (AUC-ROC > 0.70, ideally > 0.75)
- Well-calibrated probabilities (Brier score validation)
- Clear, actionable insights on churn drivers
- Accurate FY26 revenue forecast with documented assumptions
- Production-ready code and documentation

## Phase 7: Model Monitoring & Maintenance Strategy

### 7.1 Monitoring Framework Overview

Given Rilla's **1-year subscription model**, churn events primarily occur at renewal dates. This creates a natural evaluation cycle where:

- Predictions are made continuously (weekly/monthly)
- True outcomes are observed at renewal dates (typically 12 months after prediction)
- Model performance can be assessed after each renewal cohort

### 7.2 Key Performance Metrics to Monitor

**7.2.1 Prediction Accuracy Metrics (Primary)**

- **AUC-ROC**: Overall discrimination ability (target: maintain >0.70)
- **Calibration Error (Brier Score)**: How well probabilities match actual rates (target: <0.10)
- **Precision at Top Decile**: Of accounts predicted as highest risk (top 10%), what % actually churn?
- **Recall at Top Decile**: Of all churned accounts, what % were in top 10% risk?
- **Revenue Forecast Accuracy**: Predicted vs actual revenue by renewal cohort

**7.2.2 Business Impact Metrics (Secondary)**

- **Revenue at Risk**: Sum of ACV for accounts in "High Risk" tier
- **False Positive Rate**: Accounts flagged as high risk but didn't churn (CS effort efficiency)
- **False Negative Rate**: Accounts not flagged but churned (missed opportunities)
- **Model-Driven Intervention Success**: Churn rate reduction for high-risk accounts that received CS intervention

**7.2.3 Data Quality Metrics**

- **Feature Completeness**: % of accounts with complete feature sets
- **Data Freshness**: Time since last data update for each feature
- **Missing Value Rates**: Track missingness trends over time
- **Outlier Detection**: Unusual feature values that may indicate data issues

### 7.3 Monitoring Schedule & Frequency

**7.3.1 Weekly Monitoring (Automated)**

- **Prediction Refresh**: Recalculate AHS and churn probabilities for all active accounts
- **Data Quality Checks**: Verify data pipeline integrity, check for missing data spikes
- **Feature Distribution Drift**: Compare current feature distributions vs training baseline
- **Alert Triggers**: Flag if any metric exceeds threshold (see 7.4)

**7.3.2 Monthly Monitoring (Semi-Automated)**

- **Performance Dashboard Review**: Review all KPIs, trends, and alerts
- **Cohort Analysis**: Track performance for accounts by prediction month
- **Feature Importance Stability**: Check if top features remain consistent
- **Revenue Forecast Updates**: Update FY26+ forecasts with latest predictions

**7.3.3 Quarterly Deep Dive (Manual Review)**

- **Model Performance Assessment**: Evaluate predictions vs actuals for accounts that reached renewal
- **Calibration Analysis**: Check if probabilities are still well-calibrated
- **Segment Performance**: Analyze performance by account size, industry, tenure
- **Business Impact Review**: Assess CS intervention effectiveness
- **Retraining Decision**: Determine if model retraining is needed (see 7.5)

**7.3.4 Annual Comprehensive Review**

- **Full Model Re-evaluation**: Complete performance audit
- **Feature Engineering Review**: Assess if new features should be added
- **Model Architecture Review**: Consider if different algorithms would perform better
- **Business Process Review**: Evaluate how AHS is being used and its impact

### 7.4 Alert Thresholds & Triggers

**7.4.1 Performance Degradation Alerts**

- **AUC-ROC drops below 0.65** (from baseline >0.70) → Immediate investigation
- **Calibration error (Brier) increases >0.15** (from baseline <0.10) → Retraining trigger
- **Precision at top decile drops >20%** from baseline → Feature drift investigation
- **Revenue forecast error >15%** for completed renewal cohort → Model review

**7.4.2 Data Quality Alerts**

- **Feature missingness increases >10%** from baseline → Data pipeline check
- **Feature distribution shift (KS statistic >0.2)** → Data drift investigation
- **Data freshness >7 days old** → Pipeline failure alert
- **Outlier rate >5%** → Data quality review

**7.4.3 Business Impact Alerts**

- **False negative rate >30%** (missed churners) → Model sensitivity review
- **High-risk accounts increase >50%** month-over-month → Business trend or model issue?
- **Revenue at risk increases >20%** without business explanation → Investigation

### 7.5 Model Retraining Strategy

**7.5.1 Retraining Triggers (Any of the following)**

1. **Scheduled Retraining (Primary)**

- **Quarterly Retraining**: Every 3 months, retrain with latest 12-18 months of data
- **Post-Renewal Season Retraining**: After major renewal periods (e.g., Q1 if many contracts renew in Q1)
- Rationale: Captures seasonal patterns and recent behavioral changes

2. **Performance-Based Retraining**

- **AUC-ROC drops below 0.65** and remains low for 2 consecutive months
- **Calibration error >0.15** for 2 consecutive renewal cohorts
- **Revenue forecast error >20%** for completed renewal cohort

3. **Data Drift Retraining**

- **Significant feature distribution shift** (KS statistic >0.3 for key features)
- **New feature availability**: When new data sources become available
- **Business model changes**: If Rilla changes pricing, product features, or customer segments

4. **Time-Based Retraining**

- **Annual Full Retrain**: Complete model rebuild with latest data and features
- **After 12 months in production**: Ensure model doesn't become stale

**7.5.2 Retraining Process**

**Step 1: Data Preparation (Week 1)**

- Extract latest data (all 4 CSV files + any new sources)
- Re-run feature engineering pipeline
- Create updated train/validation/test splits with temporal logic
- Validate data quality matches or exceeds original dataset

**Step 2: Model Retraining (Week 1-2)**

- Retrain model with same architecture (or improved if needed)
- Use same hyperparameter tuning approach
- Validate performance on holdout test set
- Compare new model vs current production model

**Step 3: Model Validation (Week 2)**

- **Backtesting**: Evaluate new model on historical periods where we have outcomes
- **A/B Testing Preparation**: If significant changes, prepare for gradual rollout
- **Stakeholder Review**: Present performance comparison and get approval

**Step 4: Model Deployment (Week 2-3)**

- **Shadow Mode** (if major changes): Run new model in parallel for 1 month, compare predictions
- **Gradual Rollout** (if significant changes): Deploy to 10% → 50% → 100% of accounts
- **Full Deployment**: Replace production model, monitor closely for first month

**Step 5: Post-Deployment Monitoring (Ongoing)**

- Enhanced monitoring for first 3 months after deployment
- Compare predictions between old and new model (if shadow mode used)
- Validate that performance improvements hold in production

**7.5.3 Retraining Data Strategy**

Given 1-year subscription cycles:

- **Training Window**: Use 12-18 months of historical data
- **Validation Window**: Last 3-6 months before cutoff date
- **Test Window**: Most recent completed renewal cohort
- **Temporal Splits**: Always use time-based splits (no random splits) to avoid look-ahead bias
- **Minimum Data Requirements**: Need at least 100 churn events for reliable training

### 7.6 Data Drift Detection

**7.6.1 Feature Distribution Drift**

- **Method**: Kolmogorov-Smirnov (KS) test comparing current vs training distributions
- **Frequency**: Weekly automated checks
- **Threshold**: KS statistic >0.2 triggers investigation, >0.3 triggers retraining consideration
- **Key Features to Monitor**: Top 10-15 most important features from model

**7.6.2 Concept Drift Detection**

- **Method**: Monitor prediction accuracy over time for accounts with known outcomes
- **Frequency**: Monthly, after renewal cohorts complete
- **Indicators**: 
- Model performance degrades despite stable feature distributions
- Feature importance shifts significantly
- Business context changes (new product features, market conditions)

**7.6.3 Response to Drift**

- **Minor Drift (KS 0.2-0.3)**: Investigate cause, monitor closely, may adjust feature engineering
- **Moderate Drift (KS 0.3-0.4)**: Plan retraining within 1-2 months
- **Major Drift (KS >0.4)**: Immediate retraining trigger

### 7.7 Model Versioning & Rollback Strategy

**7.7.1 Version Control**

- **Model Artifacts**: Save model files, feature engineering code, and performance metrics
- **Version Naming**: Use semantic versioning (e.g., v1.0.0, v1.1.0 for retrains, v2.0.0 for architecture changes)
- **Metadata Tracking**: Document training date, data cutoff, performance metrics, key changes

**7.7.2 Rollback Criteria**

- **Performance Degradation**: New model performs worse than previous on validation set
- **Production Issues**: New model causes errors or unexpected behavior
- **Business Impact**: New model predictions don't align with business expectations

**7.7.3 Rollback Process**

- Maintain previous model version for 3 months after deployment
- If rollback needed, revert within 24 hours
- Document reason for rollback and plan fix

### 7.8 Implementation Requirements for Monitoring

**7.8.1 Infrastructure Needs**

- **Prediction Pipeline**: Automated weekly/monthly AHS calculation
- **Monitoring Dashboard**: Real-time view of model performance, data quality, alerts
- **Data Storage**: Historical predictions and outcomes for performance tracking
- **Alerting System**: Email/Slack notifications for threshold breaches

**7.8.2 Code Structure for Monitoring**

- **Prediction Function**: Reusable function to generate AHS for all accounts
- **Performance Evaluation Function**: Calculate metrics comparing predictions vs actuals
- **Drift Detection Function**: Automated feature distribution and concept drift checks
- **Reporting Function**: Generate monthly/quarterly performance reports

**7.8.3 Data Pipeline Requirements**

- **Automated Data Refresh**: Weekly extraction of latest data from source systems
- **Data Validation**: Automated checks for data quality, completeness, freshness
- **Feature Engineering Pipeline**: Reproducible feature calculation from raw data
- **Prediction Storage**: Save predictions with timestamps for historical tracking

### 7.9 Success Metrics for Monitoring Program

**7.9.1 Model Health Metrics**

- Model performance maintained within 5% of baseline
- Retraining completed successfully within 3 months of trigger
- Zero unplanned model failures or rollbacks

**7.9.2 Business Value Metrics**

- CS team uses AHS to prioritize accounts (adoption rate)
- Churn reduction in high-risk accounts that received intervention
- Revenue forecast accuracy within 10% for planning purposes
- Time saved in account health assessment (if measurable)

### 7.10 Implementation Notes for Coding Agent

**Critical Instructions for Step-by-Step Implementation:**

1. **Run Each Cell Sequentially**: Execute notebook cells one at a time, examining outputs before proceeding
2. **Validate Intermediate Results**: After each major step (data loading, feature engineering, model training), verify:

- Data shapes and types are as expected
- No unexpected errors or warnings
- Results make business sense

3. **Check for Bugs**: If results seem unexpected:

- Review code logic
- Check data quality
- Validate assumptions
- Document findings and potential plan adjustments

4. **Iterative Refinement**: If data reveals issues not in original plan:

- Document the issue
- Propose solution
- Update approach before proceeding

5. **Save Intermediate Results**: Use pickle/parquet to save:

- Processed datasets
- Feature engineering outputs
- Trained models
- Evaluation results

6. **Documentation**: Add markdown cells explaining:

- What each section does
- Key findings
- Decisions made
- Assumptions and limitations

**Monitoring Implementation Priority:**

- **Phase 1-6**: Build initial model and deliverables
- **Phase 7**: After model is validated, implement monitoring framework:
- Start with basic performance tracking (predictions vs actuals)
- Add automated drift detection
- Build monitoring dashboard/reports
- Set up alerting system