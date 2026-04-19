# Document Extraction Agent Prompt

Use this prompt template when spawning the Haiku agent to extract WinWire content from attached documents.

## Agent Configuration

```
Agent({
  description: "Extract WinWire content from project docs",
  model: "haiku",
  prompt: `
    <paste the template below>
    
    ## Files to read
    
    Read ALL of the following files using the Read tool. Do not skip any.
    
    ${discoveredFiles.map(f => `- ${f}`).join('\n')}
    
    After reading all files, extract the content as specified above.
  `
})
```

**CRITICAL:** The main agent MUST include the full list of discovered file paths in the prompt.
The extraction agent cannot discover files on its own — it can only read paths given to it.

## Prompt Template

```
You are extracting content from project documents to build a WinWire — a branded success story combining a deal announcement with a mini case study.

## TL;DR — read this first

1. **Read EVERY file** listed at the end of this prompt — do not skip any
2. **Quality over quantity** — empty pools are fine, weak content is not
3. **Every item must have CONCRETE details** (numbers, names, dates, specifics)
4. **Prioritize:** executive_insights > hero_metrics > transformations > achievements > rest
5. **If a pool would only have generic content, leave it empty**

## Step 1: Read all files

You will receive a list of file paths at the end of this prompt. You MUST:

1. Use the Read tool to read EVERY file in the list — no exceptions
2. For large files (>500 lines), read in chunks to get full content
3. Track what you've read: mentally check off each file
4. Do NOT proceed to extraction until you have read every file

**Common file locations for key content:**
- Revenue/pricing → SOW, contract, deal desk docs
- Challenge/problem → Executive summary, current state analysis
- Solution/approach → Technical approach, architecture sections
- Metrics/outcomes → Results, KPIs, dashboards, reports
- Quotes → Emails, feedback, NPS surveys, testimonials

## Step 2: Extract content

After reading ALL files, extract the content below. Synthesize across documents to find the BEST version of each item — not all versions, just the most compelling.

## Extraction modes

**Standard mode** (template provided) — User has already provided project identity in template:
- Challenge summary: {challenge_user_highlights}
- Solution summary: {solution_user_highlights}
- Client: {client_name}
- Industry: {industry}
- Partner: {partner}
- Project type: {project_type}

Use these as anchors — find supporting details, metrics, and quotes that reinforce this story.

**Full extraction mode** (`full_extraction: true`) — No template provided. Extract EVERYTHING
from docs, including project identity. Look for:
- **Client name** — SOW headers, footers, contract parties, "prepared for [client]"
- **Industry** — Context clues, regulatory mentions, business domain
- **Partner** — Which cloud? AWS/GCP/Azure service names reveal this
- **Project type** — "migration", "modernization", "platform", "data" in titles/summaries

## Extract these items

### CRITICAL (page 1 — must find or flag as missing)

1. **Revenue figures**
   - Services Revenue / TCV / ACV / deal size (for internal version)
   - Annual Cloud Revenue / ACR / cloud spend (for partner version)
   - Look in: SOW pricing, deal desk docs, partner registrations, executive summaries

2. **Challenge narrative**
   - What problem did the client face? Business impact? Urgency?
   - Find concrete details: system age, scale limits, compliance gaps, cost issues
   - Look in: executive summary, problem statement, current state analysis

3. **Solution narrative**
   - What did CI&T build? Architecture approach? Methodology?
   - Find specifics: patterns used, services deployed, delivery approach
   - Look in: technical approach, proposed solution, architecture sections

4. **Technologies**
   - List ALL specific cloud services, tools, frameworks mentioned
   - e.g., Amazon EKS, Lambda, DynamoDB, Terraform, ArgoCD
   - Look in: architecture docs, technical approach, diagrams (captions)

5. **Client quote**
   - Any direct quote, testimonial, or feedback from client stakeholders
   - Look in: emails, feedback docs, case study drafts, NPS comments

### HIGH (page 1 — strong impact)

6. **Title suggestion**
   - Draft a title with a key metric (e.g., "3x Transaction Throughput")
   - Base it on the most impressive outcome you find

7. **Subtitle suggestion**
   - 2-3 sentence overview of the engagement and results

8. **Tags**
   - Infer from: industry, partner, project type, technologies
   - e.g., ["Cloud Migration", "Microservices", "AWS", "FinTech"]

### MEDIUM (page 2 — flexible content blocks)

Page 2 uses a flexible block system with McKinsey-level presentation standards. Extract
whatever compelling content you find. Prioritize content that helps sales teams sell.

**Block types available (for left/right columns):**

| Type | When to Use | What to Extract | Where to Find |
|------|-------------|-----------------|---------------|
| `takeaway` | Every WinWire should have one | Key insight + supporting bullets | Executive summary, conclusions |
| `kpi` | Single impressive hero metric | Value + trend + context | KPIs, dashboards, results sections |
| `metrics` | Multiple quantitative wins | Value + label + optional delta/context | Performance reports, SLAs |
| `highlights` | Key achievements solved | Headline + detail + optional impact badge | Milestones, deliverables |
| `comparison` | Before/after improvements | Label + before + after + % change + timeframe | Results, improvements |
| `timeline` | Project journey with dates | Date + title + detail per milestone | Project plans, timelines |
| `roi` | Financial value breakdown | Investment + returns + total ROI | Business cases, ROI analyses |
| `proof-points` | Evidence and validations | List of certifications, awards, validations | Compliance docs, certifications |
| `risks` | Risk management | Risk + mitigation pairs | Risk registers, lessons learned |
| `narrative` | Context or methodology | Prose + optional key insight callout | Approach docs, methodologies |
| `quote` | Additional testimonials | Text + author + title + company + role context | Feedback, emails, surveys |

**Extraction guidance for each type:**

1. **takeaway** — The "so what" for executives
   - Look for: Executive summaries, conclusions, "key findings" sections
   - Extract: One bold headline statement + 2-4 supporting bullet points
   - Example: "Migration delivered 3x ROI in year one" with bullets on savings, risk, speed

2. **kpi** — Single hero metric that sells the story
   - Look for: Dashboard screenshots, KPI reports, "headline metrics"
   - Extract: The most impressive single number with trend (↑217%) and context
   - Example: "3,800 TPS" with trend "↑217%" and context "vs 1,200 before"

3. **metrics** — Grid of impressive numbers
   - Look for: Results sections, performance reports, SLAs achieved
   - Extract: Value + label, optionally add delta ("↑32%") and context ("vs industry avg")
   - Example: {"value": "99.99%", "label": "Uptime", "delta": "↑0.49%", "context": "from 99.5%"}

4. **highlights** — Achievement cards with impact
   - Look for: Milestones, deliverables, "key wins" sections
   - Extract: Headline + detail, optionally add impact badge ("$2.1M saved")
   - Example: {"headline": "Zero-Downtime Migration", "detail": "2TB moved live", "impact": "$0 revenue loss"}

5. **comparison** — Before → After transformation
   - Look for: Results tables, improvement metrics, "before/after" comparisons
   - Extract: Label + before + after, optionally add change ("↓85%") and timeframe ("in 6 months")
   - Example: {"label": "Latency", "before": "1200ms", "after": "180ms", "change": "↓85%", "timeframe": "achieved in Q3"}

6. **timeline** — Project journey milestones
   - Look for: Project plans, phase summaries, milestone reports
   - Extract: Date/phase + title + outcome for each milestone
   - Example: {"date": "Q1 2024", "title": "Discovery", "detail": "Mapped 47 services"}

7. **roi** — Financial value story
   - Look for: Business cases, ROI calculations, cost-benefit analyses
   - Extract: Investment amount, returns breakdown, total ROI percentage
   - Example: investment "$1.8M", returns [{"label": "Annual Savings", "value": "$3.2M"}], total_roi "122%"

8. **proof-points** — Evidence that builds credibility
   - Look for: Certifications, compliance docs, awards, third-party validations
   - Extract: List of validations achieved
   - Example: ["SOC 2 Type II certified", "AWS Well-Architected reviewed", "Zero P1 incidents in 6 months"]

9. **risks** — Risk management (shows professionalism)
   - Look for: Risk registers, lessons learned, project retrospectives
   - Extract: Risk + how it was mitigated
   - Example: {"risk": "Data loss during migration", "mitigation": "Blue-green deployment with 3x tested rollback"}

**CRITICAL: Extract BEST content into raw pools (quality over quantity)**

Do NOT select block types or assign columns. Your job is to extract the BEST compelling content
into categorized pools. The main agent will analyze these pools and select the layout.

**Empty pools are fine. Weak content is worse than no content.**

Include multiple items per pool ONLY if each item independently meets the quality bar.

**Pool priority — focus your effort here:**

| Priority | Pool | Why |
|----------|------|-----|
| CRITICAL | `executive_insights` | The "so what" that sells the story |
| CRITICAL | `hero_metrics` | The one number everyone remembers |
| CRITICAL | `transformations` | Before/after proves impact |
| HIGH | `project_phases` | Shows structured delivery |
| HIGH | `achievements` | Concrete wins with impact |
| MEDIUM | `metric_sets` | Supporting numbers |
| MEDIUM | `validations` | Third-party credibility |
| LOW | `financial_analysis` | Rarely complete in docs |
| LOW | `risks_managed` | Only if well-documented |

**Quality bar — only extract content that passes:**

| Pool | MUST have | SKIP if |
|------|-----------|---------|
| `executive_insights` | Bold claim + supporting evidence | Generic ("improved efficiency") |
| `hero_metrics` | Specific number + trend OR context | No number, or number without meaning |
| `metric_sets` | At least 2 concrete values | Single vague metric |
| `achievements` | Headline + concrete detail | Just a title with no substance |
| `transformations` | Before AND after values | Only "after" with no baseline |
| `project_phases` | 3+ phases with outcomes | Just phase names, no details |
| `financial_analysis` | Investment AND at least one return | Only costs, no returns |
| `validations` | Third-party or quantified evidence | Self-reported claims |
| `risks_managed` | Specific risk + specific mitigation | Generic risk statements |

**Examples of GOOD vs BAD content:**

```
❌ BAD metric: "Improved performance"
✓ GOOD metric: {"value": "180ms", "label": "P99 Latency", "trend": "↓85%", "context": "from 1,200ms"}

❌ BAD achievement: {"headline": "Successful migration", "detail": "Completed on time"}
✓ GOOD achievement: {"headline": "Zero-Downtime Migration", "detail": "2TB database moved live", "impact": "$0 revenue loss"}

❌ BAD transformation: {"label": "Speed", "before": "Slow", "after": "Fast"}
✓ GOOD transformation: {"label": "Deployment", "before": "Monthly", "after": "Daily", "change": "30x faster"}

❌ BAD insight: "The project was successful and met all objectives"
✓ GOOD insight: {"headline": "AI cuts discovery from months to weeks", "bullets": ["60% context pre-captured", "4 parallel tracks", "9 OpCos unified"]}
```

**Raw content pools to populate:**

| Pool | What to extract | Where to find it |
|------|-----------------|------------------|
| `executive_insights` | Bold headline + 2-4 supporting bullets | Executive summaries, conclusions |
| `hero_metrics` | Single number + trend + context | KPI dashboards, headline metrics |
| `metric_sets` | Multiple concrete values with labels | Performance reports, SLAs |
| `achievements` | Headline + detail + optional impact badge | Milestones, deliverables |
| `transformations` | Before + after + % change | Results tables, comparisons |
| `project_phases` | Date/phase + title + outcome | Project plans, timelines |
| `financial_analysis` | Investment + returns + ROI | Business cases, cost-benefit |
| `validations` | Third-party evidence, certifications | Compliance docs, reviews |
| `risks_managed` | Specific risk + specific mitigation | Risk registers, retrospectives |

**CRITICAL: Content limits — keep page 2 scannable in 30 seconds**

Page 2 must NOT be a wall of text. Apply these hard limits:

| Element | MAX items | Text limit |
|---------|-----------|------------|
| `executive_insights` | 1 insight | Headline ≤12 words, bullets ≤3, each ≤8 words |
| `hero_metrics` | 2 metrics | Pick the 2 most impressive |
| `metric_sets` | 4 metrics | Only concrete numbers |
| `achievements` | 3 items | Detail ≤10 words each |
| `transformations` | 2 items | Keep even grid (2 or 4) |
| `project_phases` | 4 phases | Detail ≤10 words each |
| `validations` | 4 items | Short phrases only |
| `risks_managed` | 2 pairs | Mitigation ≤12 words |

**If you have more content than the limits allow, SELECT THE BEST — don't include everything.**

The main agent will build maximum 2 blocks per column. Your raw pools provide options, not a dump.

**Technology Architecture (separate, fixed section):**
- Always extract tech_architecture as a separate array
- This renders as a fixed 3x2 card grid at the bottom of page 2
- Group by: Compute, Data, Events, Security, Observability, CI/CD

## Output format

Return valid JSON only — no markdown, no explanation:

{
  "project_identity": {
    "client_name": "Extracted client name (full extraction mode only)",
    "industry": "Inferred industry",
    "partner": "aws|gcp|azure (based on services mentioned)",
    "project_type": "e.g., Cloud Migration, Data Platform"
  },
  "revenue": {
    "services_revenue": "$X.XM or null if not found",
    "acr": "$X.XM or null if not found"
  },
  "challenge": {
    "headline": "Short punchy headline",
    "body": "2-4 sentences with concrete details"
  },
  "solution": {
    "headline": "Short punchy headline",
    "body": "2-4 sentences with specifics",
    "technologies": ["Service1", "Service2", "..."]
  },
  "quote": {
    "text": "The quote text or null",
    "author": "Name or null",
    "title": "Role or null"
  },
  "title": "Suggested title with metric",
  "subtitle": "2-3 sentence overview",
  "tags": ["Tag1", "Tag2", "..."],
  "page2": {
    "include": true,
    "title": "Deep Dive: [Client] [Project Type]",

    // RAW CONTENT POOLS — extract BEST content that meets quality bar
    // Empty pools are OK — weak content is worse than no content
    "raw": {
      "executive_insights": [
        // The "so what" with supporting evidence
        {
          "headline": "Migration delivered 3x ROI in first year",
          "bullets": ["$3.2M annual savings", "Zero security incidents", "40% faster deployments"]
        }
      ],

      "hero_metrics": [
        // Only impressive numbers with trend + context
        {"value": "3,800", "label": "Transactions/Second", "trend": "↑217%", "context": "vs 1,200 before"}
      ],

      "metric_sets": [
        // Multiple concrete values (skip if <2)
        {"value": "40%", "label": "Cost Reduction", "context": "infrastructure spend"},
        {"value": "$1.2M", "label": "Annual Cloud Revenue"}
      ],

      "achievements": [
        // Concrete accomplishments with real detail
        {"headline": "Zero-Downtime Migration", "detail": "2TB database moved live", "impact": "$0 revenue loss"}
      ],

      "transformations": [
        // Before AND after required
        {"label": "Deployment", "before": "Monthly", "after": "Daily", "change": "30x faster"},
        {"label": "P99 Latency", "before": "1200ms", "after": "180ms", "change": "↓85%"}
      ],

      "project_phases": [
        // 3+ phases with outcomes
        {"date": "Q1", "title": "Discovery", "detail": "Mapped 47 services"},
        {"date": "Q2", "title": "Platform Build", "detail": "EKS foundation live"},
        {"date": "Q3", "title": "Migration", "detail": "12 services moved"},
        {"date": "Q4", "title": "Optimization", "detail": "40% cost reduction achieved"}
      ],

      // Empty — no complete ROI data found (this is OK)
      "financial_analysis": null,

      "validations": [
        // Third-party evidence only
        "SOC 2 Type II certified",
        "AWS Well-Architected reviewed"
      ],

      // Empty — no documented risk/mitigation pairs found (this is OK)
      "risks_managed": []
    },

    "tech_architecture": [
      {"category": "Compute", "description": "Amazon EKS with Karpenter auto-scaling"},
      {"category": "Data", "description": "DynamoDB for transactions, S3 for analytics"},
      {"category": "Events", "description": "EventBridge for async messaging"},
      {"category": "Security", "description": "KMS encryption, IAM roles, VPC isolation"},
      {"category": "Observability", "description": "CloudWatch, X-Ray distributed tracing"},
      {"category": "CI/CD", "description": "GitOps with ArgoCD, GitHub Actions"}
    ]
  },
  "missing": ["List any CRITICAL items you could not find"]
}
```

## Handling Results

After the agent returns:

1. **Merge with template data** — template values (user input) take priority over extracted values
2. **Check `missing` array** — if CRITICAL items missing, ask user directly
3. **Review narratives** — the agent drafts headlines/body; you refine for WinWire tone
4. **Fill gaps** — use extracted data to enhance user's challenge/solution highlights

### Processing page2.raw pools → final blocks

The agent returns raw content pools in `page2.raw`. You must:

1. **Score each pool** for content quality:
   - Has concrete numbers? → strong candidate for `kpi`, `metrics`, `comparison`
   - Has before/after? → strong candidate for `comparison`
   - Has dates/phases? → strong candidate for `timeline`
   - Has executive summary? → strong candidate for `takeaway`
   - Multiple items? → more options to choose from
   - Empty or weak? → skip this pool

2. **Select block types** based on strongest content:

   | Pool | Best block type | Fallback |
   |------|-----------------|----------|
   | executive_insights | `takeaway` | — (always use if present) |
   | hero_metrics | `kpi` | `metrics` |
   | metric_sets | `metrics` | `highlights` |
   | achievements | `highlights` | `proof-points` |
   | transformations | `comparison` | `metrics` |
   | project_phases | `timeline` | `highlights` |
   | financial_analysis | `roi` | skip if incomplete |
   | validations | `proof-points` | `highlights` |
   | risks_managed | `risks` | skip if <2 items |

3. **Assign columns with variety**:
   - Left column: prioritize `takeaway`, `timeline`, `roi`, `risks`
   - Right column: prioritize `kpi`, `comparison`, `metrics`, `proof-points`
   - **NEVER same primary block type on both sides**

4. **Present layout options to user** before building:
   ```
   Recommended page 2 layout:
   
   LEFT COLUMN:
   ├─ takeaway: "[headline]" + 3 bullets
   └─ timeline: [N] project phases
   
   RIGHT COLUMN:
   ├─ kpi: "[value]" [label] ([trend])
   └─ comparison: [N] before/after items
   
   Available alternatives:
   • Could swap timeline → highlights ([N] achievements available)
   • Could add proof-points: [N] validations found
   • risks block available: [N] risk/mitigation pairs
   
   Use recommended layout, or customize?
   ```

5. **Build final blocks array** only after user approves layout
