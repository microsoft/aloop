# Data Analysis & Insights

## Goal
Analyze **[YOUR DATASET or TOPIC, e.g., "customer satisfaction survey results"]**
and produce a complete analysis report with visualizations, insights, and
actionable recommendations for **[YOUR AUDIENCE, e.g., "the product leadership team"]**.

**One-Sentence Summary**:
> [e.g., "This report analyzes 500 survey responses to identify the top pain
> points, segment satisfaction by role, and recommend 3 concrete actions."]

## Success Criteria (in priority order)
- [ ] **Executive summary** — key findings in 5 bullets (NON-NEGOTIABLE, goes first)
- [ ] Summary statistics for all key metrics
- [ ] Segmentation by relevant dimensions (role, region, experience, etc.)
- [ ] Top pain points / opportunities identified and ranked
- [ ] Cross-tabulation to find surprising patterns (not just averages)
- [ ] At least 5 charts (matplotlib code blocks describing each visualization)
- [ ] Actionable recommendations section — specific, not vague
- [ ] Statistical significance notes where applicable
- Score target: 85/100

## Constraints
- Use pandas, numpy for analysis
- Describe charts in detail and provide matplotlib code (container can't render images)
- Output files: artifacts/analysis-report.md, artifacts/analyze.py
- Tables in markdown format

## Instructions to Agent
- IMPORTANT: Write complete files in single write_file calls. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Lead with "so what" — the executive summary should give the reader the answer
  before the methodology. Don't make them dig.
- Look for SURPRISING cross-tabulations, not just averages. "Developers with 5+
  years are less satisfied than juniors" is interesting. "Average satisfaction is
  3.7" is not.
- Every chart must have a clear takeaway in its caption.
- Recommendations must be specific and actionable: "Do X because Y" not "Consider improving Z."
- DO NOT RAMBLE. Analysis should be tight. If a finding doesn't lead to a
  recommendation, cut it.

## Loop Settings
- interval_minutes: 10
- max_iterations: 15
- abort: false
