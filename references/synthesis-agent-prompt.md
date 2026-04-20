# Phase 2: Synthesis Agent Prompt

This is Phase 2 of a 2-phase extraction process. This agent receives the raw extraction
from Phase 1 and synthesizes it into the final WinWire content.

**Note:** Phase 2 can be done by the main agent directly (recommended) or by spawning
a dedicated Sonnet agent for complex cases.

## When to use a dedicated agent

**Main agent handles Phase 2 (default):**
- Simpler, has conversation context
- Can ask user clarifying questions naturally
- Good for most cases

**Spawn Sonnet agent for Phase 2:**
- Very large extraction (>50KB raw content)
- Main agent context is already large
- Need fresh perspective on synthesis

## Agent Configuration (if spawning)

```
Agent({
  description: "Synthesize WinWire content from raw extraction",
  model: "sonnet",
  prompt: `
    <paste the template below>
    
    ## Raw extraction from Phase 1
    
    ${JSON.stringify(phase1Output, null, 2)}
    
    ## User-provided context (if any)
    
    - Services Revenue: ${servicesRevenue || "not provided"}
    - ACR: ${acr || "not provided"}
    - Versions to build: ${versions.join(", ")}
  `
})
```

## Prompt Template

```
You are Phase 2 of a 2-phase WinWire extraction process.

Phase 1 has read all project documents and extracted raw content. Your job is to
SYNTHESIZE this into a polished WinWire — not mechanically select, but intelligently
craft a compelling narrative by looking at everything together.

## TL;DR

1. Read ALL the raw extraction before writing anything
2. Understand the full story first — what makes this win compelling?
3. Synthesize across sources — combine the best from each
4. Write coherent narratives, not bullet dumps
5. Ensure page 2 variety: MAX 2 blocks/column, different types per side
6. Output final JSON ready for build_html.py

## Step 1: Understand the full story

Before writing anything, answer these questions:

1. **What's the core narrative?**
   - What was the client's pain?
   - What did CI&T uniquely deliver?
   - What's the headline result?

2. **What's the single most impressive metric?**
   - This goes in the title and/or KPI block

3. **What content is duplicated across files?**
   - Pick the best-phrased version

4. **What's missing that we need to ask the user?**
   - Quote, ACR, revenue, etc.

## Step 2: Craft the narratives

Write these in WinWire tone: confident, concrete, short sentences.

**Title** (≤15 words)
- Include the most impressive metric
- Pattern: "[Client]: [Metric-driven outcome statement]"
- Example: "HEINEKEN: AI-Powered Discovery Cuts B2B Harmonization from Months to 6 Weeks"

**Subtitle** (2-3 sentences)
- What CI&T did + key result + scope
- Make it scannable

**Challenge headline** (≤8 words)
- The pain in punchy form
- Example: "Nine fragmented platforms, one global vision"

**Challenge body** (2-4 sentences)
- Concrete details: system age, scale, specific problems
- Business impact of the pain

**Solution headline** (≤8 words)
- What CI&T built/delivered
- Example: "AI agents that read code before humans"

**Solution body** (2-4 sentences)
- Architecture, methodology, key decisions
- What makes this technically interesting

**Quote** (if found)
- Best testimonial from extraction
- Include speaker, title, company
- If none found, flag as missing

**Technologies**
- Deduplicated list from all sources
- Order by importance/relevance

**Tags** (4-6)
- Industry, partner, project type, key tech
- Example: ["B2B Commerce", "AI-Augmented Discovery", "Hybris → Virto"]

## Step 3: Build page 2 content

Page 2 must be SCANNABLE IN 30 SECONDS. Apply these hard limits:

| Constraint | Limit |
|------------|-------|
| Blocks per column | MAX 2 |
| Timeline items | MAX 4 |
| Comparison items | MAX 2 |
| Takeaway bullets | MAX 3, each ≤8 words |
| Highlights items | MAX 3 |
| Any item detail | ≤10 words |

**Column assignments (ensure variety):**
- LEFT: `takeaway`, `timeline`, `roi`, or `risks`
- RIGHT: `kpi`, `comparison`, `metrics`, or `proof-points`
- NEVER same block type on both sides

**Block selection logic:**
- `takeaway`: Executive "so what" — always include if you can write a compelling one
- `kpi`: Single hero metric with trend — use if you have an impressive number
- `timeline`: Project phases — use if 3-4 clear phases with outcomes
- `comparison`: Before/after — use if you have concrete before AND after values
- `metrics`: Multiple numbers — use if 2-4 strong metrics
- `highlights`: Achievements — use if concrete wins with detail
- `proof-points`: Evidence — use if certifications, validations, awards
- `risks`: Risk management — use if documented risk/mitigation pairs

**Synthesize, don't just copy:**
- Combine related content from multiple files
- Rewrite for conciseness (meet word limits)
- Pick the best version of duplicated content

## Step 4: Build tech_architecture

Fixed 3x2 grid at bottom of page 2. Six cards:

| Category | What to include |
|----------|-----------------|
| Compute / Platform | Main platform, runtime, containers |
| Data / Storage | Databases, storage, data services |
| Integration / Events | APIs, messaging, event systems |
| Security / Compliance | Auth, encryption, compliance |
| Observability | Monitoring, logging, tracing |
| CI/CD / Delivery | Build, deploy, DevOps tools |

If a category has nothing, use a generic description based on the project type.

## Output format

Return valid JSON matching the build_html.py schema:

{
  "project": {
    "client_name": "HEINEKEN International B.V.",
    "anonymize": false,
    "industry": "Consumer Goods / Beverage",
    "partner": "azure",
    "project_type": "B2B Commerce Harmonization",
    "title": "HEINEKEN: AI-Powered Discovery Cuts B2B Harmonization from Months to 6 Weeks",
    "subtitle": "CI&T landed a €236K engagement to re-engineer fragmented B2B SAP Hybris platforms...",
    "tags": ["B2B Commerce", "AI-Augmented Discovery", "Platform Harmonization"]
  },
  
  "challenge": {
    "headline": "Nine fragmented platforms, one global vision",
    "body": "HEINEKEN operates divergent B2B e-commerce stacks across operating companies..."
  },
  
  "solution": {
    "headline": "AI agents that read code before humans",
    "body": "CI&T deployed an AI-enhanced discovery methodology...",
    "technologies": ["SAP Hybris", "Virto Commerce", "Azure", "Anthropic Claude"]
  },
  
  "metrics_internal": {
    "items": [
      {"value": "€236K", "label": "Services Revenue"},
      {"value": "69 days", "label": "Deal Cycle"},
      {"value": "€700K+", "label": "Follow-on Pipeline"}
    ]
  },
  
  "metrics_partner": {
    "items": [
      {"value": "$X.XM", "label": "Annual Cloud Revenue"},
      {"value": "50-60%", "label": "Rules Pre-Captured by AI"},
      {"value": "6 weeks", "label": "Discovery per OpCo"}
    ]
  },
  
  "quote": {
    "text": "...",
    "author": "Name",
    "title": "Title",
    "company": "Company"
  },
  
  "context_bar_internal": [
    {"label": "Engagement Start", "value": "January 2026"},
    {"label": "Contract Structure", "value": "Fixed-fee + T&M"},
    {"label": "OpCos Covered", "value": "Brazil, Mexico"},
    {"label": "Team", "value": "Principal + LATAM delivery"}
  ],
  
  "context_bar_partner": [
    {"label": "Cloud Platform", "value": "Microsoft Azure"},
    {"label": "Discovery Duration", "value": "6 Weeks/OpCo"},
    {"label": "AI Licenses", "value": "12× Anthropic Claude"},
    {"label": "Scope", "value": "Hybris → Virto Migration"}
  ],
  
  "page2": {
    "include": true,
    "title": "Deep Dive: HEINEKEN B2B Commerce Harmonization",
    "blocks": [
      {
        "type": "takeaway",
        "column": "left",
        "headline": "AI rewrites the discovery playbook",
        "bullets": ["50-60% rules pre-captured", "6-week cycles", "SME load cut 70%"]
      },
      {
        "type": "timeline",
        "column": "left",
        "title": "6-Week Discovery",
        "items": [
          {"date": "Weeks 1-2", "title": "AI Preparation", "detail": "Ingest artifacts"},
          {"date": "Weeks 3-4", "title": "SME Sessions", "detail": "Fill gaps only"},
          {"date": "Weeks 5-6", "title": "Delivery", "detail": "Feature map + plan"}
        ]
      },
      {
        "type": "kpi",
        "column": "right",
        "value": "50-60%",
        "label": "Business Rules Pre-Captured",
        "trend": "Before SME interviews",
        "context": "AI agents reverse-engineer from code"
      },
      {
        "type": "comparison",
        "column": "right",
        "title": "Discovery Transformation",
        "items": [
          {"label": "Duration", "before": "Months", "after": "6 weeks", "change": "↓75%"},
          {"label": "SME Load", "before": "Multi-day", "after": "4-8 hours", "change": "↓70%"}
        ]
      }
    ],
    "tech_architecture": [
      {"category": "Commerce Platforms", "description": "SAP Hybris (legacy) → Virto Commerce (.NET)"},
      {"category": "AI Layer", "description": "Anthropic Claude for code analysis and generation"},
      {"category": "Cloud Platform", "description": "Microsoft Azure (target)"},
      {"category": "Integration", "description": "Salesforce SFA/SFDC, ERP connectors"},
      {"category": "Delivery Model", "description": "US Principal + LATAM nearshore team"},
      {"category": "Methodology", "description": "AI-enhanced discovery, artifacts-first approach"}
    ]
  },
  
  "logos": {
    "client_logo_url": ""
  },
  
  "missing": ["Client quote not found", "ACR not specified"]
}

## Quality checklist before outputting

- [ ] Title includes a metric
- [ ] Challenge and solution are 2-4 sentences each, concrete
- [ ] Page 2 has MAX 2 blocks per column
- [ ] Left and right columns use DIFFERENT block types
- [ ] Timeline has ≤4 items, each detail ≤10 words
- [ ] Comparison has ≤2 items (even grid)
- [ ] Takeaway has ≤3 bullets, each ≤8 words
- [ ] Tech architecture has 6 cards
- [ ] Missing items flagged in "missing" array
```

## Handling the output

After synthesis returns:

1. Check `missing` array — ask user for any critical items
2. Present consolidated content preview to user
3. Get approval before building HTML/PDF
