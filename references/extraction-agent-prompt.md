# Document Extraction Agent Prompt

Use this prompt template when spawning the Haiku agent to extract WinWire content from attached documents.

## Agent Configuration

```
Agent({
  description: "Extract WinWire content from project docs",
  model: "haiku",
  prompt: <see template below>
})
```

## Prompt Template

```
You are extracting content from project documents to build a WinWire — a branded success story combining a deal announcement with a mini case study.

## Your task

Read ALL attached documents and extract the content listed below. Synthesize across documents to find the most compelling version of each item. Prioritize storytelling quality — choose details that make the project's impact vivid and concrete.

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

**Selection logic:**
- **ALWAYS include a `takeaway`** — this is the "so what" that executives scan for
- Prioritize blocks with HARD NUMBERS — sales teams need concrete proof points
- 3-5 blocks is ideal; quality over quantity
- If nothing compelling, return empty blocks array (page 2 will be skipped)

**CRITICAL: Column variety rule**

Left and right columns MUST use different primary block types. Same type on both sides = amateur document. Variety = professional.

```
❌ BAD:   left=highlights, right=highlights    ← monotonous, unprofessional
❌ BAD:   left=metrics, right=metrics          ← no visual contrast
✓ GOOD:  left=takeaway+timeline, right=kpi+comparison
✓ GOOD:  left=takeaway+metrics, right=highlights+proof-points
```

**Block selection decision tree** — match content to block type:

| Content has...                    | Use block type   |
|-----------------------------------|------------------|
| Sequential phases/steps           | `timeline`       |
| Before/after improvements         | `comparison`     |
| One impressive hero number        | `kpi`            |
| Multiple metrics with values      | `metrics`        |
| Executive summary / "so what"     | `takeaway`       |
| Achievements with outcomes        | `highlights`     |
| Certifications / validations      | `proof-points`   |
| Risk + mitigation pairs           | `risks`          |
| Investment → returns breakdown    | `roi`            |

**Recommended pairings for common content:**

| Left column content | Right column content | Left types | Right types |
|---------------------|----------------------|------------|-------------|
| Project phases      | Business outcomes    | `takeaway` + `timeline` | `kpi` + `comparison` |
| Discovery findings  | Results achieved     | `takeaway` + `highlights` | `metrics` + `proof-points` |
| Approach + risks    | Impact + validation  | `takeaway` + `risks` | `kpi` + `proof-points` |

**Column hints:**
- `"column": "left"` — appears in left column
- `"column": "right"` — appears in right column
- Omit column to let the system distribute evenly
- Put `takeaway` or `kpi` in the left column (first thing seen)

**Technology Architecture (separate, fixed section):**
- Always extract tech_architecture as a separate array (not in blocks)
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
    "blocks": [
      // TAKEAWAY — Executive summary (always include if possible)
      {
        "type": "takeaway",
        "column": "left",
        "headline": "Migration delivered 3x ROI in first year while reducing risk",
        "bullets": ["$3.2M annual savings", "Zero security incidents", "40% faster deployments"]
      },

      // KPI — Single hero metric
      {
        "type": "kpi",
        "column": "right",
        "value": "3,800",
        "label": "Transactions/Second",
        "trend": "↑ 217%",
        "context": "vs. 1,200 TPS before migration"
      },

      // METRICS — Multiple numbers with optional delta/context
      {
        "type": "metrics",
        "title": "Business Impact",
        "column": "left",
        "items": [
          {"value": "99.99%", "label": "Uptime", "delta": "↑0.49%", "context": "from 99.5%"},
          {"value": "40%", "label": "Cost Reduction"}
        ]
      },

      // HIGHLIGHTS — Achievements with optional impact badge
      {
        "type": "highlights",
        "title": "Key Achievements",
        "column": "right",
        "items": [
          {"headline": "Zero-Downtime Migration", "detail": "2TB database moved live", "impact": "$0 revenue loss"},
          {"headline": "PCI Compliant", "detail": "Certified in 3 weeks vs typical 3 months"}
        ]
      },

      // COMPARISON — Before/after with change % and timeframe
      {
        "type": "comparison",
        "title": "Transformation",
        "column": "left",
        "items": [
          {"label": "Deployment", "before": "Monthly", "after": "Daily", "change": "30x faster"},
          {"label": "Latency", "before": "1200ms", "after": "180ms", "change": "↓85%", "timeframe": "achieved Q3"}
        ]
      },

      // TIMELINE — Project journey
      {
        "type": "timeline",
        "title": "Project Journey",
        "column": "right",
        "items": [
          {"date": "Q1", "title": "Discovery", "detail": "Mapped 47 services"},
          {"date": "Q2", "title": "Platform Build", "detail": "EKS foundation live"},
          {"date": "Q3", "title": "Migration", "detail": "12 services moved"},
          {"date": "Q4", "title": "Optimization", "detail": "40% cost reduction"}
        ]
      },

      // ROI — Financial breakdown
      {
        "type": "roi",
        "title": "Return on Investment",
        "column": "left",
        "investment": "$1.8M",
        "investment_label": "Total Investment",
        "returns": [
          {"label": "Annual Savings", "value": "$3.2M"},
          {"label": "Risk Avoided", "value": "$800K"}
        ],
        "total_roi": "122%"
      },

      // PROOF-POINTS — Evidence list
      {
        "type": "proof-points",
        "title": "Validated Results",
        "column": "right",
        "items": ["SOC 2 Type II certified", "AWS Well-Architected reviewed", "Zero P1 incidents in 6 months"]
      },

      // RISKS — Risk management
      {
        "type": "risks",
        "title": "Risks Managed",
        "column": "left",
        "items": [
          {"risk": "Data loss during migration", "mitigation": "Blue-green deployment with 3x tested rollback"},
          {"risk": "Performance degradation", "mitigation": "Load tested to 5x peak before cutover"}
        ]
      }
    ],
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
