# Agent log

Add a dated entry each time you work with your AI coding agent, with the newest entry at the bottom. Each entry records what you asked the agent, what it produced, and what you checked or changed. Paste your key prompts in exactly as you typed them. Include at least one time the agent got something wrong, and how you caught it.

Copy this outline for each entry:

```markdown
## YYYY-MM-DD: What you worked on

- **Asked:** "Paste your prompt here."
- **Agent produced:** What it made or changed.
- **Checked or changed:** How you checked it, and what you fixed.
```

## 2026-11-10: Median sale price chart and table

- **Asked:** "Read AGENTS.md and docs/descriptions_sheet.md first. Then add a horizontal bar chart of the median sale price for each city above the table on index.html. Keep the table and the $10000 rule as they are."
- **Agent produced:** The agent first found that the file is named `docs/data_description_sheet.md`, and that `index.html` had no table or $10,000 rule. It asked how to proceed. After the answers, it added `scripts/make_city_medians.py`, which writes `data/city_median_sale_price.json` from the CSV with a $10,000 floor. It then rewrote `index.html` with a horizontal bar chart above a table, and added a rebuild note to the README.
- **Checked or changed:** The script's counts match the data sheet: 40 sales under $10,000 are left out, and 35,402 of 35,442 rows are used. In a headless browser at phone width, the page showed 18 bars and 18 table rows, with no script errors and no horizontal scroll. The agent had first hard-coded city and row counts on the page; it changed them to read from the JSON file.
