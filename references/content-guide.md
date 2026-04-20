# WinWire Content Guide

## JSON Data Structure

The build_html.py script expects a JSON file with this structure. All fields marked with
`*` are required for page 1. The rest are optional (page 2 or nice-to-have).

```json
{
  "project": {
    "client_name": "NovaPay",              // * or anonymized_name if anonymized
    "anonymized_name": "A Leading FinTech Company",
    "anonymize": false,
    "industry": "Financial Services",       // *
    "partner": "aws",                       // * one of: aws, gcp, azure
    "project_type": "Cloud Migration",      // *
    "title": "Cloud-Native Transformation Unlocks 3x Transaction Throughput",  // * SHARED
    "subtitle_internal": "CI&T landed a $3.2M engagement to migrate NovaPay's payment platform to AWS...",  // * for CI&T audience
    "subtitle_partner": "AWS-powered migration tripled NovaPay's transaction capacity, unlocking $1.2M ACR...",  // * for Partner audience
    "subtitle": "...",  // legacy fallback if version-specific not provided
    "tags": ["Cloud Migration", "Microservices", "AWS", "FinTech"]  // * SHARED
  },

  "challenge": {
    "headline": "A monolith blocking growth",    // * SHARED
    "body_internal": "NovaPay's 12-year-old monolith couldn't scale past 1,200 TPS — a $3.2M modernization opportunity for CI&T.",  // * CI&T angle
    "body_partner": "NovaPay's 12-year-old monolith couldn't scale past 1,200 TPS — blocking $1.2M in AWS consumption potential.",  // * Partner angle
    "body": "..."  // legacy fallback
  },

  "solution": {
    "headline": "Event-driven microservices on AWS",  // * SHARED
    "body_internal": "CI&T designed a cloud-native architecture on EKS, enabling premium pricing through our microservices expertise...",  // * CI&T angle
    "body_partner": "AWS services powered the transformation — EKS, Lambda, DynamoDB, EventBridge driving $1.2M ACR...",  // * Partner angle
    "body": "...",  // legacy fallback
    "technologies": ["Amazon EKS", "AWS Lambda", "DynamoDB", "EventBridge", "Step Functions", "CloudFront"]  // * SHARED
  },

  "metrics_internal": {
    "items": [
      {"value": "$3.2M", "label": "Services Revenue"},           // *
      {"value": "$280K", "label": "Incentive Funding (MAP 2.0)"}, // *
      {"value": "94 days", "label": "Deal Cycle"}                 // *
    ]
  },

  "metrics_partner": {
    "items": [
      {"value": "$1.2M", "label": "Annual Cloud Revenue"},
      {"value": "40%", "label": "Infrastructure Cost Reduction"},
      {"value": "6 AWS Services", "label": "Core Services Adopted"}
    ]
  },

  "quote": {
    "text": "CI&T didn't just migrate our platform...",  // *
    "author": "Marcus Chen",                              // *
    "title": "CTO",                                       // *
    "company": "NovaPay"                                   // *
  },

  "context_bar_internal": [
    {"label": "Incentive Program", "value": "AWS MAP 2.0"},
    {"label": "Funding Received", "value": "$280K"},
    {"label": "Deal Cycle", "value": "94 Days"},
    {"label": "Delivery Team", "value": "18 People"}
  ],

  "context_bar_partner": [
    {"label": "Incentive Program", "value": "AWS MAP 2.0"},
    {"label": "Funding Received", "value": "$280K"},
    {"label": "Deal Cycle", "value": "94 Days"},
    {"label": "Delivery Timeline", "value": "9 Months"}
  ],

  // ═══════════════════════════════════════════════════════════════════════
  // PAGE 2 — RAW CONTENT POOLS (returned by extraction agent)
  // ═══════════════════════════════════════════════════════════════════════
  // The extraction agent returns raw content pools. The main agent analyzes
  // these and selects the best layout with visual variety between columns.
  //
  // Pool → Block type mapping:
  //   executive_insights → takeaway
  //   hero_metrics       → kpi
  //   metric_sets        → metrics
  //   achievements       → highlights
  //   transformations    → comparison
  //   project_phases     → timeline
  //   financial_analysis → roi
  //   validations        → proof-points
  //   risks_managed      → risks

  "page2_raw_example": {
    "executive_insights": [
      {"headline": "Migration delivered 3x ROI", "bullets": ["$3.2M savings", "Zero incidents", "40% faster"]}
    ],
    "hero_metrics": [
      {"value": "3,800", "label": "TPS", "trend": "↑217%", "context": "vs 1,200 before"}
    ],
    "metric_sets": [
      {"value": "99.99%", "label": "Uptime", "delta": "↑0.49%"},
      {"value": "40%", "label": "Cost Reduction"}
    ],
    "achievements": [
      {"headline": "Zero-Downtime Migration", "detail": "2TB moved live", "impact": "$0 loss"}
    ],
    "transformations": [
      {"label": "Latency", "before": "1200ms", "after": "180ms", "change": "↓85%"}
    ],
    "project_phases": [
      {"date": "Q1", "title": "Discovery", "detail": "Mapped 47 services"}
    ],
    "financial_analysis": {
      "investment": "$1.8M",
      "returns": [{"label": "Annual Savings", "value": "$3.2M"}],
      "total_roi": "122%"
    },
    "validations": ["SOC 2 certified", "AWS Well-Architected reviewed"],
    "risks_managed": [
      {"risk": "Data loss", "mitigation": "Blue-green deployment with rollback"}
    ]
  },

  // ═══════════════════════════════════════════════════════════════════════
  // PAGE 2 — FINAL BLOCKS FORMAT (after main agent selects layout)
  // ═══════════════════════════════════════════════════════════════════════
  // After analyzing raw pools, the main agent builds this blocks array.
  // ALWAYS include a "takeaway" block (the executive "so what").
  // Prioritize blocks with hard numbers. 3-5 blocks is ideal.
  // NEVER use the same primary block type in both columns.

  "page2": {
    "include": true,
    "title": "Deep Dive: NovaPay Cloud Migration",
    "blocks": [

      // ─── TAKEAWAY — Executive summary "so what" (always include!) ───
      {
        "type": "takeaway",
        "column": "left",
        "headline": "Migration delivered 3x ROI in first year while reducing risk",
        "bullets": ["$3.2M annual savings", "Zero security incidents", "40% faster deployments"]
      },

      // ─── KPI — Single hero metric with trend ───
      {
        "type": "kpi",
        "column": "right",
        "value": "3,800",
        "label": "Transactions/Second",
        "trend": "↑ 217%",
        "context": "vs. 1,200 TPS before migration"
      },

      // ─── METRICS — Grid of numbers with optional delta/context ───
      {
        "type": "metrics",
        "title": "Business Impact",
        "column": "left",
        "items": [
          {"value": "99.99%", "label": "Uptime", "delta": "↑0.49%", "context": "from 99.5%"},
          {"value": "40%", "label": "Cost Reduction", "context": "infrastructure spend"}
        ]
      },

      // ─── HIGHLIGHTS — Achievements with optional impact badge ───
      {
        "type": "highlights",
        "title": "Key Achievements",
        "column": "right",
        "items": [
          {"headline": "Zero-Downtime Migration", "detail": "2TB database moved live", "impact": "$0 revenue loss"},
          {"headline": "PCI Compliant", "detail": "Certified in 3 weeks vs typical 3 months"}
        ]
      },

      // ─── COMPARISON — Before/after with % change and timeframe ───
      {
        "type": "comparison",
        "title": "Transformation",
        "column": "left",
        "items": [
          {"label": "Deployment", "before": "Monthly", "after": "Daily", "change": "30x faster"},
          {"label": "P99 Latency", "before": "1,200ms", "after": "180ms", "change": "↓85%", "timeframe": "achieved Q3"}
        ]
      },

      // ─── TIMELINE — Project journey milestones ───
      {
        "type": "timeline",
        "title": "Project Journey",
        "column": "right",
        "items": [
          {"date": "Q1", "title": "Discovery", "detail": "Mapped 47 services"},
          {"date": "Q2", "title": "Platform Build", "detail": "EKS foundation live"},
          {"date": "Q3", "title": "Migration", "detail": "12 services moved"},
          {"date": "Q4", "title": "Optimization", "detail": "40% cost reduction achieved"}
        ]
      },

      // ─── ROI — Investment breakdown ───
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

      // ─── PROOF-POINTS — Evidence checkmarks ───
      {
        "type": "proof-points",
        "title": "Validated Results",
        "column": "right",
        "items": ["SOC 2 Type II certified", "AWS Well-Architected reviewed", "Zero P1 incidents in 6 months", "Client NPS: 72"]
      },

      // ─── RISKS — Risk management pairs ───
      {
        "type": "risks",
        "title": "Risks Managed",
        "column": "left",
        "items": [
          {"risk": "Data loss during migration", "mitigation": "Blue-green deployment with 3x tested rollback"},
          {"risk": "Performance degradation", "mitigation": "Load tested to 5x peak before cutover"}
        ]
      },

      // ─── NARRATIVE — Prose with optional key insight callout ───
      {
        "type": "narrative",
        "title": "Our Approach",
        "column": "right",
        "insight": "Incremental migration reduced risk by 80%",
        "text": "CI&T used event storming workshops to decompose the monolith into bounded contexts, then migrated services incrementally using the strangler fig pattern."
      },

      // ─── QUOTE — Testimonial with full context ───
      {
        "type": "quote",
        "text": "The CI&T team's deep AWS expertise made all the difference.",
        "author": "Sarah Johnson",
        "author_title": "VP Engineering",
        "company": "NovaPay",
        "role_context": "Led 200-person engineering org"
      }
    ],

    // TECHNOLOGY ARCHITECTURE — Fixed 3x2 card grid at bottom (not customizable)
    "tech_architecture": [
      {"category": "Compute & Orchestration", "description": "Amazon EKS with Karpenter for auto-scaling..."},
      {"category": "Data & Storage", "description": "DynamoDB for transactional data..."},
      {"category": "Event Architecture", "description": "EventBridge as the backbone..."},
      {"category": "Security & Compliance", "description": "AWS KMS for encryption..."},
      {"category": "Observability", "description": "CloudWatch + X-Ray for distributed tracing..."},
      {"category": "CI/CD & DevOps", "description": "GitOps with ArgoCD..."}
    ]
  },

  // ═══════════════════════════════════════════════════════════════════════
  // LEGACY FORMAT (still supported for backwards compatibility)
  // ═══════════════════════════════════════════════════════════════════════
  // If page2.blocks is not present, the system falls back to this format:
  //
  // "page2": {
  //   "include": true,
  //   "deep_dive_title": "NovaPay Cloud Migration",
  //   "page2_left": { "type": "challenges", "title": "...", "items": [...] },
  //   "phases": [...],           // fallback if page2_left not provided
  //   "metrics_table": [...],    // before/after pairs
  //   "tech_architecture": [...]  // 6 category cards
  // }

  "logos": {
    "cit_logo_url": "https://upload.wikimedia.org/wikipedia/commons/5/56/CI%26T_logo.svg",
    "partner_logo_url": "",
    "client_logo_url": ""
  }
}
```

## Metrics by version

Both versions always render exactly three headline metric cards on page 1. **The first card
in each version is reserved for a revenue metric — it is mandatory and cannot be substituted
out.** See the "Non-negotiable rule: the revenue metric" section in SKILL.md for the full
enforcement flow (template → doc mining → user ask → explicit warning).

### CI&T Internal
Focus on business value to CI&T:
- **Services Revenue sold** — total contract value. **MANDATORY — reserved slot #1.**
- **Incentive program funding** — partner program dollars received (MAP, ISV Accelerate, etc.)
- **Deal cycle length** — days from opportunity to close

### Partner-facing
Focus on value to the cloud partner and client outcomes:
- **Annual Cloud Revenue (ACR)** — recurring cloud spend. **MANDATORY — reserved slot #1.**
- **Business outcomes** — measurable client improvements (cost reduction, throughput, etc.)
- **Technology adoption** — number and type of partner services used

### If the revenue metric truly cannot be recovered
The user must be warned explicitly (see SKILL.md). If they choose to proceed anyway, render
the reserved slot as `"—"` with the normal label — do **not** promote a different metric into
the slot or drop the card. The missing dash is a visible reminder that the number is absent.

### Shared across versions
- Incentive programs used, funding amounts
- Deal duration, project approach
- Client challenge and solution narrative

## Writing tone

- **Confident but not boastful.** State results with numbers, let them speak.
- **Concrete over abstract.** "Tripled transaction throughput" not "significantly improved performance."
- **Short sentences in the challenge/solution blocks.** These are scanned, not read deeply.
- **Quote should feel authentic.** It's attributed to a client executive — make it sound like
  something a real CTO or VP would say, not marketing copy.

## Page 1 vs Page 2

**Page 1 (required):** The one-pager. Must contain everything someone needs to understand
the win at a glance: hero with title/subtitle, challenge/solution side by side, 3 key metric
cards, client quote, and context bar with deal details.

**Page 2 (optional):** The deep dive. For people who want more: phased project approach,
full before/after metrics table, and detailed technology architecture cards (6 cards in a
3x2 grid). Only include if the user provides enough detail to fill it meaningfully.

## Content labels by version

| Element | CI&T Internal | Partner (AWS example) |
|---------|--------------|----------------------|
| Topbar label | Win Wire — Internal | Win Wire — Partner |
| Solution label | The Solution | AWS-Powered Solution |
| Metric cards | Revenue, Funding, Cycle | ACR, Cost Reduction, Services |
| Page 2 title prefix | Deep Dive: | Deep Dive: |
| Page 2 approach title | Project Approach | Migration Approach |
| Page 2 metrics title | Full Metrics | Business Outcomes |
| Page 2 tech title | Technology Architecture | AWS Services Adopted |
| Footer prefix | CI&T · Confidential | CI&T & AWS |
