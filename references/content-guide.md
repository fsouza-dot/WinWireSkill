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
    "title": "Cloud-Native Transformation Unlocks 3x Transaction Throughput",  // *
    "subtitle": "CI&T partnered with NovaPay to migrate their legacy payment processing platform to AWS, delivering a modern microservices architecture that tripled capacity and cut infrastructure costs by 40%.",  // *
    "tags": ["Cloud Migration", "Microservices", "AWS", "FinTech"]  // *
  },

  "challenge": {
    "headline": "A monolith blocking growth",    // *
    "body": "NovaPay's 12-year-old monolithic..."  // * 2-4 sentences
  },

  "solution": {
    "headline": "Event-driven microservices on AWS",  // *
    "body": "CI&T designed and built a cloud-native...",  // * 2-4 sentences
    "technologies": ["Amazon EKS", "AWS Lambda", "DynamoDB", "EventBridge", "Step Functions", "CloudFront"]  // *
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
  // PAGE 2 — FLEXIBLE BLOCKS FORMAT (preferred)
  // ═══════════════════════════════════════════════════════════════════════
  // Page 2 uses content blocks that adapt to whatever compelling content
  // exists. Only include blocks with real content — don't pad with weak content.
  // If no compelling content, set include: false to skip page 2 entirely.

  "page2": {
    "include": true,
    "title": "Deep Dive: NovaPay Cloud Migration",
    "blocks": [
      // METRICS — Big numbers that impress
      {
        "type": "metrics",
        "title": "Business Impact",
        "column": "left",
        "items": [
          {"value": "3.8K TPS", "label": "Transaction Throughput"},
          {"value": "99.99%", "label": "Platform Uptime"},
          {"value": "40%", "label": "Cost Reduction"}
        ]
      },

      // HIGHLIGHTS — Key achievements with details
      {
        "type": "highlights",
        "title": "Key Achievements",
        "column": "right",
        "items": [
          {"headline": "Zero-Downtime Migration", "detail": "2TB database moved without service interruption"},
          {"headline": "PCI Compliant", "detail": "Certified in 3 weeks vs typical 3 months"}
        ]
      },

      // COMPARISON — Before → After pairs
      {
        "type": "comparison",
        "title": "Before & After",
        "column": "left",
        "items": [
          {"label": "Deployment Frequency", "before": "Monthly", "after": "Daily"},
          {"label": "P99 Latency", "before": "1,200ms", "after": "180ms"}
        ]
      },

      // LIST — Technologies, deliverables, phases
      {
        "type": "list",
        "title": "Technologies Deployed",
        "column": "full",
        "style": "bullet",  // or "numbered"
        "items": ["Amazon EKS", "Lambda", "DynamoDB", "EventBridge", "CloudWatch", "ArgoCD"]
      },

      // NARRATIVE — Prose paragraph for context
      {
        "type": "narrative",
        "title": "Our Approach",
        "column": "right",
        "text": "CI&T used event storming workshops to decompose the monolith into bounded contexts, then migrated services incrementally using the strangler fig pattern."
      },

      // QUOTE — Additional testimonials (if not on page 1)
      {
        "type": "quote",
        "column": "full",
        "text": "The CI&T team's deep AWS expertise made all the difference.",
        "author": "Sarah Johnson",
        "author_title": "VP Engineering, NovaPay"
      }
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
