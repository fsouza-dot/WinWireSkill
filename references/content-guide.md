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

  "page2": {
    "include": true,
    "deep_dive_title": "NovaPay Cloud Migration",

    "approach_title": "Project Approach",
    "phases": [
      {
        "name": "Discovery & Domain Mapping",
        "description": "4 weeks of event storming sessions..."
      },
      {
        "name": "Foundation & Platform",
        "description": "Built the EKS-based platform..."
      },
      {
        "name": "Core Services Migration",
        "description": "Migrated the 8 highest-value services..."
      },
      {
        "name": "Optimization & Handoff",
        "description": "Performance tuning, chaos engineering..."
      }
    ],

    "metrics_table": [
      {"metric": "Transaction throughput", "before": "1,200 TPS", "after": "3,800 TPS"},
      {"metric": "Deployment frequency", "before": "Monthly", "after": "Daily"},
      {"metric": "Infrastructure cost / txn", "before": "$0.012", "after": "$0.004"},
      {"metric": "P99 latency", "before": "1,200ms", "after": "180ms"},
      {"metric": "Compliance update lead time", "before": "6-8 weeks", "after": "3-5 days"},
      {"metric": "Platform uptime", "before": "99.5%", "after": "99.99%"}
    ],

    "tech_architecture": [
      {
        "category": "Compute & Orchestration",
        "description": "Amazon EKS with Karpenter for auto-scaling..."
      },
      {
        "category": "Data & Storage",
        "description": "DynamoDB for transactional data..."
      },
      {
        "category": "Event Architecture",
        "description": "EventBridge as the backbone..."
      },
      {
        "category": "Security & Compliance",
        "description": "AWS KMS for encryption..."
      },
      {
        "category": "Observability",
        "description": "CloudWatch + X-Ray for distributed tracing..."
      },
      {
        "category": "CI/CD & DevOps",
        "description": "GitOps with ArgoCD..."
      }
    ]
  },

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
