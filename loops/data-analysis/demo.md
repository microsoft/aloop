# Data Analysis Demo — Developer Survey Insights

## Goal
Generate a synthetic developer survey dataset (500 respondents) and produce a
complete analysis report with visualizations, insights, and recommendations for
the Azure AI platform team.

**One-Sentence Summary**:
> An analysis of 500 developer survey responses revealing which Azure AI features
> drive satisfaction, where the biggest pain points are, and what to prioritize next.

## Success Criteria (in priority order)
- [ ] **Executive summary** — top 3 findings + recommendations in 1 page (NON-NEGOTIABLE, goes first)
- [ ] Python script generating realistic survey data (500 respondents)
- [ ] Summary statistics for all questions
- [ ] Segmentation by role (PM, Developer, DevRel) and experience level
- [ ] Top pain points identified and ranked
- [ ] Correlation analysis between satisfaction and feature usage
- [ ] At least 5 charts (matplotlib code blocks with descriptions)
- [ ] Cross-tabulations that reveal surprises — not just averages
- [ ] Actionable recommendations: "Do X because Y"
- Score target: 85/100

## Constraints
- Use pandas, numpy for analysis
- Output files: artifacts/survey-analysis.md, artifacts/generate_data.py, artifacts/analyze.py
- Describe charts in detail with matplotlib code blocks
- Format tables in markdown

## Instructions to Agent
- IMPORTANT: Write EACH file in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Lead with "so what" — the executive summary should have the recommendations,
  not just the findings.
- Make the synthetic data realistic: satisfaction scores (1-10), NPS, feature
  usage frequency, open-ended pain points, role/experience segmentation.
- Include at least 10 survey questions.
- Look for surprising cross-tabulations, not just averages. "Senior devs are
  2x more likely to report deployment friction" is insight. "Average satisfaction
  is 7.2" is not.
- DO NOT RAMBLE. Every chart must have a "so what" caption.

## Loop Settings
- interval_minutes: 10
- max_iterations: 15
- abort: false
